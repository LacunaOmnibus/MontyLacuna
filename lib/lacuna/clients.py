
import json, logging, logging.handlers, os, os.path, pprint, re, requests, sys, threading, time, uuid
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

    Args:
        api_key (str): Your TLE api_key.  Defaults to 'anonymous'.
        config_file (str):  Path to your config file.
        config_section (str): The section in your config file to read from.
        host (str): ``us1.lacunaexpanse.com`` or ``pt.lacunaexpanse.com``.  
            Defaults to 'us1'.
        logfile (str): Path to your logfile.  Defaults to no logfile.
        show_captcha (bool):  If set to false, and a 
            method call needs a captcha solved, an exception 
            will be raised.  If left true, the user will automatically be 
            prompted to solve a captcha when needed.  Defaults to True.  
        sleep_on_call (int): Number of seconds to sleep after each call to 
            attempt to avoid using more than the limit of 60 RPCs per minute.  
            Defaults to 1.  
        sleep_after_error (bool):  If we've used over 
            60 RPCs in a minute, the server will produce an error, and if this 
            setting is True, when we get that server error we'll sleep for a 
            minute and then re-try our call.  If this setting is false, we'll 
            throw an exception.  Defaults to True.  
        sleep_on_call (int): Seconds to sleep after each TLE 
            server request.  Defaults to 1.
        warn_on_sleep (bool): If you exceed 60 RPCs 
            per minute, and the script is therefore going to pause for a minute, 
            and this is set to True, a warning will be displayed to let you know 
            why your script is taking so long.  Defaults to True.  

    Generally, you'll omit all arguments except for config_file and 
    config_section, and just fill the appropriate values out in your config 
    file.

    If a config_file and config_section are passed in, the values in that config 
    file take precedence over any other values, including passed-in values.
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

        ### As long as this file, 'clients.py', is in ROOT/lib/lacuna/, the 
        ### following is correct.  We _do_ want __file__ here, not 
        ### sys.argv[0].
        self.root_dir   = os.path.abspath(os.path.dirname(__file__)) + '/../..'

        if config_file and config_section and os.path.isfile(config_file):
            self.config_file    = config_file
            self.config_section = config_section
            self.config         = self._read_config_file( config_file )
            ### Allow arbitrary attributes to be set from the config file; 
            ### these are going to be used by test scripts.
            for i in self.config[config_section]:
                setattr( self, i, self.config[config_section][i] )
        elif config_file and not os.path.isfile(config_file):
            raise EnvironmentError("Config file "+config_file+": no such file or directory.")
        else:
            for i in self.config_list:
                setattr( self, i, eval(i) )

        self.max_log_size = 1024*500    # 500k seems reasonable
        self.num_log_backups = 3
        self._create_module_logger()
        self._create_request_logger()
        self._create_user_logger()

        emp_name = self._determine_empname()
        log_opts = { 'empire': emp_name, 'path': 'empty', 'method': 'empty' }
        self.request_logger.info('Creating a new client',extra=log_opts)

        self._set_up_cache()

    def _set_up_cache(self):
        vardir      = self.root_dir + "/var"
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

    def _create_module_logger(self):
        """
        Usable by any modules that want to create log entries.  These should be 
        kept down to a dull roar; mostly warnings.
        """
        log_format  = '[%(asctime)s] (MODULE) (%(levelname)s) - %(message)s'
        date_format = '%Y-%m-%d %H:%M:%S'

        l = logging.getLogger( str(uuid.uuid1()) )
        l.setLevel(logging.DEBUG)

        sh = logging.StreamHandler()
        sh.setLevel(logging.WARNING)
        sh.setFormatter(logging.Formatter(log_format, date_format))
        l.addHandler(sh)

        lf_path = self.root_dir + "/var/module.log"
        lf = logging.handlers.RotatingFileHandler( lf_path, maxBytes=self.max_log_size, backupCount=self.num_log_backups )
        lf.setLevel(logging.DEBUG)
        lf.setFormatter(logging.Formatter(log_format, date_format))
        l.addHandler(lf)
        self.module_logger = l

    def _create_user_logger(self):
        """
        Documented as being accessible to the user.  Creates entries in the same 
        format as the module logger, except these are tagged as (USER) instead 
        of (MODULE), and the handlers here get set up as client attributes, so 
        the user can change their loglevels.
        """
        log_format  = '[%(asctime)s] (USER) (%(levelname)s) - %(message)s'
        date_format = '%Y-%m-%d %H:%M:%S'

        l = logging.getLogger( str(uuid.uuid1()) )
        l.setLevel(logging.DEBUG)

        ### Hrm I'm not seeing a way to get the handlers back out of the log 
        ### object after creation.  So the handlers themselves are becoming 
        ### client attributes, so we can change the log levels later if 
        ### needed.

        self.user_log_stream_handler = logging.StreamHandler()
        self.user_log_stream_handler.setLevel(logging.WARNING)
        self.user_log_stream_handler.setFormatter(logging.Formatter(log_format, date_format))
        l.addHandler(self.user_log_stream_handler)

        lf_path = None
        if self.username:
            lf_path = self.root_dir + "/var/" + self.strsquish(self.username) + ".log"
        else:
            lf_path = self.root_dir + "/var/guest.log"
        self.user_log_file_handler = logging.handlers.RotatingFileHandler( lf_path, maxBytes=self.max_log_size, backupCount=self.num_log_backups )
        self.user_log_file_handler.setLevel(logging.DEBUG)
        self.user_log_file_handler.setFormatter(logging.Formatter(log_format, date_format))
        l.addHandler(self.user_log_file_handler)
        self.user_logger = l

    def _create_request_logger(self):
        """
        Request logger entries require that you send a dict of args:
            (message, extra=some_dict)

        That some_dict has to include the keys 'empire', 'path', and 'method'.  

        The request logger should *only* be used by self.send() -- anything else 
        that wants to write to the logfile should use the module logger.
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

        self.request_log_stream_handler = logging.StreamHandler()
        self.request_log_stream_handler.setLevel(logging.WARNING)
        self.request_log_stream_handler.setFormatter(logging.Formatter(s_format, d_format))
        l.addHandler(self.request_log_stream_handler)
        
        lf = None
        if( hasattr(self, 'logfile') and self.logfile ):
            lf = self.root_dir + "/var/" + self.logfile 
        else:
            lf = self.root_dir + "/var/request.log"
        
        lf = None
        if( hasattr(self, 'logfile') and self.logfile ):
            lf = self.root_dir + "/var/" + self.logfile 
        else:
            lf = self.root_dir + "/var/request.log"

        fh = logging.handlers.RotatingFileHandler( lf, maxBytes=self.max_log_size, backupCount=self.num_log_backups )
        fh.setLevel(logging.DEBUG)
        fh.setFormatter(logging.Formatter(f_format, d_format))
        l.addHandler(fh)

        self.request_logger = l

    def _read_config_file( self, conf, default = 'DEFAULT' ):
        ### passwords sometimes contain $ characters, which confuse 
        ### ExtendedInterpolation.  BasicInterpolation uses % characters for 
        ### the same thing Extended uses $, so Basic is probably going to have 
        ### the same issues.  The interpolated sections of the config were 
        ### kinda neato, but would probably end up creating more confusion 
        ### than benefit in the end anyway, so they're going away completely.
        cp = configparser.ConfigParser( interpolation=None )
        cp.read( conf )
        for section in cp:
            if section == default:
                continue
            for i in self.config_list:
                if i not in cp[section] and i in cp[default]:
                    cp[section][i] = cp[default][i]
        return cp

    def write_default_config_file( self, path ):
        """ Writes initial data to a file to be used as a MontyLacuna config file.

        This method does no safety checking of any kind, and will clobber the 
        contents of any file passed to it.  So check to make sure you're not 
        overwriting some existing file before calling this.

        Args:
            path (str): Path to the file to write
        """
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
        """ Get a :class:`lacuna.Stats` object """
        return lacuna.stats.Stats( self )

    def is_name_available(self, name):
        """ Check if a given string is available to be registered as a new 
        empire name.

        Args:
            name (str): Name to check for availablility.
        Returns:
            bool: True if the string can be used as a new empire name, False
                otherwise.
        """
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

    def _looks_like_json( self, json_candidate:str ):
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

        This should not be something you ever need to call yourself.

        Args:
            path (str): The path after the host (eg empire, building, etc).  Don't include any directory separators.
            method (str): The name of the method to be run
            params (tuple of str): arguments/parameters to be passed to the method.
        Returns:
            dict: the json-decoded response from the server.
        Raises:
            lacauna.exceptions.NotJsonError: if the server response is not a JSON string
            lacauna.exceptions.ServerError: if the server responds with anything other than 
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

        ### The requests module leaves its sockets open in a pool.  This is 
        ### normally fine, but it generates ResourceWarnings when warnings are 
        ### on.  This includes during unit tests.  The simplest solution is 
        ### just to close the connection when we're finished with it.
        ### But with a regular run, at least sometimes, that resp object 
        ### doesn't have a connection attribute.  Probably because it came 
        ### from the cache.
        if hasattr(resp, 'connection'):
            resp.connection.close()

        emp_name = self._determine_empname()
        log_opts = { 'empire': emp_name, 'path': path, 'method': method, }

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
        ### Hence the _looks_like_json() check.
        if resp.headers['content-type'] != 'application/json-rpc' or not \
            self._looks_like_json(resp.text):
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
                    self.request_logger.warning("Sleeping for one minute.", extra=log_opts)
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

    def strsquish(self, string:str):
        """ Squish a string, removing all non-word characters.

        Args:
            string (str): The string to squish
        Returns
            str: the squished string.

        >>> new = self.strsquish( "foo bar & baz" )
        >>> print( new )    # foobarbaz
        """
        pat = re.compile("\W")
        return re.sub( pat, '', string )

################################################################

class Member(Guest):
    """ Members are logged in; username and password are required.  

    Object Attributes::

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

        Args:
            name (str): namespace to use for caching data
            expiry (int): seconds after which cached data is no longer 
                valid.  Defaults to 3600 (one hour).
        Returns:
            str: namespace that had previously been set.  Empty 
              string if no cache had previously been on.
        """
        self._cache_exp = expiry
        old_name = ''
        if hasattr(self, '_cache_name'):
            old_name = self._cache_name
        self._cache_name = name
        self._cache_on = True
        return old_name

    def cache_off(self):
        """ Turn caching off.
        Does not clear any existing caches, only stops pulling data from them.
        Returns the name of the cache that had been in use, or False if none.
        """
        self._cache_on = False
        return self._cache_name if hasattr(self, '_cache_name') else False

    def cache_clear(self, name:str = ''):
        """ Clears a named cache.  If a cache name is not passed, clears the most-recently used cache.

        Args:
            name (str): name of the cache to clear.  Defaults to the 
                cache most recently used.
        Returns:
            bool: True if a cache was cleared, false if no name was passed in and 
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
        """ Get an :class:`lacuna.alliance` object.
        """
        return lacuna.alliance.Alliance( self )

    def get_body(self, body_id):
        """ Get a :class:`lacuna.body` object by body ID.

        Args:
            body_id (int): ID of the body
        Returns
            lacuna.body.Body: The requested body object
        """
        attrs = { 'id': body_id, }
        return lacuna.body.Body( self, attrs )

    def get_body_byname(self, body_name):
        """ Get one of your empire's bodies (planet or station) by name.

        Arguments:
            body_name (str): name of the body

        Returns:
            lacuna.body.MyBody: The requested body
        """
        for bid, name in self.empire.planets.items():
            if name == body_name:
                attrs = {
                    'id': bid,
                    'name': name
                }
                return lacuna.body.MyBody( self, attrs )
        else:
            raise lacuna.exceptions.NoSuchMyBodyError("No body with the name '{}' was found.".format(body_name))

    def get_captcha(self):
        """ Get a :class:`lacuna.captcha.Captcha` object.
        """
        return lacuna.captcha.Captcha( self )

    def get_inbox(self):
        """ Get an :class:`lacuna.inbox.Inbox` object.
        """
        return lacuna.inbox.Inbox( self )

    def get_map(self):
        """ Get a :class:`lacuna.map.Map` object.
        """
        return lacuna.map.Map( self )

    def get_my_alliance(self):
        """ Get your alliance.

        Returns:
            lacuna.alliance.MyAlliance: Your alliance (or False if you're not 
                in an alliance.)
        """
        my_ally = False
        try:
            my_ally = lacuna.alliance.MyAlliance( self )
        except lacuna.exceptions.GDIError as e:
            return my_ally
        return my_ally

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
            self._update_config_file()

    def _write_empire_status(self, mydict:dict):
        """ This is almost, but not quite the same, as 
        :meth:`lacuna.bc.LacunaObject.write_empire_status`.
        """
        for i in mydict:
            setattr( self.empire, i, mydict[i] )
        self.empire.planet_names = {name: id for id, name in self.empire.planets.items()}
        self.empire.colony_names = {name: id for id, name in self.empire.colonies.items()}
        self.empire.station_names = {name: id for id, name in self.empire.stations.items()}

    def _update_config_file(self):
        if not hasattr(self, 'config'):
            return False

        with open(self.config_file, 'w') as handle:
            self.config.write(handle)

    def logout( self ):
        """ Logs the current session out.

        Normally, there's no need to call this.  However, after a client 
        connects (and logs in), their session ID will be written to the config 
        file to save them having to log in again the next time.  Saving this 
        session ID also records whether the client has recently solved a 
        captcha.

        If you're testing something out and want to see any captcha prompts, 
        you'll want to call logout() at the end of your test script.  This 
        way, running your test script multiple times will result in actual 
        captcha prompts each time.
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
                self._update_config_file()
        return rslt

