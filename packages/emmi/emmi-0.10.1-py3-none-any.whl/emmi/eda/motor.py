
#!/usr/bin/python3

import time
import asyncio
import logging
import inspect
import traceback
import enum

from functools import partial

logger = logging.getLogger(__name__)

class Motor(object):
    '''
    The simplest of the simplest motors: can only move, report position and stop.

    Generally, the API elements are expected to perform synchronously,
    non-blocking. This is for ease of implementation of motor backends.
    If the motor needs to communicate with hardware, which is generally
    necessary and typically a potentially blocking communication,
    the preferred way is to implement a custom update procedure that
    is called regularly, and have the API elements mark the task to be
    performed when called, and have the update function *actually* perform
    the tasks at a later time.
    
    The following API elements are read-only, i.e. not state-changing:

      - `.pending()`: should return `False` when the motor is ready to use;
        converesly, must retur `True` when either the motor is not yet
        initialized (e.g. because the object was created, but the initial
        status update wasn't performed yet), or when a state-altering
        command (e.g. `.goto()`) was issued but wasn't trasfered to the
        hardware anymore. Any other API call except for another call to
        `.pending()` is undefined as long as `.pending()` is `True`.

      - `.moves()`: must report  `True` if the motor is busy; generally,
        this is expected to mean "executing a motion" but can mean whatever
        the motor might be doing, e.g. initilizing or performing a custom
        recovery operation. Reports `False` if the motor is ready to take
        on new tasks

      - `.where()`: must always report the current position of the motor,
        and the position must always be well-defined if
        `.pending() == False`.

    The following API elements usually modify the state of the motor.
    By registering / triggering hardware communication on the next update
    loop, they mostly they cause `.pending()` to immediately return `True`.
    although that's not a requirement:

      - `.goto(x)`: the main task of a motor, to move to the absolute
        position `x`

      - `.stop()`: immediatedly cancel / stop the current task, in
        particular (but not only) if it's a movement, and work towards
        entering a non-moving state.

    These are error-handling API elements:
    
      - `.errors`: expected to return an iterable with current errors.
        Generally, higher layers will refuse to operate the motor (except
        for `.stop()`) when this list is non-empty. Once errors pop up
        in the errors list, they are expected to remain there until
        explicitly cleared. There's no specific error type to use. The
        code tries to make no assuptions, but it's been mostly tested
        with the Python `str` type, so be prepared to hunt some bugs
        if you choose something else.

      - `.clear()`: explicitly clear the current error list. If the
        error-causing circumstance still persists, the motor may update
        the error list on the next update cycle.

    External flags / extensions:

      - `.flags`: an iterable to return custom flags. There's no explicit
        expectation of a type, but generally the code uses `str`.
        There are a number of flags that the base motor API suggests,
        but the user can and is expected to expand this list. The list
        currently include:
          - `Motor.HLIM`: flag to indicate that the high-limit switch is on
          - `Motor.LLIM`: flag to indicate that the low-limit switch is on

    Note that this is the *base API* that EMMI layers will depend on -- in
    particular it's the one used by the EMMI `MotorEngine`, which in turn
    is used by the generic EMMI IOC infrastructure elements.

    Common tasks usually expected, but not always 100% required for motor
    functionliaty, like homing, setting acceleration and speed, etc, are
    deliberately not specified in this API. However, there *do* exist
    "motor mix-in classes" to implement these functions in a way as to
    be compatible with higher EMMI layers.
    '''

    # Common flags that _must_ be supported by every motor.

    # High-limit reached; no more `goto()` supported where the target
    # position is higher than the current `where()`.
    HLIM = "HLIM"

    # Low-limit reached; no more `goto()` supported where the target
    # is lower than the current `where()`.
    LLIM = "LLIM"

    def __init__(self, *args, **kwargs):
        ''' Creates a mock-up of an EDA Motor.

        Accepts all args as a courtesy of being a good mock-up class,
        but ignores most of them. A number of arguments are specific
        to the mock class. They are listed below.

        Args:
            mock_timeslice: a measure of how "fast" a mock motor is moving.
              Every `.goto()` call on a mock motor will execute a movement
              of the specified distance in exactly `mock_timeslice` seconds,
              regardless of the distance.

            limits: tuple of `(low, high)` to simulate the lower,
              respectively higher hardware limits. If any of those
              is reached in the mocking position, `.flags` will contain
              `"LLIM"` or `"HLIM"`, respectively. Alternatively, this can
              also be a dictionary with two or three items. If it's two
              items, it's used as the low/high limits, and the
              keys are used in `.flags` instead of `"HLIM"`/`"LLIM"`.
            
        '''
        self.mock_timeslice = kwargs.get('mock_timeslice', 5.0)
        self.start = 0.0
        self.target = 0.0
        self.tstamp = 0.0
        self.errors = []
        self._limits = kwargs.get('limits', None)

    def pending(self):
        '''
        As the actions of a motor are required to be non-blocking, most of the
        actions that need to communicate with hardware will not *actually* do
        anything when called directly; they will instead mark an action as
        to-be-done, and actually execute it in an implementation-dependent
        update() step.

        `.pending()` marks this "yet-to-communicate" state of the object.
        
        It is also used in the beginning, right after initialization, when
        the motor object already exists (and in theory is ready to be used),
        but the first communication / status request from the hardware isn't
        in yet.
        '''
        return False
    
    def where(self):
        '''
        Returns current position -- that is the position that we'd be currently
        having if we'd wanted to go from "current" towards "target" within
        the timeslice "mock_timeslice"
        '''
        tdelta = (time.time()-self.tstamp)
        if tdelta > self.mock_timeslice:
            tdelta = self.mock_timeslice
        dist = self.target-self.start
        return self.start + dist * (tdelta/self.mock_timeslice)

    def goto(self, val):
        '''
        Sends command to move to position (doesn't wait)
        '''
        self.start = self.where()
        self.target = val
        self.tstamp = time.time()

    def stop(self):
        '''
        Sends command to stop (doesn't wait). Technically, we'll be still
        in state "moving" for a while after this, but we'd be moving
        towards the position we're already onto.
        '''
        if self.moves():
            self.goto(self.where())

    def moves(self):
        '''
        Returns True if the motor moves. We fake this by testing whether
        we're still within the "timeslice". This has the added benefit
        that sometimes moves() returns False right away (i.e. if we weren't
        moving in the first place), and sometimes still returns False
        for a considerate amount of time (i.e. until the end of the current
        slice) if we were moving and just received a stop() command.
        '''
        now = time.time()
        return (now - self.tstamp) <= self.mock_timeslice

    def clear(self):
        '''
        Clears all outstanding error flags (they may pop up again).
        '''
        self.errors = []


    @property
    def flags(self):
        ''' Check for HLIM / LLIM and return the appropriate strings.

        Strings are either default "HLIM", "LLIM" respectively, or
        the keys of the `._limits` parameter.
        '''
        if self._limits is None:
            return set()

        f = set()

        lk = [k for k in self._limits.keys()]

        low = (self.LLIM, self._limits[0]) if not isinstance(self._limits, dict) \
            else (lk[0], self._limits[lk[0]])

        high = (self.HLIM, self._limits[-1]) if not isinstance(self._limits, dict) \
            else (lk[-1], self._limits[lk[-1]])

        p = self.where()
        
        if p <= low[1]:
            f.add(low[0])

        if p >= high[1]:
            f.add(high[0])

        return f


# Rename
MockMotor = Motor
    
    
class HomingMotorMixin:
    '''
    Mixin class to expand the `Motor` class by `.home(x)`
    functionality.
    '''

    # Flag to indicate the fact that the motor has peformed
    # a successful homing operation.
    HOMED = "HOMED"

    def home(self, positive=None):
        '''
        Perform a homing movement. If `positive` is `True`,
        attempt homing in positive direction. If it is `False`,
        try the negative direction.

        Default is `None`, which leaves it to the implementation
        to do the homing.
        '''
        raise RuntimeError(f'Not implemented')


class VelocityMotorMixin:
    '''
    Mixin class to allow setting and reading of the movement
    velocity.
    '''

    def velocity(self, val=None):
        '''
        Setter and getter for the perferred velocity.
        
        If `val` is `None`, read and return the current velocity.
        Otherwise set the velocity to the specified value (only
        the absolute value will be considered, the direction
        is determined by the main class's `.goto()` function).
        '''
        raise RuntimeError(f'Not implemented')

    
    def max_velocity(self, val=None):
        '''
        Setter and getter for the maximum velocity. Typically
        the same as `.velocity()` (which is what the default
        implementation also does), but this allows it to
        be defined differently.
        '''
        return self.velocity(val)


    def home_velocity(self, val=None):
        '''
        Setter and getter for the homing velocity, if different
        from the default velocity. Default implementation
        is just a wrapper for `.velocity()`.
        '''
        return self.velocity(val)


    def base_velocity(self, val=None):
        '''
        Setter and getter for a "base velocity", if different
        from the default velocity. Default implementation
        is just a wrapper for `.velocity()`.
        '''
        return self.velocity(val)


    def jog_velocity(self, val=None):
        '''
        Setter and getter for the jogging velocity, if different
        from the default velocity. Default implementation
        is just a wrapper for `.velocity()`.
        '''
        return self.velocity(val)    
