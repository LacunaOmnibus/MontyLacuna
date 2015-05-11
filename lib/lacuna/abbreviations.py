
import os, pickle, sys

class Abbreviations():

    ### Assumes that the script calling us lives in INSTALL/bin/
    bindir = os.path.abspath(os.path.dirname(sys.argv[0]))
    vardir = os.path.abspath(bindir + "/../var")

    mydict = { 
        'abbrv': {}, 
        'name': {}
    }

    def __init__(self, client):
        self.client     = client
        self.statefile  = None
        self._set_statefile()
        self._read_statefile()

    def _get_data( self ):
        fh = open( self.statefile, "rb" )
        self.mydict = pickle.load(fh)

    def _put_data( self, mydict:dict ):
        """ Puts data in mydict into the statefile.

        Arguments:
            mydict (dict): The dict to pickle into the statefile.

        We're purposely not acting on self.dict here, and passing the dict in 
        instead, since there may be times we want to record something other than 
        self.mydict (eg we're re-initializing the statefile).
        """
        fh = open( self.statefile, "wb" )
        pickle.dump( mydict, fh )

    def _read_statefile( self ):
        """ Sets self.mydict equal to whatever is currently stored in the 
        statefile.  Must be called after _set_statefile().
        """
        fh = open( self.statefile, "rb" )
        self.mydict = pickle.load(fh)

    def _set_statefile( self ):
        """ Get the path to the statefile based on the current empire name.  If 
        the statefile doesn't exist yet, this creates and initializes it.

        Returns:
            os.path: The path to the statefile
        """
        fn = self.client.empire.name + "_bodyabbrv.pkl"
        self.statefile = os.path.join(self.vardir, fn)
        if not os.path.isfile(self.statefile):
            self._put_data( Abbreviations.mydict )   # initialize statefile as pickle file with empty dict

    def delete( self, name ):
        """ Deletes an abbreviation assignment, given the assignment's full name.
        """
        if name == 'all':
            yn = input("I'm about to delete all of your abbreviations - is that what you want [y/N]?")
            if not re.match('^y', yn, re.I):
                print( "OK, bailing!" )
                quit()
        else:
            existing_abbrv = self.mydict['name'][ name ]
            if existing_abbrv:
                del self.mydict['abbrv'][existing_abbrv]
            if self.mydict['name'][name]:
                del self.mydict['name'][name]
        self._put_data(self.mydict)

    def get_abbrv( self, name ):
        """ Gets the abbreviation for a full name.

        Arguments:
            name (str): Full name of a body

        Returns:
            abbrv (str): The abbreviation set for that body

        Raises:
            KeyError if no abbreviation is set for the given body.
        """
        if self.mydict['name'][ name ]:
            return self.mydict['name'][name]
        else:
            raise KeyError( "No abbreviation is set for {}.".format(name) )

    def get_name( self, abbrv ):
        """ Gets the full name for an abbreviation

        Arguments:
            abbrv_or_name (str): Either a pre-set abbreviation or a body full 
            name.  If the given string is not found in the abbreviations 
            database, it's assumed to be a full body name and returned as-is.

        Returns:
            full_name (str): If the abbrv passed in was a set abbreviation, 
            returns the full unabbreviated name.  If the abbrv was not a 
            set abbreviation, but matches a body name (either colony or 
            space station), that string is returned as passed in.

        Raises:
            KeyError: If the abbrv passed in is neither a set abbreviation nor 
            a valid body name.
        """
        if self.mydict['abbrv'][ abbrv ]:
            return self.mydict['abbrv'][abbrv]
        elif abbrv in self.client.planet_names.keys():
            return abbrv
        else:
            raise KeyError( "{} is neither an assigned abbreviation nor a body name.".format(abbrv) )

    def save( self, name, abbrv ):
        """ Saves an abbreviation assignment.

        Arguments:
            name (str): The full name
            abbrv (str): The abbreviation
        """
        if name == 'all':
            raise KeyError( "Don't use 'all' when setting an abbreviation, silly." )
        self.mydict['abbrv'][ abbrv ]   = name
        self.mydict['name'][ name ]     = abbrv
        self._put_data(self.mydict)

    def show_all(self):
        """ Produces a report on all currently-stored abbreviations.
        """
        print( '' )
        if self.mydict['name'].keys():
            print( "{:<50} {}".format("FULL NAME", "ABBREVIATION") )
            for name in sorted(self.mydict['name'].keys()):
                showname = self.summarize( name, 50 )
                print( "{:<50} {}".format(showname, self.get_abbrv(name)) )
        else:
            print( "You don't have any abbreviations set up yet." )
        print( '' )

    def show( self, name ):
        """ Produces a report on a single stored abbreviation.
        """
        self._get_data()
        if name == 'all':
            self.show_all()
        elif name in self.mydict['name']:
            print( "{} is abbreviated as '{}'.".format(name, self.get_abbrv(name)) )
        else:
            print( "No abbreviation is currently set for {}".format(name) )


    def summarize( self, string:str, mymax:int ):
        """ Summarizes a string, usually for inclusion in a report section 
        with a fixed width.

        Arguments:
            string (str): String to summarize
            max (int): Max length of the string.  Must be greater than 3.

        If the string is "abcdefghijk" and the max is 6, this will return 
        "abc..."

        Returns the summarized string, or the original string if it was shorter 
        than max.
        """
        mymax = 4 if mymax < 4 else mymax
        if len(string) > mymax:
            submax = mymax - 3
            string = string[0:submax] + "..."
        return string

