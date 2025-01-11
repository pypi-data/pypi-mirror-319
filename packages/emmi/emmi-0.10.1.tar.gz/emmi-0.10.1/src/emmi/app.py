#!/usr/bin/python3

import asyncio, time, logging
import logging
logger = logging.getLogger(__name__)

from os import environ

from emmi.api.exports import ExportObjectFromDict

from softioc import softioc, builder, asyncio_dispatcher

'''
Base modules for easier development of EPICS
'''

def loadFromYaml(path):
    from yaml import load, dump
    try:
        from yaml import CLoader as Loader, CDumper as Dumper
    except ImportError:
        from yaml import Loader, Dumper
        
    if (path is not None) and len(path) > 0:
        return load(open(path, 'r').read(), Loader=Loader)

    return {}


def cfgFromFlat(flatCfg, prefix='', splitChar='_'):
    '''
    Returns a (possibly nested) configuration dictionary from a flat
    list of key-value pairs `flatCfg`. The initial list can for instance
    be a list of environment variables.

    Only entries where the key matches a specific prefix are considered.
    `prefix`, however, may be an empty string, which leads to accepting
    the list as given.
    
    Splits variable names at `splitChar` and adds a new dictionary
    level for each split.
    '''

    if not isinstance(prefix, str):
        return {}

    env = {}

    for k,v in flatCfg.items():
        if not k.startswith(prefix):
            continue
        
        parts = k.split(splitChar)

        current_dict = env
        for p in parts[:-1]:
            current_dict = current_dict.setdefault(p, {})
        current_dict[parts[-1]] = v
        
    if len(prefix):
        return env.get(prefix, {})
    else:
        return env


def cfgUnify(*cfgs, mangle_case=True):
    '''
    Returns a unified configuration object by consecutively applying
    dictionary values from `cfgs`. The individual configuration
    dictionaries in `cfgs` can be recursive.

    If `mangle_case` is enabled (default), then a special handling
    of key string case is perfomed, as follows.

    Quite generally, the preferred format of key names is
    all-lower-case ("likethis") or camel-case ("likeThis"), without
    dashes or underscores, and the typical usage case for this function
    is to put together configuration information from different sources,
    e.g. config files (e.g. YAML hierarchies) and environment variables.
    It is acknowledged that some configuration sources (e.g. environment
    variables) have their typical case customs (e.g. ALL_UPPER_CASE_IN_ENV_VARS).

    For this reason, when encountering all-caps keys, corresponding
    existing keys are searched in previous configuration dictionaries.
    If those are found, then the new ALL-CAPS key is interpreted to
    update one of the existing variables. For instance an environment
    variable `APPLICATIONNAME` will overwrite a previous config setting
    `applicationName`.

    If no case-sensitive keys with the same name exist, then new keys are
    created from scratch. But if the newly to-be-created key is all-caps,
    then instead of using it verbatim, it is converted to lower-case (!),
    to keep the style of lower-case variable names consistend.

    Note that while this gives well-defined results, it may not behave as
    expected if configuration keys use camel-case and are expected; for
    instance, "FOOBAR" would be translated to "foobar" if "fooBar"
    doesn't already exist.
    
    Defining camel-case variables in environment variables works, though:
    "$fooBar=application" would be translated to a configuration variable
    "fooBar='application' regardless of where it is found.

    The configuration dictionaries in `cfgs` are applied subsequently,
    meaning the last one wins (i.e. overwrites previously existing values
    for the same key).
    '''

    #print ("Unify:", *cfgs)
    
    cfg = dict()
    for c in cfgs:
        if c is None:
            continue

        # Map of:  CAMELCASEKEY -> camelCaseKey  for the existing dict ('cfg')
        if mangle_case:
            keysCaseMap = { k.upper(): k for k in cfg.keys() }
            if len(keysCaseMap) != len(cfg):
                raise RuntimeError("Oops. You probably have several camel-case configKey items in your "
                                   "config settings that each map to the same all-caps CONFIGKEY. "
                                   "You can't to that.")
            
        for input_k,v in c.items():

            if mangle_case and input_k.isupper():
                # case-mangling: if we have an all-caps input key, we need
                # to find a corresponding cammel-case key to it.
                try:
                    k = keysCaseMap[input_k]
                except KeyError:
                    k = input_k.lower()
                    #print(f'{input_k} is a new one, using it as {k}')
            else:
                # no key-case-mangling
                k = input_k
                
            cfg[k] = v if not isinstance(v, dict) \
                else cfgUnify(cfg.get(k, None), v)
            
    return cfg


class IocApplication(object):
    '''
    Specialized application model for EPICS IOCs.
    
    While frameworks like `pythonSoftIOC` bring a lot of initialization
    code to the table, generally writing a robust application with useful
    features for production concerns itself with more detals, as for
    instance:
    
      - Configuration parameters -- EPICS prefix, timing and polling
        defaults etc.

      - Additional flow variables -- heartbeat and kill switch PVs

      - Keeping track of PV objects (e.g. as created by pythonSoftIOC's
        `builder.aIn/aOut` methods).

      - Ability to rapidly invoke features offered by `emmi.api.exports`,
        e.g. add PVs for the properties of a custom object, possibly based
        on an declarative configuration, e.g. as with
        `emmi.api.exports.ExportObjectFromDict`).

    In creating a "smooth application experience", all these different
    roles have subtle interactions, which are none the less quite generic,
    universal and repetitive for essentially any Python-based IOC.

    This object offers a convenient interface of juggling these requirements.
    
    One of the main premises of the application, beyond the obvious fact that
    it's an IOC, is that every configuration aspect may come from more several
    sources with differing priorites. For instance:
    
       - Default settings with lowest priorites inside the Python code itself

       - On-disk configuration files (e.g. in JSON or YAML format)

       - Environment variables with a specific naming scheme (e.g. prefixed
         by the name of the application), overriding any config file settings

       - Command line arguments, being used with highest priority and overriding
         even enviroment variable settings.

    For this, `IocApplication` holds an internal nested configuration dictionary,
    accessible in the `.conf` attribute. It is of course possible to update the
    dictionary directly. But also the helper functions `addFlatConfig()` and
    `addNestedConfig()` are intended to merge new values form a higher-priority
    dictionary, overriding existing settings where necessary.

    The `.conf` attribute is meant as well for internal use by `IocApplication`
    as for external use and reference by objects that aren't managed by a
    specific `IocApplication` instance.

    Here is a non-exhaustive list of `.conf` variables that `IocApplication`
    reacts to (using the hierarchical sytax for `option.suboption` to reflect
    to entries within the nested dicitonary `.conf["option"]["subobtion"]`):

      - `epics.prefix`: The EPICS PV prefix to use. Ultimately this is used
        by `setupIoc()`, but the latter may be triggered from `__init__()`.

      - `epics.heartbeat`: The interval at which the "::heartbeat" PV is
        updated (see `setupIoc()` for details)

      - `epics.killSwitch`: Whether or not to export a kill switch PV which
        has the ability to shut down the entire IOC remotely (note that there
        may be security implications with this).

      - `epics.defaults`: Default settings for various Connectors (from
        `emmi.api.exports`) that will be passed on from within the
        `exportObject()`  method. See `emmi.api.exports.ExportObjectFromDict()`
        for details, that's what `exportObject()` uses under the hood.

    Configuration settings that aren't used by `IocApplication` are entirely
    the IOC programmer's responsibility. We suggest, however, that one or more
    sub-sections are created within `.conf` to host such settings (e.g.
    `.conf["harp"]` as used by `miniquant-ioc`, an EMMI-based IOC for the
    HydraHarp 400 photon counter by PicoQuant; or `.conf["scpi"]', as used
    by `escpi` a generic SCPI-to-EPICS brige that is built using EMMI and
    `IocApplication`.)

    A minimal `IocApplication` which exports properties of `MyDeviceObject`
    might look like this:

    ```
    #!/usr/bin/python3
    
    from emmi.app import IocApplication
    from emmi.scpi import MagicScpi
    from os import environ
    from json import load as jsn_load

    # very simple example for an object containing a property/attribute
    # that we want to export access to via EPICS PVs in a python IOC
    class MyDeviceObject:
        theProperty = 3.14

    dev = MyDeviceObject()

    # This one might for example contain something like:
    #   { 'epics': { 'prefix': 'BAR' } }
    cfg = jsn_load(open("./simple-ioc.json"))

    # Initialize with default EPICS prefix of FOO.
    # Also suppress the initialisation of the IOC for now, because
    # we may want to load even more configuration options.
    app = IocApplication (prefix="FOO", setupIoc=False)

    # We want to use the settings from JSON file. These will override
    # existing settings with the same key; e.g. after this, the
    # EPICS prefix might actually be set on track for "BAR".
    app.addNestedConfig(cfg)

    # Add support for magic configuration by environment variables.
    # For instance, after this, the variable MYIOC_EPICS_PREFIX=MOO
    # will actually override the PV prefix defined at runtime from "FOO",
    # or "BAR" defined in the config file, to "MOO" defined in the env-var.
    app.addFlatConfig(os.environ, prefix='MYIOC')

    # Initialization of IOC. This will already create a 'FOO::heartbeat'
    # and 'FOO::killSwitch` PV.
    app.setupIoc(killSwitch=True)

    # Add our object-specific PVs -- in this case, for the
    # MyDeviceObject.theProperty attribute.
    app.exportObject(dev, settings={ 'recordType': 'property',
                                     'property': { 'name': 'theProperty',
                                                   'kind': 'analog' } })

    # Finally run the IOC. After this, the PVs are available on
    # the network to be used and abused with caget/caput.
    app.runIoc()
    ```

    This application is actually available verbatim form the `examples/`
    subdirectory of the main `emmi` sources tree -- you are encouraged
    to try this out!

    `IocApplication` works hand in hand with `emmi.api.exports` to make
    it easy to use a declarative interface for which properties/attributes
    to be exported as PVs.
    '''
    
    def __init__(self, prefix=None, cfg=None, setupIoc=False,
                 name=None, env=None, args=None):
        '''
        Initialize an IOC application based on pythonSoftIOC.
        
        Args:
        
            prefix: the variable / device prefix to use for the EPICS device
        
            cfg: a (possibly nested) configuartion dictionary. Currently, the
              following keys are used:
              - `epics.prefix`: the IOC variable / device prefix. If present, this
                overrides the `prefix` parameter from `__init__()`.
              An alternative way of configuring the application is by
              passing over `args` and `env` information.

            setupIoc: if set to `True`, this will automatically call the
              `setupIoc()` method with default parameters, which needs to be done
              before the IOC is ready to accept `exportObject()` and execute.
              However, generally you don't want to do that if you have multiple
              configuration sources (e.g. YAML files, environment variables etc)
              to be loaded in additio to `cfg`, and which may not yet be available
              at the point at which your `IocApplication` is being defined.

            args: Command line arguments for the application, typically from
              `sys.argv`. These are not processed right away, since an argument
              parser is needed for that. They are stored for later processing
              through `.configure()`.
              There are a number of command line arguments which, if present
              in the parser, have a very specific meaning for `IocApplication`.
              See the documentation of `.configure()` for a documentation.
        '''
        
        self.conf = cfg or dict({})

        self._args = args
        self._env = env if env is not None else {}
        self._name = name or 'emmi'
        #self._logger = logger

        self.otel_logger_provider = self.setup_otel_logger(logger)

        if prefix is not None:
            self._set_prefix(prefix)

        if setupIoc:
            self.setupIoc()


    def setup_otel_logger(self, logger):

        env = self._env
        service = env.get("EMMI_OTELCOL_SERVICE", self._name)
        otelcol_url = env.get("EMMI_OTELCOL_URL", "") # http://localhost:4317

        if (otelcol_url is None) or (len(otelcol_url)==0):
            return None
            
        from opentelemetry._logs import set_logger_provider
        from opentelemetry.exporter.otlp.proto.grpc._log_exporter \
            import OTLPLogExporter
        from opentelemetry.sdk._logs import LoggerProvider, LoggingHandler
        from opentelemetry.sdk._logs.export import BatchLogRecordProcessor
        from opentelemetry.sdk.resources import Resource

        otel_logger_provider = LoggerProvider(
            resource=Resource.create(
                {
                    "service.name": service,
                    "service.class": "epics-ioc",
                    "service.instance.id": os.uname().nodename,
                }
            ),
        )
        set_logger_provider(otel_logger_provider)
        otel_otlp_exporter = OTLPLogExporter(endpoint=otelcol_url,
                                             insecure=True)
        otel_logger_provider.add_log_record_processor(
            BatchLogRecordProcessor(otel_otlp_exporter)
        )

        #  console_exporter = ConsoleLogExporter()
        #  logger_provider.add_log_record_processor(BatchLogRecordProcessor(console_exporter))

        otel_handler = LoggingHandler(level=logging.NOTSET,
                                      logger_provider=otel_logger_provider)
        logger.addHandler(otel_handler)

        self.have_otel = True

        return otel_logger_provider


    def configure(self, parser,
                  args=None, args_prefix_map=None,
                  env=None, env_prefix_map=None, env_prefix=None):
        '''
        Reads configuration settings for the application.

        Configuration precedence is enforced through `cfgUnify()`
        and in the following order:

          - The least important setting is one read from a (possibly
            nested) config file, specified through a possible
            `--from-yaml` argument (see the "Args" section below).
        
          - Next in line are environment variables: variables of the
            form `{env_prefix}_{config_keys}={value}` override pre-existing
            keys `{config_keys}` (same caveats with underscore apply),
            or are freshly defined if they didn't exist previously.
        
          - The highest precedence is given to command line arguments,
            specified verbatim. The `cfg` object keys correspond to the
            line arguments, with every underscore opening a `cfg`
            subsection (e.g. `--epics-prefix` sets the
            `cfg["epics"]["prefix"]` key).
        

        Args:
            parser: a configured Python command line parser
        
            args: an arguments array (e.g. `sys.argv`)

            args_prefix_map: if this is not `None`, it acts as an additional
              filter on the command line arguments which we want to consider.
              The general format of a command line argument is
              `--{prefix}-{confkey}`, where `{confkey}` is the (possibly nested,
              by the use of the `-` character) configuration key. The keys in
              `args_prefix_map` are expected to describe the valid `{prefix}`
              values which are considered. Their value counterpart is the
              subtree within the config dictionary where to insert the values.
              Note that the subsection cannot be nested (i.e. it needs to be
              a direct subsection of the config tree). To disable config
              command line arguments either don't pass an `args` object,
              or pass an empty `dict()` here.

            env: environment variables list. If not specified, the one
              passed over to `.__init__()` will be used.

            env_prefix_map: this is used for filtering environment variables in
              a similar fashion to how `args_prefix_map` is used for filtering
              arguments, with one notable difference: if this is `None`,
              then environment variable configurations is disabled completely.
              This is because typically, there are more configuration variables
              that _don't_ concern us than there are those that do.
              So this _must_ contain at least one entry, or env-var config is
              disabled.

            env_prefix: convenience use that creates
              `env_prefix_map = { "...": None }` (i.e. an entry which uses
              the prefix "..." to insert data into the root of the config tree),
              if `env_prefix_map` is `None`.

        Returns: the command-line arguments namespace, for possible subsequent
        use.
        '''
        if args is None:
            args = self._args

        if env is None:
            env = self._env

        pargs = parser.parse_args()

        ## Note that some stuff here should be logged, but generally,
        ## at this point there's no logger available if we want to let
        ## OpenTelemetry handle the logging (because we initialize
        ## OpenTelemetry only after the config has been handled).

        # Least important: config file --from-yaml
        if hasattr(pargs, "from_yaml"):
            #print(f"config={pargs.from_yaml} type=file")
            ycfg = loadFromYaml(pargs.from_yaml)
            self.addNestedConfig(ycfg)

        # Next in line: env-vars with {env_prefix}
        if env_prefix_map is None and env_prefix is not None:
            env_prefix_map = { env_prefix: None }
        if env_prefix_map is not None:
            for k,v in env_prefix_map.items():
                print(f'config={k} type=env subsection={v}')
                self.addFlatConfig(env, prefix=k, subsection=v)

        # Highest priority: direct command line arguments
        if args_prefix_map is None:
            args_prefix_map = { "": None }
        for k,v in args_prefix_map.items():
            #print(f'config="{k}" type=args subsection="{v}"')
            filtered = {k:v for k,v in vars(pargs).items() if v is not None}
            self.addFlatConfig(filtered, prefix=k, subsection=v)

        if (self.otel_logger_provider is None):
            logging.basicConfig(level=self.conf.get('log', {}).get('level', "INFO"))

        return pargs
        

    @property
    def prefix(self):
        return self.conf['epics']['prefix']


    @property
    def epicsPrefix(self):
        logger.warning(f'epicsPrefix is deprecated, use .prefix instead')
        return self.conf['epics']['prefix']


    def _set_prefix(self, prefix):
        # pythonSoftIOC will add a ':' by its own. Meanwhile, we're trying
        # to use prefix _exactly_ as specified (for later compatibility with
        # caproto, for instance).
        if prefix[-1] == ':':
            self.conf.setdefault('epics', {}).setdefault('prefix', prefix)
        else:
            logger.warning(f'EPICS prefix doesn\t have trainling colon ({prefix})'
                           f' -- expecting EMMI to add it is deprecated and will be remove')
            self.conf.setdefault('epics', {}).setdefault('prefix', f'{prefix}:')


    def addNestedConfig(self, cfg):
        self.conf = cfgUnify(self.conf, cfg)


    def addFlatConfig(self, cfg, prefix='', separator='_', subsection=None):
        nested = cfgFromFlat(cfg, prefix, separator)
        self.addNestedConfig(nested if subsection is None else {subsection: nested})


    #def testModeRequested(self):
    #    '''
    #    Returns True if test mode was requested of the IocApplication.
    #    The application itself does not behave differently, but external
    #    modules (e.g. hardware initialisation) might.
    #
    #    NOTE: This should be obsolete pretty soon. It's not a good idea
    #    for code to differentiate its behavior depending on whether
    #    it's supposed to be in test mode or not.
    #    '''
    #    return self.conf['epics']['prefix'].endswith('TEST')
        

    def setupIoc(self, prefix=None, heartbeat=1.0, killSwitch=True):
        '''
        Initializes the IOC part of the application. If `prefix` is specified,
        it overrides whatever prefix was set in the configuration system.
        Note that only one PV is initialized here -- the obligatory 'heartbeat'
        PV that every EMMI IocApplication has and which just implements an
        ever-incrementing counter with a fixed frequency (default: 1 second).
        '''

        # If prefix is not 'None', override the cfg.epics.prefix.
        if prefix is not None:
            self._set_prefix(prefix)

        try:
            p = self.prefix
        except KeyError as e:
            logger.error(f'key="{str(e)}" desc="Did you configure the EPICS prefix?"')
            raise

        # Set some defaults if they're not specified in cfg.epics
        self.conf.setdefault('epics', {}).setdefault('heartbeat', heartbeat)
        self.conf.setdefault('epics', {}).setdefault('killSwitch', killSwitch)


        # We're storing the prefix CAproto style, as-is, including the
        # trailing ':'. But pythonSoftIOC expects it without, and will
        # add the trailing ':' by itself.
        if self.prefix[-1] != ':':
            logger.warning(f'Your prefix doesn\'t contain a trailing colon (:) '
                           f'-- that\'s good, but pythonSoftIOC will add one and there\'s nothing'
                           f' we can do about it for now.')
            pysoftioc_prefix = self.prefix
        else:
            pysoftioc_prefix = self.prefix[:-1:]
            
        logger.info(f'Using EPICS device prefix: "{pysoftioc_prefix}" (that\'s what we\'ll send to pysoftioc)')
        
        self.softioc = softioc
        self.iocBuilder = builder
        self.iocDispatch = asyncio_dispatcher.AsyncioDispatcher()
        self.iocBuilder.SetDeviceName(pysoftioc_prefix)

        # the device property part
        self.pv = {}

        if self.conf['epics']['heartbeat'] is not None:
            self.pv['heartbeat'] = self.iocBuilder.aIn('heartbeat', initial_value=0)

        if self.conf['epics']['killSwitch']:
            self.pv['killSwitch'] = self.iocBuilder.boolOut('killSwitch', initial_value=False,
                                                            on_update=self.die)


    def die(self, really=True):
        '''
        Turns off the runLoop variable if `really` is `True`. This is needed
        for the killSwitch option of the application (which, once activated,
        should be impossible to stop).
        '''
        if really:
            self.runLoop = False


    async def heartbeat(self):
        '''
        This is the "heartbeat" loop of the application.
        '''
        self.runLoop = True
        counter = 0
        while self.runLoop:
            self.pv['heartbeat'].set(counter)
            counter += 1
            await asyncio.sleep(self.conf['epics']['heartbeat'])
        self.running = False


    def startIoc(self, setup=False):
        '''
        Starts the IOC. In the pythonSoftIOC implementation, this just registers
        our own `heartbeat()` loop with the dispatcher and initialises the
        IOC (see `pythonSoftIOC.iocInit()`).
        '''
        if setup:
            self.setupIoc()
        self.iocBuilder.LoadDatabase()
        self.iocDispatch(self.heartbeat)

        logger.info(f'EMMI IOC appliction with EPICS prefix: "{self.prefix}" (EMMI internal representation)')
        self.softioc.iocInit(self.iocDispatch)
        self.running = True


    def stopIoc(self):
        '''
        Signalizes the heartbeat loop that it has to stop. This in turn will make
        the main loop of `runIoc()` stop.
        '''
        self.runLoop = False
    

    def runIoc(self, exit=True, setup=False):
        '''
        Calls startIoc() and waits for it to return (which may be never).
        If `exit` is set to `True` (the default), the pythonSoftIOC `exit()`
        method is called, which kills the application.
        '''
        
        self.startIoc(setup=setup)
        
        while self.running:
            time.sleep(0.1)

        if self.otel_logger_provider is not None:
            self.otel_logger_provider.shutdown()
        
        if exit:
            self.softioc.exit()


    def exportObject(self, device_obj, settings):
        '''
        Takes properties of object `device_object` and generates EPICS PVs
        according to the dicitonary `settings`. `settings` is a (usually YAML-generated)
        declarative format as defined in `emmi.api.exports`.
        This is actually just a wrapper for `emmi.api.exports.ExportObjectFromDict()`.
        '''
        defaults = self.conf.get('epics', {}).get('defaults', None)
        return ExportObjectFromDict(self.iocDispatch, device_obj, settings,
                                    recordTypeDefaults=defaults)
