# implements a CAproto based PVGroup for MotorEngine

from caproto.server import PVGroup, pvproperty
from caproto import ChannelType, ChannelDouble, ChannelString

from emmi.eda.worker import MotorEngine, MotorState
from emmi.eda.motor import Motor

import asyncio, logging, random, string, os

import pprint

logger = logging.getLogger(__name__)

class EpicsMotorFlags:
    PositiveDirection = 0x0001 #  1. DIRECTION: last raw direction; (0:Negative, 1:Positive)
    Done        = 0x0002 #  2. DONE: motion is complete.
    HighLimit   = 0x0004 #  3. PLUS_LS: plus limit switch has been hit.
    HomingLimit = 0x0008 #  4. HOMELS: state of the home limit switch.
                         #  5. Unused
    Position    = 0x0020 #  6. POSITION: closed-loop position control is enabled.
    SlipStall   = 0x0040 #  7. SLIP_STALL: Slip/Stall detected (eg. fatal following error)
    AtHome      = 0x0080 #  8. HOME: if at home position.
    HaveEncoder = 0x0100 #  9. PRESENT: encoder is present.
    MotorFault  = 0x0200 # 10. PROBLEM: driver stopped polling, or hardware problem
    Moving      = 0x0400 # 11. MOVING: non-zero velocity present.
    GainSupport = 0x0800 # 12. GAIN_SUPPORT: motor supports closed-loop position control.
    CommError   = 0x1000 # 13. COMM_ERR: Controller communication error.
    LowLimit    = 0x2000 # 14. MINUS_LS: minus limit switch has been hit.
    IsHomed     = 0x4000 # 15. HOMED: the motor has been homed.

    # Unsupported
    EmegencyStop = 0x0000
    

# Yep. SPEC uses different flags *facepalm*
class SpecMotorFlags:
    Moving        = 0x0002
    LowLimit      = 0x0004
    HighLimit     = 0x0008
    EmergencyStop = 0x0010
    MotorFault    = 0x0020

    # Unsupported (set to 0x0000), but required by MotorRecordBase
    Done              = 0x0000
    PositiveDirection = 0x0000
    

class MotorRecordBase(PVGroup):
    '''
    Basic implementation of an EPICS motor record, based on the base version
    of the EMMI MotorEngine.
    '''

    mrec = pvproperty(name='', value=0.0, record='motor')
    state = pvproperty(name=".state", value=MotorState.INIT)
    clear = pvproperty(name=".clear", value=0)
    error = pvproperty(name=".error", max_length=40, dtype=ChannelType.STRING)

    def __init__(self, name, motor=None, engine=None, prefix=None, env=None, **kwargs):
        '''
        Initializes a basic version of an EPICS MotorRecord as a CAproto async PVGroup.
        We are using the EMMI motor model.

        Args:
        
            prefix: The EPICS motor prefix to use.

            motor: The motor object to use. Either this, or `engine`, must be
              specified. If this is not `None`, a standard `emmi.eda.MotorEngine`
              will be instantiated. This can be used for moving and minds the
              limits, but doesn't have any features beyond that.

           engine: The `emmi.eda.MotorEngine` object to use. If this is specified,
              the `motor` parameter is ignored.
        '''

        self._env = env.copy() if env is not None \
            else os.environ.copy()

        self.MotorFlags = {
            'epics': EpicsMotorFlags,
            'spec': SpecMotorFlags
        }[self._env.get('EMMI_MOTOR_FLAGS', 'epics').lower()]
        
        if motor is None and engine is None:
            raise RuntimeError(f'Have no motor to work with')

        if engine is not None:
            self.engine = engine
        else:
            self.engine = MotorEngine(motor)

        if prefix is None:
            prefix = f'{name}:' if name is not None \
                else f'{"".join(random.choices(string.ascii_lowercase, k=6))}:'
        logger.info(f'motor="{name}" prefix={prefix}')

        # hardware motor status flags writing shadow (see MotorFlags)
        self._motor_flags = 0

        # cannot _update during INIT (no hardware connection yet)
        self.engine.add_hook(self._update, states="all")
        self.engine.add_hook(self._idle_prepare, states=['IDLE'])
        self.engine.add_hook(self._motion_enter, states=["BUSY", "STAGING"])
        self.engine.add_hook(self._motion_exit, states=["IDLE", "ERROR" ])
        
        super().__init__(prefix=prefix, name=name, **kwargs)

        self._init_fields()


    def _init_fields(self):
        self._motor_fields = self.mrec.field_inst
        self._motor_fields.value_write_hook = self._value_write_hook        

    @classmethod
    async def _update_field(self, field, new_value, update_fields=False):
        if new_value != field.value:
            await field.write(new_value, update_fields=update_fields)
            
    async def _value_write_hook(self, inst, val):
        logger.info(f'name={self.name} go={val}')
        old_val = self.engine.position
        if old_val < val:
            self._prepare_flags(set=["PositiveDirection"])
        else:
            self._prepare_flags(clear=["PositiveDirection"])
        self.engine.go(val)

        
    def _prepare_flags(self, clear=None, set=None):
        # clears/sets a number of flags
        if set is None:
            set = []
        if clear is None:
            clear = []

        for f in set:
            val = getattr(self.MotorFlags, f)
            self._motor_flags |= val

        for f in clear:
            val = getattr(self.MotorFlags, f)
            self._motor_flags &= ~val
            

    def _prepare_clear_flag(self, flag):
        self._motor_flags &= ~flag


    async def _motion_enter(self, state, enter):
        # Called when a motion state is entered (i.e. motion begins)
        if (enter != True):
            return

        logger.info(f'name={self.name} msg="Starting motion" state={state} entering={enter}')
        
        f = self._motor_fields
        
        self._prepare_flags(clear=["Done"], set=["Moving"])
        
        await asyncio.gather(
            MotorRecordBase._update_field(f.motor_is_moving, 1),
            MotorRecordBase._update_field(f.done_moving_to_value, 0),
            return_exceptions=False
        )


    async def _motion_exit(self, state, enter):
        # Called when a motion state is exitted (i.e. done moving)
        if (enter != True):
            return

        logger.info(f'name={self.name} msg="Finishing motion" state={state} entering={enter}')
        
        f = self._motor_fields
        
        self._prepare_flags(clear=["Moving"], set=["Done"])
        
        await asyncio.gather(
            MotorRecordBase._update_field(f.motor_is_moving, 0),
            MotorRecordBase._update_field(f.done_moving_to_value, 1),
            return_exceptions=False
        )

        
    async def _update(self, state, enter):
        
        # Called on every state step, expected to update essential values
        # like RBV and limit states
        f     = self._motor_fields
        rbv   = self.engine.position
        flags = self.engine.flags
        error = self.engine.errors[-1] if len(self.engine.errors)>0 else ""
        await asyncio.gather(
            MotorRecordBase._update_field(self.state, self.engine.state),
            MotorRecordBase._update_field(f.user_readback_value, rbv),
            MotorRecordBase._update_field(f.dial_readback_value, rbv),
            MotorRecordBase._update_field(f.raw_readback_value, rbv),
            MotorRecordBase._update_field(f.user_high_limit, Motor.HLIM in flags),
            MotorRecordBase._update_field(f.user_low_limit, Motor.LLIM in flags),
            MotorRecordBase._update_field(f.motor_status, self._motor_flags),
            MotorRecordBase._update_field(self.error, error),
            return_exceptions=False
        )

        if f.stop.value != 0:
            self.engine.stop()
            await MotorRecordBase._update_field(f.stop, 0)


    async def _idle_prepare(self, state, enter):
        if enter == True:
            await self.clear.write(0)

    @mrec.startup
    async def mrec(self, inst, val):
        await asyncio.gather(
            self.engine.run(),
            asyncio.sleep(0.01),
            return_exceptions=False
        )            


    @clear.putter
    async def clear(self, inst, val):
        if val > 0:
            self.engine.motor_clear()



#async def VELO(self, inst, val):

## This should actually be part of MotorRecordVelocityMixin, but
## we can't defined it there owing to a cyclic dependency from insive
## _velo_pvproperty.
async def _velo_putter(group_obj, inst, val):
    # find variant name
    for vname,obj in group_obj._variants.items():
        if obj == inst:
            print(f'Putting: {vname} <- {val}')
            await group_obj.engine.motor_async_set(vname, val)
            return
    raise RuntimeError(f'Variant name for {inst.name} not found -- this is a bug')


            
def _velo_pvproperty(*args, **kw):
    kw.update({
        'dtype': ChannelType.DOUBLE,
        'put': _velo_putter,
    })
    
    return pvproperty(*args, **kw)


class MotorRecordVelocityMixin(PVGroup):
    '''
    Motor record mixin for .VELO field.
    '''
    
    VELO = _velo_pvproperty(name=".VELO")

    def __init__(self):
        self.engine.add_hook(self._velo_update,
                             states=['IDLE', 'BUSY', 'STOP', 'ERROR', 'FAIL'])
        self._variants = {
            'velocity': self.VELO,
        }


    async def _velo_update(self, state, enter):
        async def _read_and_update(self, vname):
            data = await self.engine.motor_async_get(vname)
            pv = self._variants[vname]
            await MotorRecordBase._update_field(pv, data)
        updates = [ _read_and_update(self, vname) for vname in self._variants ]
        await asyncio.gather(*updates, return_exceptions=False)
