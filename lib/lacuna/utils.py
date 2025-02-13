
import datetime, re, sys

class Utils():
    """
    Various useful utility methods that don't require a client.
    """

    def mytry( self, function, args:list = [] ):
        """ Calls a function or method.  If that function raises an exception, 
        this prints out the exception message ONLY, instead of printing the 
        entire trace, making it easier for the user to see what the problem 
        was.  

        This is only to be used in the case where you meant for execution to 
        halt in the case of an exception.  If you're planning on dealing with 
        an exception, re-throwing, whatever, you need to handle it yourself.  
        This method exists only to deal nicely with any caught exceptions, 
        which includes halting execution.

        Arguments:
            function (function): The function or method to call
            args (list): Any arguments that need to be passed to the function.

        Returns:
            retval (varies): whatever ``function`` would have returned.

        .. code-block:: python
            :linenos:
            :emphasize-lines: 3,5

            ute = lacuna.utils.Utils()

            retval = ute.mytry( somefunc, arg1, arg2, arg3 )
            ### Or...
            retval = ute.mytry( someobj.somemeth, arg1, arg2, arg3 )

        Warning:
            If the function you're attempting to call takes a list argument, 
            and you pass an empty list, the function will end up getting 
            called with no arguments at all.  This feels like an edge case 
            that won't be encountered often, but it's possible.
        """

        value   = None
        rv      = None
        try:
            if args:
                rv = function( args )
            else:
                rv = function()
        except:
            type, value, tb = sys.exc_info()
        finally:
            if value:
                print( "{}".format(value) )
                quit()
            else:
                return rv

    def squish( self, string:str, lc:bool = False ):
        """ Squish a string, optionally lowercasing it in the process.

        Arguments:
            string (str): The string to squish.
            lc_flag (bool): Whether or not to also lowercase the string.  Defaults to False.
        Returns:
            squished_string (str): The squished string.
        """
        pat = re.compile("\W")
        new = re.sub(pat, "", string)
        if lc:
            new = new.lower()
        return new


    def summarize( self, string:str, mymax:int ):
        """ Summarizes a string, usually for inclusion in a report section 
        with a fixed width.

        Arguments:
            string (str): String to summarize
            max (int): Max length of the string.  Must be greater than 3.

        If the string is ``abcdefghijk`` and the max is 6, this will return 
        ``abc...``

        Returns the summarized string, or the original string if it was shorter 
        than max.
        """
        mymax = 4 if mymax < 4 else mymax
        if len(string) > mymax:
            submax = mymax - 3
            string = string[0:submax] + "..."
        return string

    def tle2time(self, tle_time:str):
        """ Converts a TLE datetime string into a datetime object.

        Args:
            tle_datetime (str): eg ``30 11 2014 21:40:31 +0000``.
                The "+0000" is meant to be the timezone, but in TLE 
                datetime strings this is always "+0000" (UTC), so 
                this method is ignoring it, and it could actually 
                be omitted from the passed-in string.

        Returns:
            datetime.datetime: A `datetime.datetime <https://docs.python.org/3.4/library/datetime.html>`_ object
        """
        m = re.match("^(\d\d) (\d\d) (\d{4}) (\d\d):(\d\d):(\d\d)", tle_time)
        if m:
            return datetime.datetime(
                int(m.group(3)),    # year
                int(m.group(2)),    # month
                int(m.group(1)),    # day
                int(m.group(4)),    # hour
                int(m.group(5)),    # minute
                int(m.group(6)),    # second
            )
        else:
            raise AttributeError( "{} isn't a TLE datetime string.".format(tle_time) )


