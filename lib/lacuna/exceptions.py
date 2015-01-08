
class BadCredentialsError(Exception):
    """ One or both of username and/or password is bad.  We're not sure which."""
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return repr(self.value)

class BadConfigSectionError(Exception):
    """ User specified a config file section which does not exist."""
    def __init__(self, section):
        self.section = section
    def __str__(self):
        return repr(self.section)

class BadBuildingError(Exception):
    """ The building requested exists but isn't usable (probably damaged)"""
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return repr(self.value)

class CaptchaResponseError(Exception):
    """ The user's response to a captcha puzzle was incorrect."""
    def __init__(self, section):
        self.section = section
    def __str__(self):
        return repr(self.section)

class GDIError(Exception):
    """ The client attempted to access own alliance methods, but is not currently
    in an alliance.
    """
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return repr(self.value)

class NoAvailableShipsError(Exception):
    """ We attempted to do something that requires one or more ships (eg fetch 
    spies), but no ships were available.
    """
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return repr(self.value)

class NotJsonError(Exception):
    """ The server responded, but handed back something other than JSON"""
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return repr(self.value)

class NoUsableSpiesError(Exception):
    """ No spies onsite satisfy the requirements. """
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return repr(self.value)

class NoSuchMyBodyError(Exception):
    """ The body requested does not exist in my empire."""
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return repr(self.value)

class NoSuchBuildingError(Exception):
    """ The building requested does not exist"""
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return repr(self.value)

class NoSuchEmpireError(Exception):
    """ The empire name used does not exist"""
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return repr(self.value)

class RequestError(Exception):
    """ A network request is not responding properly.  Generally this means that 
    response.status_code is other than 200.
    """
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return repr(self.value)

class ServerError(Exception):
    """ The TLE server returned a 500 and a JSON error string
    """
    def __init__(self, code:int, message:str):
        self.code       = code
        self.message    = message
        self.text       = message
    def __str__(self):
        return repr("Server error " + str(self.code) + ": " + self.message)

class TopoffError(Exception):
    """ A script got a --topoff argument, but we're already over the requested number.
    """
    def __init__(self, number:int, message:str):
        self.number     = number
        self.message    = message
        self.text       = message
    def __str__(self):
        return repr("Topoff error - we're already above" + str(self.number) + ": " + self.message)


