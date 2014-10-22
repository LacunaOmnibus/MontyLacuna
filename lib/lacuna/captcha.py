
import os, requests, tempfile, time, webbrowser
from lacuna.bc import LacunaObject
from lacuna.exceptions import \
    CaptchaResponseError, \
    RequestError, \
    ServerError


""" Displays a captcha image and attempts to discover if the user's response 
to that captcha was accurate.

        cap = Captcha( <client object> )
    ...or, more often...
        cap = client.get_captcha()

    cap.showit()        # Displays the captcha image in a browser
    cap.prompt_user()   # Asks the user to answer the captcha

    if cap.solveit():
        print( "The user's response was correct" )
    else:
        print( "The user's response was NOT correct" )

"""

### Dev notes:
### The tempfile containing the captcha image is not deleted until solveit() 
### has been called.  
### 
### Allowing the tempfile to delete itself (delete=True during tempfile 
### creation), or using the tempfile in conjunction with a 'with:' expression, 
### have both been attempted.
### 
### The problem is that, when using those auto-deletion methods, the tempfile 
### is occasionally being removed from the system before the browser we're 
### firing off actually gets a chance to read it.  Everything is happening in 
### the right order, it's just that the browser startup is too slow.
###
### Deleting the tempfile manually in solveit() works - don't decide to get 
### clever and replace the unlink() in solveit() with some form of tempfile 
### autodeletion without a lot of testing.

class Captcha(LacunaObject):
    path = 'captcha'

    @LacunaObject.call_member_meth
    def fetch( self, **kwargs ):
        """ Fetches a captcha for the user to solve from the server.

        Generally, you don't need to call this, use showit() instead.

        This mirrors the TLE Captcha::fetch() method.  It fetches the url and 
        guid for the captcha, but does not actually fetch the captcha image 
        (which lives at url) itself.

        Retval includes:
            'guid' - a hashed CHECK captcha ID,
            'url' - The URL to the image
        """
        self.url  = kwargs['rslt']['url']
        self.guid = kwargs['rslt']['guid']
        pass

    def showit( self ):
        """ Actually downloads the captcha image, and attempts to display it  
        to the user in one of several browsers.

        If fetch() is called first, showit() uses that fetched data, but this 
        is not necessary.  showit() will call fetch for you.
        """
        if not hasattr(self,'url') or not hasattr(self,'guid'):
            self.fetch()

        img_resp = requests.get( self.url )
        if img_resp.status_code != 200:
            raise RequestError("The captcha image URL is not responding.")

        f = tempfile.NamedTemporaryFile( suffix='.png', prefix='tle_capcha_', delete=False );
        self.tempfile = f.name
        f.write( img_resp.content )

        local_url = 'file://' + f.name
        found_browser = False
        for b in [ None, 'windows-default', 'macosx', 'safari', 'firefox', 
            'google-chrome', 'chrome', 'chromium-browser', 'chromium' ]:
            try:
                browser = webbrowser.get( b )
                browser.open( local_url, 0, True )
                found_browser = True
                break
            except webbrowser.Error as e:
                pass
        if not found_browser:
            raise EnvironmentError("Unable to find a browser to show the captcha image.  Captcha solution is required.")

    def prompt_user(self):
        """ Prompts the user to solve the displayed captcha.
        It's not illegal to call this without first calling solveit(), but 
        doing so makes no sense.
        """
        self.resp = input("Enter the solution to the captcha here: ")
        return self.resp

    def solveit(self):
        """ Sends the user's response to the server to check for accuracy.
        Returns True if the user's response was correct.  Raises 
        CaptchaResponseError otherwise.
        """
        if not hasattr(self,'resp'):
            raise AttributeError("You must prompt the user for a response before calling solveit().")
        try:
            self.solve( self.guid, self.resp )
        except ServerError as e:
            raise CaptchaResponseError("Incorrect captcha response")
        finally:
            delattr( self, 'url' )
            delattr( self, 'guid' )
            delattr( self, 'resp' )
            if os.path.isfile(self.tempfile):
                os.unlink( self.tempfile )
        return True

    @LacunaObject.call_member_meth
    def solve( self, guid:str, solution:str, **kwargs ):
        """ Mirrors the TLE Captcha::solve() method, but unless you really 
        need this and you really know why, use solveit() instead.
        """
        pass

