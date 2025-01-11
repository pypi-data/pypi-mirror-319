import enum, logging, traceback, asyncio, inspect
from functools import partial

logger = logging.getLogger(__name__)

class MotorState(enum.IntEnum):
    INIT  = 0
    IDLE  = 1
    BUSY  = 2
    STOP  = 3
    ERROR = 4
    FAIL  = 5


class MotorEngine(object):
    '''
    Generic motor engine class. Essentially cycles through the states
    as it should, and serves the most basic properties `position` and
    `position_relative` correctly. It's based on generic True/False
    conditional procedures to decide when to switch.

    In its default incarnation, the conditionals are just generic waiting
    functions (1 second for anything), so it can be used as a mock-up for
    unit testing. But if you replace the conditionals by things that do
    "real stuff", it's actually usable for production.
    '''
    
    def __init__(self, motor=None, init_probe=None):
        '''
        Initializes a motor engine.

        Args:
            motor: a `MockMotor` compatible motor hardware driver
        
            init_probe: if not `None`, it's a callable of the form `func(motor)`,
              which should return `False` for as long as the motor is still
              initializing.)
        '''
        
        self.__motor = motor or MockMotor()

        # current state
        self.__state = "INIT"
        self.__old_state = None

        self.__init_probe = init_probe

        # sub-type of the "BUSY" state
        self.__business = None

        # When this is not None, it is expected to hold a tuple
        # (name, work_callable, busy_callable) that triggers a new BUSY state.
        # "name" is the name of the business (essentially a nice label for the user)
        # "work_callable" is a function that triggers the action
        # "busy_callable" is a function that evalues to True for as long as the
        #                 motion persists.
        self.__scheduled_go = None

        # This is the similar to "__scheduled_go", only that the name is "STOP",
        # the go-callable is motor.stop(), and busy_check is motor.moves().
        # It's necessary to keep this separate from __scheduled_go because this
        # is actually supposed to be able to preemt __scheduled_go at any time.
        # This needs for special handling in the code.
        self.__scheduled_stop = None

        self.__state_hooks = {}

    @property
    def _hooks(self):
        return self.__state_hooks


    def add_hook(self, proc, states=None):
        '''
        Adds a hook to be called when the corresponding state is entered.
        The hook is of the signature `def proc(state, entering)`,\
        with `entering` being a boolean that is `True` once per state-cycle,
        when the corresponding state is being transitioned into.

        The hook function may be a coroutine (asyncio), in which case it will
        be awaited for.

        Hooks are only handled inside this object's own `.run()` method. If you're
        implementing your own loop, by stepping through the states using the
        (non-blocking) `.state_proc()`, then you need to take care of the hooks
        yourself. The `add_hook()` / `remove_hook()` functionality for tracking
        the registered hooks is still at your disposal, but the hooks will simply
        not be executed.

        Returns a handle object that can be used to remove the hook (i.e.
        by using `.remove_hook()`).
        '''
        if states in (None, "all"):
            states = ['INIT', 'IDLE', 'BUSY', 'STOP', 'ERROR', 'FAIL' ]
            
        hook_ref = {}
        for s in states:
            pl = self.__state_hooks.setdefault(s, [])
            pl.append(proc)
            hook_ref.setdefault(s, pl[-1])

        return hook_ref


    def remove_hook(self, obj_list):
        for sname, sproc in obj_list.items():
            self.__state_hooks[sname].remove(sproc)


    @property
    def business(self):
        if self.__state in [ "BUSY", ]:
            return self.__business
        else:
            return None
    

    @property
    def errors(self):
        return self.__motor.errors


    @property
    def flags(self):
        return self.__motor.flags


    def state_INIT(self, state):
        # ...put init stuff here.
        if self.__init_probe is None:
            if self.__motor.pending():
                return state
            else:
                return "IDLE"
        if self.__init_probe(self.__motor):
            return "IDLE"
        
        return "INIT"


    # STOP state: trigger STOP hardware command, stay here while hardware is moving
    def state_enter_STOP(self, state):
        if self.__scheduled_stop:
            self.__scheduled_stop[1]()
        return state

    def state_STOP(self, state):
        if self.__scheduled_stop and self.__scheduled_stop[2]():
            return "STOP"
        self.__scheduled_go = None
        self.__scheduled_stop = None
        if len(self.errors) > 0:
            return "ERROR"
        return "IDLE"


    # BUSY state: trigger busy action, stay here while action not done
    def state_enter_BUSY(self, state):
        if self.__scheduled_stop: # STOP trumps everything
            logger.debug(f'BUSY: {self.__scheduled_go["name"]} requested, '
                         f'but also have a stop request pending')
            return "STOP"
        
        logger.debug(f'BUSY: {self.__scheduled_go["name"]}')
        try:
            self.__scheduled_go["proc"]()
        except Exception as e:
            logger.error(f'msg="Business raised exception" error="{str(e)}"')
            return "FAIL"
        return "BUSY"
    

    def state_BUSY(self, state):
        
        if len(self.errors) > 0:
            logger.info(f'state={state} exit=STOP reason="{len(self.errors)} errors"')
            return "STOP"
        
        if self.__scheduled_stop is not None:
            logger.info(f'state={state} exit=STOP reason="scheudled"')
            return "STOP"
        
        if self.__scheduled_go["busy"]() == False:
            logger.info(f'state={state} exit=STOP reason="finished"')
            return "STOP"

        return state    


    # IDLE state: stay here until there is work scheduled.
    def state_IDLE(self, state):
        
        if len(self.errors) > 0:
            logger.debug(f'Have {len(self.errors)}, STOP-ing motor')
            return "STOP"
        
        if self.__scheduled_go is not None:
            self.__business = self.__scheduled_go["name"] or "(default)"
            logger.debug(f'Going BUSY, business {self.__business}')
            return 'BUSY'

        return state


    def state_ERROR(self, state):
        '''
        The only way we can leave ERROR is by clearing/going to IDLE
        '''
        if len(self.errors) == 0:
            return "IDLE"


    # There's no escape from death.
    def state_FAIL(self, state):
        pass
             

    def state_proc(self):
        ## State procedures -- execute the current state procedure.
        ## If the state (just) switched, execute "state_enter_{state}" instead.
        
        state = self.__state

        # BUSY state needs some special treatment -- it may be of the form 'BUSY.{}'
        s_proc_name = state if not state.startswith("BUSY.") else state[:4]
        s_proc = getattr(self, f'state_{s_proc_name}')

        #print(f"State run: {self.__old_state} {state}")

        # If we just entered the current state, maybe there's a dedicated state_enter_{...}
        if state != self.__old_state:
            logger.debug ("State: %s -> %s" % (self.__old_state, state))
            try:
                s_proc = getattr(self, f'state_enter_{state}')
            except AttributeError:
                pass

        new_state = s_proc(state)
            
        self.__old_state = state

        if new_state is not None:
            self.__state = new_state

        return self.__state


    async def _run_hooks(self, state_from, state_to):
        entering = (state_from != state_to)
        wait_for = []

        if not state_to in self.__state_hooks:
            return
        
        for proc in self.__state_hooks[state_to]:
            try:
                p = proc(state_to, entering)
            except Exception as e:
                logger.error(f'state={state} hook="{proc}" '
                             f'msg="Raised exception" '
                             f'error="{e}"')
            if inspect.iscoroutine(p):
                wait_for.append(p)
        await asyncio.gather(*wait_for, return_exceptions=False)


    async def run(self, period=0.01, stop_on_fail=True):
        '''
        Async function to run the Motor Engine
        '''

        last_state = None
        
        if self.__state == "FAIL":
            raise RuntimeError("Attempted to start a motor engine in a failed state")

        while (self.__state not in [ "FAIL" ]) or (not stop_on_fail):
            try:
                current_state = self.state_proc()
                await asyncio.gather(asyncio.sleep(period),
                                     self._run_hooks(last_state, current_state),
                                     return_exceptions=False)
                last_state = current_state
                
            except Exception as e:
                logger.error(f'Motor engine failed: {str(e)}')
                logger.error(traceback.format_exc())
                self.__state == "FAIL"
                raise

        logger.error("Motor engine in FAIL state")

        
    @property
    def state(self):
        '''
        Returns the current state
        '''
        return self.__state

    
    def step(self):
        '''
        Returns the current state after having performed one state-step.
        '''
        return self.state_proc()
    
    
    # Current position -- getter reads out the hardware, setter
    # is a bit more complicated because we have to acknowledge
    # the current state (i.e. can't just override current states).
    @property
    def position(self):
        return self.__motor.where()
    
    @position.setter
    def position(self, val):
        self.go(val)

    
    def stop(self):
        '''
        Triggers an exit from any BUSY state into stop.
        '''        
        self.__scheduled_stop = ("stop",
                                 lambda: self.__motor.stop(),
                                 lambda: self.__motor.moves())
        logger.debug(f"Stop requested, current state is {self.state}")
        
        
    def go(self, call, *call_args,
           name=None,
           done_flag=None,
           busy_flag=None,
           busy_check=None,
           **call_kwargs):
        '''
        Triggers a work session / BUSY round.

        Args:
        
            call: work task. If it's a callable, it's called as it is.
              If it's a string, it is interpreted to be a member of the motor instance
              that the Engine was passed, and is called with `*call_args` and `**call_kwargs`
              as parameters. `call` can be omitted altogether, in which case the
              motor's `.goto()` function is assumed.

            name: if not `None`, then the full state will be `BUSY.{name}`. Otherwise
              it's just `BUSY` if `call` is a true callable, or `BUSY.{call}` if `call`
              was passed as a string.

            done_flag: if not `None`, the presence of this flag in `motor.flags` indicates
              that the work has finished.

            busy_flag: if not `None`, the presence of this flag in `motor.flags` indicates
              that the device is still busy performing this task.

            busy_check: if not `None`, it is expected to be a callable which returns `True`
              while the device is still busy peforming the task.

            *call_args, **call_kwargs: named and unnamed arguments to pass to `call`.

        Returns: the result of the `call` call.
        '''

        # go call
        if hasattr(call, "__call__"):
            # callable is an explicit lambda or similar
            callable = call
            
        elif isinstance(call, str):
            # callable is a string-named member of the motor
            callable = getattr(self.__motor, call)
            if name is None:
                name = call

        else:
            # default parameter 'call' is a number, callable is suppsoed to be 'goto',
            # and we need to place the number in front of the call_args list, in fact.
            callable = self.__motor.goto
            call_args = tuple([call] + list(call_args))
            name = "goto"

        # busy call
        if hasattr(busy_check, "__call__"):
            busy_callable = busy_check
            
        elif done_flag is not None:
            busy_callable = lambda: done_flag not in self.__motor.flags
            
        elif busy_flag is not None:            
            busy_callable = lambda: busy_flag in self.__motor.flags
            
        else:
            def still_busy():
                #print(f'pending={self.__motor.pending()} moves={self.__motor.moves()}'
                #      f' flags={self.__motor.flags}')
                return self.__motor.pending() or self.__motor.moves()
            busy_callable = still_busy

        self.__scheduled_go = {
            'name': name,
            'proc': partial(callable, *call_args, **call_kwargs),
            'busy': busy_callable
        }

        logger.debug(f"New go: {self.__scheduled_go}")

        
    def motor_clear(self):
        self.__motor.clear()


    async def motor_async_get(self, prop):
        '''
        Tries to set a motor property and returns when it is available.
        If the motor property is an avaitable, it is being awaited.
        If it is a regular function, the motor is awaited for `.pending()`
        to become `False`, then the value of the property is returned.
        If it is a property or field, it is returned as-is, without waiting
        for `.pending()`.
        '''
        # This is either a value, or a function (possibly coroutine)
        p = getattr(self.__motor, prop)

        if self.state == "FAIL":
            logger.error(f'motor={self.__motor.name} prop="{prop}" '
                         f'msg="Ignoring get request during FAIL engine state"')            
            return None        
        
        if inspect.iscoroutinefunction(p):
            return await p()
        if inspect.ismethod(p):
            while self.__motor.pending() == True:
                await asyncio.sleep(1e-6)
            return p()
        return p


    async def motor_async_set(self, prop, val):
        '''
        Sets a property and waits for the completion.
        If the motor property is an avaitable, it is being awaited.
        If it is a regular function or a property, it is set directly.
        '''        
        p = getattr(self.__motor, prop)

        if self.state == "FAIL":
            logger.error(f'motor={self.__motor.name} prop="{prop}" '
                         f'msg="Ignoring set request during FAIL engine state"')
            return None        
        
        if inspect.iscoroutinefunction(p):
            return await p(val)
        if inspect.ismethod(p):
            return p(val)
        else:
            return setattr(self.__motor, prop, val)
        



class WorkerObject(object):
    '''
    Interface for a worker object to be managed by a WorkerEngine.
    '''
    def work(self, params):
        pass

    def abort(self):
        pass

    def clear(self):
        pass

    def isBusy(self):
        pass


class WorkerEngine(object):
    '''
    This models an EPICS device that "does something." It's the precursor of
    a positioner (e.g. a Motor) in the sense that it has a simple state
    diagram which shows whether the device is currently busy performing a
    task ("BUSY"), or free to accept tasks ("IDLE").

    The complete state diagram is as follows:

      - INIT: starting up, ends up in IDLE

      - IDLE: waiting for tasks, can exit through BUSY or ERROR

      - BUSY: currently performing, can exit through DONE or ERROR

      - DONE: done performing, cleaning up / waiting to go to IDLE

      - ERROR: error, user needs to acknowledge

      - FAIL: irrecoverable error

    The state names are configurable.
    '''
    
    def __init__(self, stateNames=None):

        self.states = stateNames or {
            'INIT': 'INIT',
            'IDLE': 'IDLE',
            'BUSY': 'BUSY',
            'DONE': 'DONE',
            'ERROR': 'ERROR',
            'FAIL': 'FAIL'
        }

        # All should return the 
        self.state_workers = {
            'INIT': self.state_INIT,
            'IDLE': self.state_IDLE,
            'BUSY': self.state_BUSY,
            'DONE': self.state_DONE,
            'ERROR': self.state_ERROR,
            'FAIL': self.state_FAIL
        }

        # Initial work do be done when entering a state -- no return value.
        self.state_entries = {
            'INIT': self.enter_state_INIT,
            'IDLE': self.enter_state_IDLE,
            'BUSY': self.enter_state_BUSY,
            'DONE': self.enter_state_DONE,
            'ERROR': self.enter_state_ERROR,
            'FAIL': self.enter_state_FAIL
        }

        self.__state = self.states["INIT"]
        self.__do_run = True
        

    def enter_state_generic(self):
        pass

    # Ignore INIT for now, jump straight to IDLE
    enter_state_INIT = enter_state_generic
    def state_INIT(self):
        return "IDLE"
    
    # FAIL is easy, it does nothing.
    def enter_state_FAIL(self):
        log.error("Entered FAIL -- tttthat's all, folks!")
    def state_FAIL(self):
        return "FAIL"

    # The rest... just wait.
    enter_state_IDLE = enter_state_generic
    enter_state_BUSY = enter_state_generic
    enter_state_DONE = enter_state_generic
    enter_state_ERROR = enter_state_generic

    async def run(self, period=0.1):
        while self.__do_run:
            tstart = time.time()
            current_state = self.__state
            new_state = self.state_workers[current_state]()
            if new_state != current_state:
                logger.debug("State: %r -> %r" % (current_state, new_state))
                self.__state = new_state
                self.state_entries[new_state]()
            tdiff = time.time()-tstart
            await asyncio.sleep(tdiff)
