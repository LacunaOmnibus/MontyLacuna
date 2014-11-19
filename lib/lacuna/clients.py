
import json, logging, os, os.path, pprint, re, requests, threading, time, uuid
import configparser
import beaker.cache, beaker.util
from my_validate_email import validate_email

import lacuna.alliance
import lacuna.bc
import lacuna.body
import lacuna.captcha
import lacuna.empire
import lacuna.exceptions
import lacuna.inbox
import lacuna.map
import lacuna.stats

class Guest(lacuna.bc.SubClass):
    """ Guest users are not logged in.

    Accepts the following named arguments:
        - config_file --  path to your configparser-friendly config file
        - config_section -- the section in your config file to read from
        - api_key -- your TLE api_key.  Omitting this is fine; the default key (the string 'anonymous') will be used.
        - logfile -- path to your logfile.  Defaults to no logfile; only WARNING or higher log events will display to the terminal.
        - proto -- http or https.  Defaults to http.
        - host -- us1.lacunaexpanse.com or pt.lacunaexpanse.com.  Defaults to us1.
        - sleep_on_call -- Integer seconds.  Defaults to 1.  Number of seconds to sleep after each call to attempt to avoid using more than the limit of 60 RPCs per minute.
        - sleep_on_error -- Boolean.  Defaults to True.  If we've used over 60 RPCs in a minute, the server will produce an error, and if this setting is True, when we get that server error we'll sleep for a minute and then re-try our call.  If this setting is false, we'll throw an exception.

    Generally, you'll omit all arguments except for config_file and 
    config_section, and just fill the appropriate values out in your config.

    If a config_file and config_section are passed in, the values in that config 
    file take precedence over any other values, including passed-in values.

    **Caching**
    None of the MontyLacuna modules are performing any caching for you.  
    However, if your script performs some selective caching, it could well run 
    (much) faster, so there is a 'cache' attribute you can use in your 
    scripts.

    The 'cache' attribute is a beaker CacheManager object, with a file-based 
    cache already set up for you.

    **Debugging**
        To take a look at the actual JSON that would be sent to the TLE 
        servers for a specific method call, in your calling code you can set a 
        debugging method on your client, eg:

            >>> 
            empire.client.debugging_method = 'view_profile'
            empire.view_profile()

        In this case, the call to view_profile() will cause the JSON that 
        would normally be sent to the server to instead be dumped to your 
        screen, after which the script will quit.
    """

    pp = pprint.PrettyPrinter( indent = 4 )

    config_list = [
        'host', 'proto',
        'username', 'password', 'api_key',
        'sleep_on_call', 'sleep_after_error', 'session_id',
        'warn_on_sleep', 'show_captcha', 'logfile'
    ]

    def __init__( self,
            api_key:str             = 'anonymous',
            config_file:str         = '', 
            config_section:str      = '',
            host:str                = 'us1.lacunaexpanse.com',
            logfile:str             = '',
            password:str            = '', 
            proto:str               = 'http', 
            session_id:str          = '', 
            show_captcha:bool       = True,
            sleep_after_error:bool  = True, 
            sleep_on_call:int       = 1, 
            username:str            = '', 
            warn_on_sleep:bool      = True, 
        ):

        if config_file and config_section and os.path.isfile(config_file):
            self.config_file    = config_file
            self.config_section = config_section
            self.config         = self.read_config_file( config_file )
            for i in self.config_list:
                if i in self.config[config_section]:
                    setattr( self, i, self.config[config_section][i] )
        elif config_file and not os.path.isfile(config_file):
            raise EnvironmentError("Config file "+config_file+": no such file or directory.")
        else:
            for i in self.config_list:
                setattr( self, i, eval(i) )

        self._create_user_logger()

        self._create_request_logger()
        emp_name = self._determine_empname()
        log_opts = {
            'empire': emp_name,
            'path': 'empty',
            'method': 'empty',
        }
        self.request_logger.info('Creating a new client',extra=log_opts)

        self._set_up_cache()

    def _set_up_cache(self):
        libdir      = os.path.abspath(os.path.dirname(__file__))
        vardir      = libdir + "/../../var"
        cachedir    = vardir + "/cache"
        lockdir     = vardir + "/cachelck"
        if os.path.isdir(vardir):
            if not os.path.isdir(cachedir):
                os.mkdir(cachedir)
            if not os.path.isdir(lockdir):
                os.mkdir(lockdir)
        else:
            raise EnvironmentError("You're missing var/ off your installation directory.  Fix your install.")
        cache_opts = {
            'cache.type':       'file',
            'cache.data_dir':   cachedir,
            'cache.lock_dir':   lockdir,
            'expire':           3600
        }
        self.cache = beaker.cache.CacheManager(**beaker.util.parse_cache_config_options(cache_opts))

    def _create_user_logger(self):
        log_format  = '[%(asctime)s] (USER) (%(levelname)s) - %(message)s'
        date_format = '%Y-%m-%d %H:%M:%S'

        l = logging.getLogger( str(uuid.uuid1()) )
        l.setLevel(logging.DEBUG)

        sh = logging.StreamHandler()
        sh.setLevel(logging.WARNING)
        sh.setFormatter(logging.Formatter(log_format, date_format))
        l.addHandler(sh)

        if( hasattr(self, 'logfile') and self.logfile ):
            fh = logging.FileHandler( os.path.normpath(self.logfile) )
            fh.setLevel(logging.DEBUG)
            fh.setFormatter(logging.Formatter(log_format, date_format))
            l.addHandler(fh)

        self.user_logger = l

    def _create_request_logger(self):
        """
        Don't use logging.getLogger() to get at the logger.  Instead, use the 
        client.request_logger attribute.
        """
        ### logging.getLogger( 'logger_name' ) returns a singleton, but we're 
        ### calling this logger creator once for each client.  There will 
        ### definitely be scripts with multiple clients.
        ###
        ### Originally, the 'logger_name' being used here was static 
        ### ("tle_request").  What was happening was that the second client 
        ### created was producing 2 log entries per call to log.LEVEL(msg), 
        ### and the third client created was producing 3 log entries, etc.  
        ###
        ### So each client needs to have his own distinctly-named logger.  And 
        ### since doing this every time I want a logger is tedious and 
        ### fraught:
        ###    emp_name = self._determine_empname()
        ###    l = logging.getLogger( emp_name + '_tle_request' )
        ### ...we're adding the logger as a client attribute instead.
        ### 
        ### Since getLogger() is right out, the logger's name doesn't have to 
        ### be anything recognizable, just unique per client, so we're just 
        ### using a uuid as the logger name.

        ### screen
        s_format = '(REQ) %(levelname)s -- %(empire)s - %(path)s::%(method)s - %(message)s'

        ### file
        f_format = '[%(asctime)s] (REQ) (%(levelname)s) - %(empire)s - %(path)s::%(method)s - %(message)s'

        ### date (used by f_format)
        d_format = '%Y-%m-%d %H:%M:%S'

        l = logging.getLogger( str(uuid.uuid1()) )
        l.setLevel(logging.DEBUG)

        sh = logging.StreamHandler()
        sh.setLevel(logging.WARNING)
        sh.setFormatter(logging.Formatter(s_format, d_format))
        l.addHandler(sh)

        if( hasattr(self, 'logfile') and self.logfile ):
            fh = logging.FileHandler( os.path.normpath(self.logfile) )
            fh.setLevel(logging.DEBUG)
            fh.setFormatter(logging.Formatter(f_format, d_format))
            l.addHandler(fh)

        self.request_logger = l

    def read_config_file( self, conf, default = 'DEFAULT' ):
        cp = configparser.ConfigParser( interpolation=configparser.ExtendedInterpolation() )
        cp.read( conf )
        for section in cp:
            if section == default:
                continue
            for i in self.config_list:
                if i not in cp[section] and i in cp[default]:
                    cp[section][i] = cp[default][i]
        return cp

    def write_default_config_file( self, path ):
        cp = configparser.ConfigParser()
        cp['DEFAULT'] = {
            'host': 'us1.lacunaexpanse.com',
            'proto': 'http',
            'api_key': 'anonymous',
            'sleep_on_call': 1,
            'sleep_after_error': 1,
            'warn_on_sleep': 1,
            'show_captcha': 1,
            'logfile': 'var/tle.log',
        }
        with open(path, 'w') as handle:
            cp.write(handle)

    def _build_url(self):
        """ Returns a base URL composed of the proto (http or https) and the 
        host.  The returned URL does NOT end with a slash.
        """
        url = self.proto + "://" +  self.host
        return url

    def get_stats(self):
        return lacuna.stats.Stats( self )

    def is_name_available(self, name):
        try:
            rslt = self.send( 'empire', 'is_name_available', (name,) )
        except lacuna.exceptions.ServerError as e:
            if e.code == 1000 and e.text == 'Empire name is in use by another player.':
                return False
            else:
                ### An actual server error - game server is 
                ### down/overloaded/whatever.
                print("Server is borked: ", e)
                exit()
        return True

    def looks_like_json( self, json_candidate:str ):
        return True if re.match("^{.*}$", json_candidate) else False

    def _determine_empname(self):
        """ Used for logging.  A guest empire name will be returned as 
        "UNKNOWN".
        """
        empname = 'UNKNOWN'
        if hasattr(self, 'username') and self.username:
            empname = self.username
        return empname

    def send_password_reset_message(self, email='', **kwargs):
        """ This is meant to send a password reset email to the user's 
        registered email address.  However, it seems that the TLE server is not 
        sending any emails at all, via this method or the browser.
        """ 
        if 'empire_id' not in kwargs and 'empire_name' not in kwargs:
            raise AttributeError("Either empire_name or empire_id must be sent.")

        if 'empire_id' in kwargs and not kwargs['empire_id'].isdigit():
            raise TypeError("empire_id must be an integer.")

        if not validate_email( email ):
            raise TypeError(email, "is not a valid email address.")

        try:
            rslt = self.send( 'empire', 'send_password_reset_message', (kwargs) )
        except lacuna.exceptions.ServerError as e:
            raise lacuna.exceptions.NoSuchEmpireError("Cannot recover password; no such empire exists.")

        if rslt['sent']:
            print( "The server says it sent a message, but sending mail seems to be broken server-side, so you may get nothing." )
        else:
            raise RuntimeError( "The server says it has not sent the message, but gives no indication as to why not." )

    def send( self,  path:str="", method:str="", params:tuple=(), depth:int=1 ):
        """ Marshals a request and actually sends it to the server, collecting 
        and json-decoding the response.

        Accepts:
            - path -- The path after the host (eg empire, building, etc).  Don't include any directory separators.
            - method -- The name of the method to be run
            - params -- Tuple of arguments/parameters to be passed to the method.

        Returns:
            A dictionary; the json-decoded response from the server.

        Raises:
            - NotJsonError if the server response is not a JSON string
            - ServerError if the server responds with anything other than 
              a 200, along with a JSON string
        """

        url = self._build_url()
        if path:
            url = '/'.join( (url, path) )

        request = {
            "jsonrpc": "2.0",
            "id": 1,
            "method": method,
            "params": params,
        }
        request_json = json.dumps( request )
        if hasattr(self, 'debugging_method') and self.debugging_method == method:
            print( request_json )
            quit()

        emp_name = self._determine_empname()
        log_opts = {
            'empire': emp_name,
            'path': path,
            'method': method,
        }
        emp_name = self._determine_empname()
        l = self.request_logger

        def get_req():
            self._from_cache = False
            resp = requests.post( url, request_json )
            return resp

        resp = ''
        self._from_cache = False
        if self._cache_on:
            cache = self.cache.get_cache(self._cache_name, type='file', expire=self._cache_exp)
            cache_key = method + repr(params)
            self._from_cache = True
            resp = cache.get( key = cache_key, createfunc = get_req )
        else:
            resp = requests.post( url, request_json )

        ### The json parser will happily return a result when handed a raw 
        ### string instead of json (json.dumps("foobar") works just fine).  
        ### The module is documented to do this.
        ### 
        ### ...so an HTML page containing "server error" will not cause 
        ### json.loads() to produce a ValueError; it'll just be treated as a 
        ### big-ass string.
        ### 
        ### An error page like that should not have a JSON content-type, so 
        ### just checking that _should_ be enough.  But in the spirit of CYA, 
        ### I still want to confirm that the supposedly JSON string I'm 
        ### receiving when the content type indicates JSON, is actually JSON.  
        ### Hence the looks_like_json() check.
        if resp.headers['content-type'] != 'application/json-rpc' or not \
            self.looks_like_json(resp.text):
                self.request_logger.error('Response is not JSON', extra=log_opts)
                raise lacuna.exceptions.NotJsonError( "Response from server is not json: " + resp.text )

        if resp.status_code != 200:
            json_error = json.loads( resp.text )
            error = lacuna.exceptions.ServerError( json_error['error']['code'], json_error['error']['message'] )

            if depth > 3:
                self.request_logger.error('Likely recursion detected', extra=log_opts)
                raise RuntimeError("Likely infinite recursion detected; bailing!")
            depth += 1

            if error.code == 1010 and re.match('Slow down', error.text) and self.sleep_after_error:
                self.request_logger.warning("60 RPC per minute limit exceeded.", extra=log_opts)
                if self.warn_on_sleep:
                    self.request_logger.info("Sleeping for one minute.", extra=log_opts)
                time.sleep( 61 )
                thingy = self.send( path, method, params, depth )
            elif error.code == 1006 and error.text == 'Session expired.':
                ### Probably the user's config file had a session_id recorded, 
                ### but it's grown old.  Delete the old session_id, re-login, 
                ### and fix the params we're passing (session_id is the first 
                ### param).  Then re-send.
                self.request_logger.info('Stale session_id found; re-logging in.', extra=log_opts)
                if hasattr(self, 'session_id'):
                    delattr(self, 'session_id')
                self.login()
                fixed_params = (self.session_id, params[1:])
                thingy = self.send( path, method, fixed_params, depth )
            elif error.code == 1016 and error.text == 'Needs to solve a captcha.' and self.show_captcha:
                self.request_logger.info("Displaying required captcha.", extra=log_opts)
                cap = self.get_captcha()
                cap.showit()
                cap.prompt_user()
                cap.solveit()
                thingy = self.send( path, method, params, depth )
            else:
                self.request_logger.error("("+str(error.code)+") "+error.text, extra=log_opts)
                raise error
        else:
            cache_text = " (data from cache)" if self._from_cache else ""
            self.request_logger.info('Success'+cache_text, extra=log_opts)
            thingy = json.loads( resp.text )

        if self.sleep_on_call and not self._from_cache:
            time.sleep( float(self.sleep_on_call) )
        
        ### thingy contains:
        ###     {
        ###         "id": "1",
        ###         "jsonrpc": "2.0",
        ###         "result": { dict that we're actually interested in }
        ###     }
        ### We're only returning 'result', but sometimes we're recursing into 
        ### ourself (captcha, 60 RPC/min limit) - in those cases, thingy will 
        ### already be just 'result'.
        if 'result' in thingy:
            return thingy['result']
        else:
            return thingy

################################################################

class Member(Guest):
    """ Members are logged in; username and password are required.  

    Attributes:
        >>> 
        config_file
        config_section
        host
        logfile
        proto
        username
        password
        sleep_on_call
        sleep_after_error
        show_captcha
        warn_on_sleep
    """

    ### These attributes can not be passed in as constructor arguments:
    ### _cache_exp      Integer seconds for cache entry expiration
    ### _cache_name     Name of the cache namespace.  Not an individual cache
    ###                 entry key.
    ### _cache_on       Boolean.  If true, JSON responses are cached, using
    ###                 the joined parameters as the cache entry key.
    ### _from_cache     Boolean.  Hard set to False on each call to send(),
    ###                 it's then set to True if caching is on AND if we 
    ###                 actually pulled our data from the cache.  In that 
    ###                 case, we won't perform our standard per-call sleep.

    def __init__( self,
            config_file:str         = '',
            config_section:str      = '',
            api_key:str             = '',
            host:str                = '',
            logfile:str             = '',
            proto:str               = '',
            username:str            = '',
            password:str            = '',
            sleep_on_call:int       = 1,
            sleep_after_error:bool  = True,
            show_captcha:bool       = True,
            warn_on_sleep:bool      = True
        ):

        super().__init__(
            config_file = config_file,
            config_section = config_section,
            host = host, 
            logfile = logfile, 
            proto = proto,
            username = username,
            password = password,
            sleep_on_call = sleep_on_call,
            sleep_after_error = sleep_after_error,
            show_captcha = show_captcha,
            warn_on_sleep = warn_on_sleep,
        )

        if not self.username or not self.password:
            raise AttributeError("username and password are required.")

        self._cache_on = False
        self.login()

    def cache_on(self, name:str, expiry:int=3600):
        """ Turn the cache on.

        Arguments:
            - name -- String namespace to use for caching data
            - expiry -- Integer seconds after which cached data is no longer valid.  Defaults to 3600 (one hour).
        """
        self._cache_exp = expiry
        self._cache_name = name
        self._cache_on = True

    def cache_off(self):
        """ Turn caching off.
        Does not clear any existing caches, only stops pulling data from them.
        """
        self._cache_on = False

    def cache_clear(self, name:str = ''):
        """ Clears a named cache.  If a cache name is not mentioned, clears the most-recently used cache.

        Arguments:
            - name -- String; name of the cache to clear.  Defaults to the cache most recently used.

        ::

            client.cache_on('cache_one' )
            client.cache_on('cache_two' )

            client.cache_clear()                # clear cache_two implicitly
            client.cache_clear( 'cache_one' )   # clear cache_one explicitly

        Returns True if a cache was cleared, false if no name was passed in and 
        no cache has yet been used by this client (so there's no 
        "most-recently-used" cache name to clear).
        """
        if not name:
            if self._cache_name:
                name = self._cache_name
            else:
                return False
        cache = self.cache.get_cache(name)
        cache.clear()
        return True

    def get_alliance(self):
        return lacuna.alliance.Alliance( self )

    def get_body(self, body_id):
        return lacuna.body.Body( self, body_id )

    def get_body_byname(self, body_name):
        for bid, name in self.empire.planets.items():
            if name == body_name:
                return lacuna.body.MyBody( self, bid )
        else:
            raise lacuna.exceptions.NoSuchMyBodyError("No body with the name '{}' was found.".format(body_name))

    def get_captcha(self):
        return lacuna.captcha.Captcha( self )

    def get_inbox(self):
        return lacuna.inbox.Inbox( self )

    def get_map(self):
        return lacuna.map.Map( self )

    def get_my_alliance(self):
        return lacuna.alliance.MyAlliance( self )

    def login(self):
        """ Ensures the current client is logged in.

        If self.session_id is set, we'll test it to make sure we can get a 
        response.  If so, the session_id is valid and we'll continue to use 
        that session.

        If self.session_id is not set or is found to be invalid, we'll log in 
        fresh.  The new, now-valid session_id will be written to the config 
        file.
        """
        if hasattr(self,'session_id'):
            try:
                rslt = self.send( 'empire', 'get_status', (self.session_id,) )
                self.empire = lacuna.empire.MyEmpire( self )
                mydict = lacuna.bc.LacunaObject.get_status_dict(self, rslt)
                self._write_empire_status(mydict)
                return
            except lacuna.exceptions.ServerError as e:
                pass

        try:
            rslt = self.send( 'empire', 'login', (self.username, self.password, self.api_key) )
        except lacuna.exceptions.ServerError as e:
            raise lacuna.exceptions.BadCredentialsError("Incorrect credentials (bad username/password)")
        self.session_id = rslt['session_id']
        self.empire = lacuna.empire.MyEmpire( self )
        mydict = lacuna.bc.LacunaObject.get_status_dict(self, rslt)
        self._write_empire_status(mydict)

        if hasattr( self, 'config' ):
            self.config[self.config_section]['session_id'] = self.session_id
            self.update_config_file()

    def _write_empire_status(self, mydict:dict):
        """ This is almost, but not quite the same, as 
        lacuna.bc.LacunaObject.write_empire_status().
        """
        for i in mydict:
            setattr( self.empire, i, mydict[i] )
        self.empire.planet_names = {name: id for id, name in self.empire.planets.items()}

    def update_config_file(self):
        if not hasattr(self, 'config'):
            return False
        with open(self.config_file, 'w') as handle:
            self.config.write(handle)

    def logout( self ):
        """ Logs the current session out.

        Saving the session_id in the config file allows users to complete a 
        captcha in one script and have that captcha's success apply to all 
        other scripts run, as long as that session_id is valid.

        Calling logout() invalidates that session_id and removes it from the 
        config file.  Therefore, actually calling logout() is rarely 
        necessary.
        """
        rslt = {}
        if hasattr(self, 'empire'):
            rslt = self.empire.logout()
            delattr( self, 'empire' )
        if hasattr(self, 'session_id'):
            delattr( self, 'session_id' )
        if hasattr( self, 'config' ) and hasattr( self, 'config_section'):
            if 'session_id' in self.config[self.config_section]:
                del( self.config[self.config_section]['session_id'] )
                self.update_config_file()
        return rslt

