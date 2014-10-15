
import json, pprint, re, requests, time
from validate_email import validate_email

import lacuna.alliance
import lacuna.empire
import lacuna.inbox
import lacuna.map
import lacuna.stats
from lacuna.exceptions import \
    BadCredentialsError, \
    NoSuchEmpireError, \
    ServerError

defaults = {
    'api_key': 'anonymous',
    'host': 'us1.lacunaexpanse.com',
    'proto': 'http',
}

pp = pprint.PrettyPrinter( indent = 4 )

class Client:
    """Client users are not logged in.

    Accepts:
        proto - http or https.  Default http.
        host - us1.lacunaexpanse.com or pt.lacunaexpanse.com.  Default us1.
        sleep_on_call - Integer seconds.  Default 1. 
            Number of seconds to sleep after each call to attempt to avoid 
            using more than the limit of 60 RPCs per minute.  
        sleep_on_error - Boolean.  Default True.
            If we've used over 60 RPCs in a minute, the server will produce 
            an error.  If sleep_on_error is True, we'll sleep for a minute 
            and then re-try our call.  If false, we'll throw an exception.
    """
    def __init__( self,
            host = defaults['host'],
            proto = defaults['proto'],
            sleep_on_call = 1,
            sleep_after_error = True
        ):
        self.host               = host if host else 'foo'
        self.proto              = proto if proto else 'foo'
        self.sleep_on_call      = sleep_on_call
        self.sleep_after_error  = sleep_after_error

    def build_url(self):
        """Returns a base URL composed of the protocol (http or https) and the host.
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
                The path after the hostname (eg empire, building, etc).  Don't 
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
        resp = requests.post( url, data = request_json )

        ### The imported json dumper will happily return a result when handed 
        ### a raw string instead of json (json.dumps( "foobar" ) works just 
        ### fine).  The module is documented to do this.
        ### 
        ### ...so an HTML page containing "server error" will not cause 
        ### json.loads() to produce a ValueError; it'll just be treated as a 
        ### big-ass string.
        ### 
        ### Theoretically, an error like that should not have a JSON 
        ### content-type.  In theory, practice and theory are identical; in 
        ### practice, they're not.  So I want to confirm that the 
        ### theoretically JSON string I've received is actually JSON.

        if resp.headers['content-type'] != 'application/json-rpc' or not \
            self.looks_like_json(resp.text):
                raise NotJsonError( "Response from server is not json: " + resp.text )

        if resp.status_code != 200:
            json_error = json.loads( resp.text )
            error = ServerError( json_error['error']['code'], json_error['error']['message'] )
            if error.code == 1010 and re('Slow down', error.text) and self.sleep_after_error:
                self.depth += 1
                if self.depth > 3:
                    raise RuntimeError("Likely infinite recursion detected on "+method+"; bailing!")
                time.sleep( 61 )
                thingy = self.send( path, method, params, self.depth )
            else:
                raise error
        else:
            thingy = json.loads( resp.text )

        if self.sleep_on_call:
            time.sleep( self.sleep_on_call )

        ### thingy contains:
        ###     {
        ###         "id": "1",
        ###         "jsonrpc": "2.0",
        ###         "result": { dict that we're actually interested in }
        ###     }
        return thingy['result']

################################################################

class Member(Client):
    """Members are logged in; username and password are required.  Member 
    inherits from Client.
    """
    def __init__( self,
            api_key=defaults['api_key'],
            host=defaults['host'],
            proto=defaults['proto'],
            username='',
            password=''
        ):

        super().__init__(host, proto)

        if not username or not password:
            raise AttributeError("username and password are required.")

        ### The 'else' is required here, but since host and proto already have 
        ### defaults, they'll never not be set at this point.
        self.api_key    = host if api_key else 'foo'
        self.username   = username
        self.password   = password
        self.session_id = False

        ### Gotta login before doing anything else.
        self.login()

        try:
            self.empire = lacuna.empire.MyEmpire( self )
        except ServerError as e:
            print("Member creation is unable to fetch empire:", e)
            exit()

        ### Initialize our empire object
        self.empire.get_status()

    def get_alliance(self):
        return lacuna.alliance.Alliance( self )

    def get_inbox(self):
        return lacuna.inbox.Inbox( self )

    def get_map(self):
        return lacuna.map.Map( self )

    def get_my_alliance(self):
        return lacuna.alliance.MyAlliance( self )

    ### get_stats() is in Client, as it requires no login.

    def login(self):
        try:
            rslt = self.send( 'empire', 'login', (self.username, self.password, self.api_key) )
        except ServerError as e:
            raise BadCredentialsError("Incorrect credentials (bad username/password)")
        self.session_id = rslt['session_id']

    def logout( self ):
        """The Empire class actually contains the logout method, which invalidates the current
        session_id.  Call that method, then delete our empire and session_id attributes."""
        rslt = self.empire.logout()
        delattr( self, 'empire' )
        delattr( self, 'session_id' )
        return rslt

