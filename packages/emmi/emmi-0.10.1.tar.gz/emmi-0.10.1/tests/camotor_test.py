
from emmi.eda.motor import (
    Motor,
    MockMotor,
    VelocityMotorMixin,
    HomingMotorMixin
)

from emmi.eda.worker import MotorEngine, MotorState

from emmi.api.caproto import (
    MotorRecordBase,
    MotorRecordVelocityMixin
)

from caproto.asyncio.server import run as server_run
from caproto.sync.client import read as ca_read
from caproto.sync.client import write as ca_write
from caproto import CASeverity

from caproto import ChannelType

from caproto.asyncio.client import Context as ClientContext

import pytest, os, sys, random, string, time, pprint, asyncio, traceback

import multiprocessing as mp


class EdaTestMotor(VelocityMotorMixin, MockMotor):
    
    def __init__(self, *args, **kw):
        MockMotor.__init__(self, mock_timeslice=5.0, **kw)
        VelocityMotorMixin.__init__(self)

    def goto(self, val):
        if val > 665.5 and val < 666.5:
            print(f'ERROR triggered by move-value {val}')
            self.errors.append(f'666 apparently is evil')
        if val > 666.5 and val < 667.5:
            print(f'FAIL triggered by move-value {val}')
            raise RuntimeError(f'667 is beyond evil')
        return super().goto(val)


    def velocity(self, val=None):
        if val is None:
            if hasattr(self, '_velo'):
                return self._velo
            return 0.0
        else:
            # Misusing the error flag here to transmit a message
            # via CA/EPICS to the testing class :)
            # Also, we actually always set the same velocity to
            # be able to check if the higher-level (IOC) part properly
            # queries the velocity, and doesn't just rely on the last
            # value that was set.
            self._velo = 6.28
            self.errors.append(f'VELO-set')
    
    
class MotorPvClass(MotorRecordVelocityMixin,
                   MotorRecordBase):

    _loop_slow_down_period = 0.3

    def __init__(self, *a, **kw):
        MotorRecordBase.__init__(self, *a, **kw)
        MotorRecordVelocityMixin.__init__(self)

        # If the state loop runs too fast, the state succession will not reach through
        # the PVs as it's supposed to. This is an issue of the channel-access
        # protocol (apparently), not of the Engine.
        # But for unit testing of the Engine, we really need a clean recording of the
        # succession of statest. So we're artificially slowing down.
        self.engine.add_hook(self._slow_down_loop, states="all")


    async def _slow_down_loop(self, state, enter):
        await asyncio.sleep(self._loop_slow_down_period)


@pytest.fixture(scope="session")
def session_ioc_prefix():
    return ''.join(random.choices(string.ascii_lowercase, k=7))+':'


def camotor_ioc_main(name, prefix):
    pvg = MotorPvClass(name, motor=EdaTestMotor(), prefix=prefix)
    print(f'IOC database:')
    pprint.pprint(pvg.pvdb.keys())
    return server_run(pvg.pvdb)


@pytest.fixture(scope="module")
def camotor_ioc(session_ioc_prefix):
    motor_name = 'motor'
    motor_ioc_prefix = f'{session_ioc_prefix}{motor_name}'
    p = mp.Process(target=camotor_ioc_main, args=[motor_name, motor_ioc_prefix])
    p.daemon = True     ## daemon mode will ensure that IOC exits when main process exits
    p.start()
    time.sleep(3)
    return {'process': p, 'prefix': motor_ioc_prefix}


@pytest.fixture(scope="module")
def camotor_prefix(camotor_ioc):
    return camotor_ioc['prefix']


class FieldHistory:
    '''
    Encapsulates what is essentially a chronological, time-stamped
    list of field dictionaries belonging to a motor movement.
    '''
    def __init__(self):
        self._track = []
        self._tmp_frame = {}

        # Starting point of the track, will be set on first `.append()`.
        self.t0 = None
        self._point_index = 0


    def append_field(self, field, value):
        f = self._tmp_frame
        t = time.time()
        if self.t0 is None:
            self.t0 = t
        f["t"] = t-self.t0
        f["i"] = self._point_index
        self._point_index += 1
        f[field] = value
        if len(self._track) == 0:
            print(f'Recording started @ {t}')
        self._track.append(f.copy())


    def first_point(self, name, value=None, values=None, vrange=None, vtest=None):
        return self._find_point(self._track, name, value, values, vrange, vtest)

    
    def last_point(self, name, value=None, values=None, vrange=None, vtest=None):
        return self._find_point(self._track[::-1], name, value, values, vrange, vtest)
    
        
    def _find_point(self, _track, name, value=None, values=None, vrange=None, vtest=None):
        '''
        This is for internal use, see `.first_point()` or `.last_point()`
        for actual API use.
        
        Finds the first occurence of field `name` in `_track`, which
        has value `value`, or any value within `values`, or any values
        within range `vrange` or if `vtest(value)==True`.

        Returns (field_dict) of the first matching instance.
        '''

    
        for i,f in enumerate(_track):
            try:
                fv = f[name]
            except KeyError:
                continue

            if (value is not None) and (fv == value):
                return f

            if (values is not None) and (fv in values):
                return f

            if (vrange is not None) and ((fv >= vrange[0] and fv <= vrange[1])):
                return f

            if (vtest is not None) and vtest(fv):
                return f

        raise RuntimeError(f'Not found: {name} that passes fv=={value}, '
                           f'or fv in {values}, or fv between {vrange}')


    def succession_points(self, name):
        '''
        Goes through the fields and returns the succession list of the values
        of `name` -- i.e. a chronological list of all the changes within the
        corresponding value.

        Returns a list of the corresponding point objects (i.e. field dictionaries).
        '''
        prev = None
        succession = []
        for i,f in enumerate(self._track):
            try:
                fvalue = f[name]
            except KeyError:
                continue
    
            if prev is None or fvalue != prev:
                succession.append(f)
                prev = fvalue

        return succession

    
    def succession(self, name):
        # Same as succession_points(), but returns only a list of the
        # elements, not of the point objects
        s = self.succession_points(name)
        return [p[name] for p in s]


    @property
    def points(self):
        # The "official" way to access the track list
        return self._track

    
    def __len__(self):
        return len(self._track)

    @property
    def duration(self):
        # Returns duration of the track
        return self._track[-1]["t"]

    @property
    def field_names(self):
        return [i for i in self._track[-1].keys()]


    
class FieldClient:
    ## Quick'n dirty client to interact with an epics motor.
    ## Designed mostly to capture field changes (by subscription),
    ## but also has some functionality for writing/setting values.
    
    def __init__(self, prefix):

        # Shorter handlers for the PVs, respectively the subscripton objects.
        # We want these to be available by short names/suffixes (e.g. "RBV" or "VAL")
        # for easier handling
        self._sub = {}
        self._pvs = {}

        self._prefix = prefix

        self._field_names = {
            # Basic motor
            ".VAL",
            ".RBV",
            ".MSTA",
            ".DMOV",
            ".MOVN",
            ".STOP",

            # EDA motor engine fileds
            ".state",
            ".clear",
            ".error",

            # VELO mixin
            ".VELO",
        }
        
        self.history = FieldHistory()
        self._fields = None
        self._refcnt = 0


    async def __aenter__(self, *args):
        if self._refcnt == 0:
            await self.init()
        self._refcnt += 1


    async def __aexit__(self, *args):
        if self._refcnt == 0:
            return
        self._refcnt -= 1
        if self._refcnt == 0:
            await self.shutdown()
        

    async def init(self, prefix=None):
        if prefix is not None:
            self._prefix = prefix

        print(f'New Fields connection in loop: {id(asyncio.get_event_loop())}')
        self._ctx = ClientContext()
        pvs = await self._ctx.get_pvs(*[f'{self._prefix}{f}' \
                                        for f in self._field_names])
        for pv in pvs:
            await pv.wait_for_connection()
        print(f'All connected')
        
        self._fields = {n:pv for n,pv in zip(self._field_names,pvs)}

        for name,pv in self._fields.items():
            # name mangling to remove all but the last component
            short_name = self._make_short_name(name)
            self._sub[short_name] = pv.subscribe()
            self._sub[short_name].add_callback(self._data_callback)
            self._pvs[short_name] = pv

        print(f'Short fields: {self._pvs.keys()}')        
            

    async def shutdown(self):
        print(f'Cleaning up Fields connection in loop: '
              f'{id(asyncio.get_event_loop())}')
        await self._ctx.disconnect()


    def _make_short_name(self, long_name):
        t1 = long_name.split('.')
        t2 = long_name.split('_')
        return t1[-1] if (len(t1) > 1) else t2[-1]        

    
    async def wait_for_value(self, field, value=None, span=None,
                             timeout=3.0, delay_after=1.0,
                             invert=False):
        # Direct-readout waiting for a specific field to hit a specific value
        t0 = time.time()
        while (time.time()-t0) < timeout:
            r = await self._pvs[field].read()
            if (r.status.severity == CASeverity.SUCCESS):
                data = r.data[0] #if r.data_type != ChannelType.STRING else r.data
                value_matches = (value is not None) and (data == value)
                span_matches = (span is not None) and (data >= span[0]) and (data<=span[1])
                if invert:
                    value_matches = not value_matches
                    span_matches = not span_matches
                if value_matches or span_matches:
                    if delay_after is not None:
                        await asyncio.sleep(delay_after)
                    return
                else:
                    #print(f'{field}={data}')
                    pass
            await asyncio.sleep(0.1)
        raise TimeoutError(f'Field {field} timed out waiting for value '
                           f'(want: value={value}, span={span})')


    async def write(self, field, value, delay_after=1.0):
        print(f'Field: {field} <- {value}')
        r = await self._pvs[field].write(value)
        if delay_after is not None:
            await asyncio.sleep(delay_after)
        return r


    def _data_callback(self, sub, res):
        pv = sub.pv
        name = self._make_short_name(sub.pv.name)
        data = res.data[0]
        #print(f'Result: {name} -> {data}')
        self.history.append_field(name, data)


class MoveTestBase:
    ## Base functionlaity for movement motor engine tests
    
    @pytest.fixture(scope="class")
    def target_value(self):
        # return a movement target value between -5 and +5
        return ((random.random()* - 0.5) * 10)


    @pytest.fixture(scope="class")
    async def field_client(self, camotor_prefix):
        #async with FieldClient(camotor_prefix) as client:
        #    yield client
        client = FieldClient(camotor_prefix)
        await client.init()
        print(f'Waiting for IDLE motor...')
        try:
            await client.wait_for_value('state', value=MotorState.IDLE, timeout=10.0)
            print(f'Motor ready')            
        except TimeoutError as e:
            print(f'Timeout waiting for IDLE motor: {e}')
            print(f'The test will fail.')
        yield client
        await client.shutdown()


    def test_state_succession(self, history, valid_succession):
        suc = history.succession('state')
        print(f'Received state succession: {suc}')
        print(f'Expected state succession: {valid_succession}')
        slen = len(valid_succession)
        if len(suc) == slen:
            assert suc == valid_succession
        elif len(suc) == slen-1:
            assert suc == valid_succession[1:]
        else:
            print(f'History:')
            for p in history.points:
                print(p)
            raise RuntimeError(f'Wrong number of motor states traversed '
                               f'(got {len(suc)}, succession {suc}), '
                               f'expected {slen-1} or {slen})')


@pytest.mark.motor_nofail
class TestGoodMove(MoveTestBase):
    ## Checks that a regular move works
    
    @pytest.fixture(scope="class")
    def valid_succession(self):
        return [
            MotorState.IDLE,
            MotorState.BUSY,
            MotorState.STOP,
            MotorState.IDLE
        ]

    @pytest.fixture(scope="class")
    async def history(self, field_client, target_value):
        print(f'Moving to: {target_value}')
        await field_client.write('VAL', target_value)
        await field_client.wait_for_value('MOVN', value=0, timeout=10.0)
        return field_client.history


    def test_show_session(self, history):
        print(f'Move session: {len(history)} items in {history.duration} seconds')
        #pprint.pprint(track.points)
        
    def test_movn_when_rbv(self, history):
        # Tests that MOVN flag is set when RBV is moving
        
        # The first RBV occurence
        rbvi = history.first_point('RBV',  vtest=lambda x: True)

        # "Official" beginning of movement
        movn = history.first_point('MOVN', value=1)

        # the first point where RBV actually is reported as changing
        rbvj = history.first_point('RBV',  vtest=lambda x: x != rbvi['RBV'])
        
        tdiff = movn["t"]-rbvj["t"]
        
        print(f'MOVN @ {movn["t"]}, moving @ {movn["t"]}')

        # Requre that the MOVN and RBV are changed within 0.1 seconds
        # of one another (...we can slightly increase this if it turns
        # out to be too optimistic; the whole move should always take
        # 3 seconds.)
        assert abs(tdiff) < (0.1+MotorPvClass._loop_slow_down_period)
        
    
    def test_target(self, history, target_value):
        t = history.points[-1]['RBV']
        print(f'At {t}, should be {target_value}')
        assert abs(t-target_value) < 1e-2


@pytest.mark.motor_nofail
class TestStopMove(MoveTestBase):
    ## Tests that stopping motor works
    
    @pytest.fixture(scope="class")
    def valid_succession(self):
        return [
            MotorState.IDLE,
            MotorState.BUSY,
            MotorState.STOP,
            MotorState.IDLE
        ]

    @pytest.fixture(scope="class")
    async def history(self, field_client, target_value):
        print(f'Moving to: {target_value}')
        await field_client.write('VAL', target_value)
        await asyncio.sleep(1.0)
        here = field_client.history.points[-1]["RBV"]
        print(f'Stopping while at: {here}')
        await field_client.write('STOP', 1)
        await field_client.wait_for_value('MOVN', value=0, timeout=10.0)
        return field_client.history

    def test_target(self, history, target_value):
        t = history.points[-1]['RBV']
        print(f'At {t}, should be {target_value}')
        assert t != target_value


@pytest.mark.motor_nofail
class TestErrorMove(MoveTestBase):
    ## Tests that stopping motor works
    
    @pytest.fixture(scope="class")
    def valid_succession(self):
        return [
            MotorState.IDLE,
            MotorState.BUSY,
            MotorState.STOP,
            MotorState.ERROR,
            MotorState.IDLE
        ]

    @pytest.fixture(scope="class")
    async def history(self, field_client):
        print(f'Moving to errnous value (666.0)')
        await field_client.write('VAL', 666.0)

        print(f'Waiting for ERROR state ({MotorState.ERROR})...')
        await field_client.wait_for_value('state', value=MotorState.ERROR,
                                          timeout=3.0)
        state = field_client.history.points[-1]['state']
        print(f'State: {state}, sending clear')

        assert state == MotorState.ERROR
        await field_client.write('clear', 1)
        await field_client.wait_for_value('state', value=MotorState.IDLE, timeout=3.0)

        # Check that the "clear" marker has been reset after use.
        await field_client.wait_for_value('clear', value=0, timeout=3.0)

        return field_client.history

    def test_target(self, history, target_value):
        t = history.points[-1]['RBV']
        print(f'At {t}, should be {target_value}')
        assert t != target_value


@pytest.mark.motor_fail
class TestFailMove(MoveTestBase):
    ## Tests that stopping motor works after FAIL -- note that
    ## the IOC is dead after this :-)
    
    @pytest.fixture(scope="class")
    def valid_succession(self):
        return [
            MotorState.IDLE,
            MotorState.BUSY,
            MotorState.FAIL
        ]

    @pytest.fixture(scope="class")
    async def history(self, field_client):
        print(f'Moving to errnous value (667.0)')
        await field_client.write('VAL', 667.0)

        print(f'Waiting for FAIL state...')
        await field_client.wait_for_value('state', value=MotorState.FAIL, timeout=3.0)
        state = field_client.history.points[-1]['state']
        print(f'State: {state}, sending clear')

        assert state == MotorState.FAIL

        # There's no escaping from FAIL -- check that we stay there even after clear
        await field_client.write('clear', 1)
        with pytest.raises(Exception):
            await field_client.wait_for_value('state', value=MotorState.IDLE, timeout=3.0)

        return field_client.history

    def test_target(self, history, target_value):
        t = history.points[-1]['RBV']
        print(f'At {t}, should be {target_value}')
        assert t != target_value
    
@pytest.mark.motor_nofail
class TestVeloMove(MoveTestBase):
    ## Tests that stopping motor works
    
    @pytest.fixture(scope="class")
    def valid_succession(self):
        return [
            MotorState.IDLE,
            MotorState.BUSY,
            MotorState.STOP,
            MotorState.ERROR, # we use the ERROR state for in-band messaging
            MotorState.IDLE
        ]

    @pytest.fixture(scope="class")
    async def history(self, field_client, target_value):
        print(f'Moving to: {target_value}')
        await field_client.write('VAL', target_value)
        await asyncio.sleep(1.0)

        velo = 3.14
        
        assert field_client.history.points[-1]['VELO'] == 0.0
        await field_client.write('VELO', velo)
        
        await field_client.wait_for_value('state', value=MotorState.ERROR, timeout=10.0)
        assert field_client.history.points[-1]['error'] == b'VELO-set'

        await field_client.write('clear', 1)
        await field_client.wait_for_value('state', value=MotorState.IDLE, timeout=10.0)

        await asyncio.sleep(1.0)

        # Check if the velocity was set properly. Note that the mock-up
        # test velocity mixin will always set the velicity to 6.28.
        assert field_client.history.points[-1]['VELO'] == 6.28
        
        return field_client.history        
