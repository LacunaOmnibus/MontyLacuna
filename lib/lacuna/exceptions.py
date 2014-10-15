
class BadCredentialsError(Exception):
    """One or both of username and/or password is bad.  We're not sure which."""
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return repr(self.value)

class BadConfigSectionError(Exception):
    """User specified a config file section which does not exist."""
    def __init__(self, section):
        self.section = section
    def __str__(self):
        return repr(self.section)

class GDIError(Exception):
    """The client attempted to access own alliance methods, but is not currently
    in an alliance.
    """
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return repr(self.value)

class NotJsonError(Exception):
    """The server responded, but handed back something other than JSON"""
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return repr(self.value)

class NoSuchEmpireError(Exception):
    """The empire name used does not exist"""
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return repr(self.value)

class ServerError(Exception):
    """The TLE server returned a 500 and a JSON error string"""
    def __init__(self, code:int, message:str):
        self.code       = code
        self.message    = message
        self.text       = message
    def __str__(self):
        return repr("Server error " + str(self.code) + ": " + self.message)

