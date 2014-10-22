
import json, os.path, pprint, re, requests, threading, time
import configparser
from configparser import ConfigParser, ExtendedInterpolation
from my_validate_email import validate_email

import lacuna.alliance
import lacuna.body
import lacuna.captcha
import lacuna.empire
import lacuna.inbox
import lacuna.map
import lacuna.stats
from lacuna.exceptions import \
    BadConfigSectionError, \
    BadCredentialsError, \
    NoSuchBodyError, \
    NoSuchEmpireError, \
    NotJsonError, \
    ServerError

class Guest:
    """ Guest users are not logged in.

    Accepts the following named arguments:
        config_file - path to your configparser-friendly config file
        config_section - the section in your config file to read from
        proto - http or https.  Default http.
        host - us1.lacunaexpanse.com or pt.lacunaexpanse.com.  Default us1.
        api_key - your TLE api_key.  Omitting this is fine; the default 
            key (the string 'anonymous') will be used.
        sleep_on_call - Integer seconds.  Default 1. 
            Number of seconds to sleep after each call to attempt to avoid 
            using more than the limit of 60 RPCs per minute.  
        sleep_on_error - Boolean.  Default True.
            If we've used over 60 RPCs in a minute, the server will produce 
            an error.  If sleep_on_error is True, we'll sleep for a minute 
            and then re-try our call.  If false, we'll throw an exception.

    Generally, you'll omit all arguments except for config_file and 
    config_section, and just fill the appropriate values out in your config.

    If a config file and section are passed in, the values in that config 
    file take precedence over any other values, including passed-in values.
    """

    pp = pprint.PrettyPrinter( indent = 4 )

    config_list = [
        'host', 'proto',
        'username', 'password', 'api_key',
        'sleep_on_call', 'sleep_after_error', 'session_id'
    ]

    def __init__( self,
            config_file = '', config_section = '',
            proto = 'http', host = 'us1.lacunaexpanse.com',
            username = '', password = '', api_key = 'anonymous',
            sleep_on_call = 1, sleep_after_error = True, session_id = ''
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
        
    def read_config_file( self, conf, default = 'DEFAULT' ):
        cp = ConfigParser( interpolation=ExtendedInterpolation() )
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
            'sleep_after_error': 1
        }
        with open(path, 'w') as handle:
            cp.write(handle)

    def build_url(self):
        """Returns a base URL composed of the proto (http or https) and the host.
        The returned URL does NOT end with a slash.
        """
        url = self.proto + "://" +  self.host
        return url

    def get_stats(self):
        return lacuna.stats.Stats( self )

    def is_name_available(self, name):
        try:
            rslt = self.send( 'empire', 'is_name_available', (name,) )
        except ServerError as e:
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

    def send_password_reset_message(self, email='', **kwargs):
        if 'empire_id' not in kwargs and 'empire_name' not in kwargs:
            raise AttributeError("Either empire_name or empire_id must be sent.")

        if 'empire_id' in kwargs and not kwargs['empire_id'].isdigit():
            raise TypeError("empire_id must be an integer.")

        if not validate_email( email ):
            raise TypeError(email, "is not a valid email address.")

        try:
            rslt = self.send( 'empire', 'send_password_reset_message', (kwargs) )
        except ServerError as e:
            raise NoSuchEmpireError("Cannot recover password; no such empire exists.")

        if rslt['sent']:
            print( "The server says it sent a message, but sending mail seems to be broken server-side, so you may get nothing." )
        else:
            raise RuntimeError( "The server says it has not sent the message, but gives no indication as to why not." )

    def send( self,  path="", method="", params=(), depth=1 ):
        """Marshals a request and actually sends it to the server, collecting and 
        json-decoding the response.

        Accepts:
            path (str)
                The path after the host (eg empire, building, etc).  Don't 
                include any directory separators.
            method (str)
                The name of the method to be run
            params (tuple)
                Tuple of arguments/parameters to be passed to the method.

        Returns:
            A dictionary; the json-decoded response from the server.

        Throws:
            - NotJsonError if the server response is not a JSON string
            - ServerError if the server responds with anything other than 
              a 200, along with a JSON string
        """

        url = self.build_url()
        if path:
            url = '/'.join( (url, path) )

        request = {
            "jsonrpc": "2.0",
            "id": 1,
            "method": method,
            "params": params,
        }
        request_json = json.dumps( request )
        #if method == 'get_status' or method == 'view':
        #    print( request_json )
        #    quit()
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
                raise NotJsonError( "Response from server is not json: " + resp.text )

        if resp.status_code != 200:
            json_error = json.loads( resp.text )
            error = ServerError( json_error['error']['code'], json_error['error']['message'] )

            if depth > 3:
                raise RuntimeError("Likely infinite recursion detected on "+method+"; bailing!")
            depth += 1

            if error.code == 1010 and re.match('Slow down', error.text) and self.sleep_after_error:
                time.sleep( 61 )
                thingy = self.send( path, method, params, depth )
            elif error.code == 1016 and error.text == 'Needs to solve a captcha.':
                cap = self.get_captcha()
                cap.showit()
                cap.prompt_user()
                cap.solveit()
                thingy = self.send( path, method, params, depth )
            else:
                raise error
        else:
            thingy = json.loads( resp.text )

        if self.sleep_on_call:
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
    """Members are logged in; username and password are required.  Member 
    inherits from Client.
    """
    def __init__( self,
            config_file         = '',
            config_section      = '',
            api_key             = '',
            host                = '',
            proto               = '',
            username            = '',
            password            = '',
            sleep_on_call       = 1,
            sleep_after_error   = True
        ):

        super().__init__(
            config_file = config_file,
            config_section = config_section,
            host = host, 
            proto = proto,
            username = username,
            password = password,
            sleep_on_call = sleep_on_call,
            sleep_after_error = sleep_after_error,
        )

        if not self.username or not self.password:
            raise AttributeError("username and password are required.")

        ### These are all server calls, and slow, but they must happen in 
        ### serial, because each depends upon the previous being complete.  So 
        ### don't try to thread them.
        self.login()
        self.empire = lacuna.empire.MyEmpire( self )
        self.empire.get_status()

    def get_alliance(self):
        return lacuna.alliance.Alliance( self )

    def get_body(self, body_id):
        return lacuna.body.Body( self, body_id )

    def get_body_byname(self, body_name):
        for bid, name in self.empire.planets.items():
            if name == body_name:
                return lacuna.body.Body( self, bid )
        else:
            raise NoSuchBodyError("No body with the name '{}' was found.".format(body_name))

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
                return
            except ServerError as e:
                pass

        try:
            rslt = self.send( 'empire', 'login', (self.username, self.password, self.api_key) )
        except ServerError as e:
            raise BadCredentialsError("Incorrect credentials (bad username/password)")
        self.session_id = rslt['session_id']
        if hasattr( self, 'config' ):
            self.config[self.config_section]['session_id'] = self.session_id
            self.update_config_file()

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
        rslt = self.empire.logout()
        delattr( self, 'empire' )
        delattr( self, 'session_id' )
        if hasattr( self, 'config' ) and hasattr( self, 'config_section'):
            if 'session_id' in self.config[self.config_section]:
                del( self.config[self.config_section]['session_id'] )
                self.update_config_file()
        return rslt

