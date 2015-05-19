
import os, pickle, pydoc, sys
import lacuna

class Abbreviations():
    """ Saves personal abbreviations for often-long body names.

    Arguments:
        client (lacuna.clients.Member): The client we're currently connected
                                        as.
        vardir (str): The path to the Monty var/ directory.  Defaults to
                      ``CALLING_SCRIPT/../var/``.
    """

    bindir = os.path.abspath(os.path.dirname(sys.argv[0]))
    vardir = os.path.abspath(bindir + "/../var")

    mydict = { 
        'version': '1.0',
        'abbrv': {}, 
        'name': {}
    }

    def __init__(self, client, vardir = None):
        self.client     = client
        self.statefile  = None
        self.utils      = lacuna.utils.Utils()
        if vardir and os.path.isdir(vardir):
            self.vardir = vardir

        self._set_statefile()
        self._read_statefile()

    def _get_data( self ):
        fh = open( self.statefile, "rb" )
        self.mydict = pickle.load(fh)

    def _read_statefile( self ):
        """ Sets self.mydict equal to whatever is currently stored in the 
        statefile.  Must be called after _set_statefile().
        """
        fh = open( self.statefile, "rb" )
        self.mydict = pickle.load(fh)

    def _save_dict( self, mydict:dict ):
        """ Puts data in mydict into the statefile.

        Arguments:
            mydict (dict): The dict to pickle into the statefile.

        We're purposely not acting on self.dict here, and passing the dict in 
        instead, since there may be times we want to record something other than 
        self.mydict (eg we're re-initializing the statefile).
        """
        fh = open( self.statefile, "wb" )
        pickle.dump( mydict, fh )

    def _set_statefile( self ):
        """ Get the path to the statefile based on the current empire name.  If 
        the statefile doesn't exist yet, this creates and initializes it.

        Returns:
            os.path: The path to the statefile
        """
        fn = self.client.empire.name + "_bodyabbrv.pkl"
        self.statefile = os.path.join(self.vardir, fn)
        if not os.path.isfile(self.statefile):
            self._save_dict( Abbreviations.mydict )   # initialize statefile as pickle file with empty dict

    def delete( self, name ):
        """ Deletes an abbreviation assignment, given the assignment's full name.

        Arguments:
            name (str): Full name of a body; its abbreviation will be removed.

        Raises:
            KeyError: If no abbreviation exists for ``name``.
        """
        if name == 'all':
            yn = input("I'm about to delete all of your abbreviations - is that what you want [y/N]?")
            if not re.match('^y', yn, re.I):
                print( "OK, bailing!" )
                quit()
        else:
            if name in self.mydict['name']:
                abbrv = self.mydict['name'][ name ]
                del self.mydict['abbrv'][abbrv]
                del self.mydict['name'][name]
            else:
                raise KeyError("No abbreviation exists for {}.".format(name))
        self._save_dict(self.mydict)

    def get_abbrv( self, name ):
        """ Gets the abbreviation for a full name.

        Arguments:
            name (str): Full name of a body

        Returns:
            abbrv (str): The abbreviation set for that body

        Raises:
            KeyError: if no abbreviation is set for ``name``.
        """
        if self.mydict['name'][ name ]:
            return self.mydict['name'][name]
        else:
            raise KeyError( "No abbreviation is set for {}.".format(name) )

    def get_name( self, abbrv ):
        """ Gets the full name for an abbreviation

        Arguments:
            abbrv_or_name (str): Either a pre-set abbreviation or a body full
                                 name.  If the given string is not found in 
                                 the abbreviations database, it's assumed to 
                                 be a full body name and returned as-is.

        Returns:
            full_name (str): If the argument was a set abbreviation, returns
                             the full unabbreviated name.  If the argument was 
                             not a set abbreviation, but matches a body name 
                             (either colony or space station), that argument 
                             is returned as passed in.

        Raises:
            KeyError: If the abbrv passed in is neither a set abbreviation nor
                      a valid body name.

        """
        if abbrv in self.mydict['abbrv']:
            return self.mydict['abbrv'][abbrv]
        elif abbrv in self.client.empire.planet_names.keys():
            return abbrv
        else:
            raise KeyError( "{} is neither an assigned abbreviation nor a body name.".format(abbrv) )

    def list_abbrvs( self ):
        """ Get a list of currently-set abbreviations

        Returns:
            list (list of str): Alpha-sorted list of abbreviations
        """
        return sorted( self.mydict['abbrv'].keys() )

    def list_names( self ):
        """ Get a list of full body names for which there are abbreviations set

        Returns:
            list (list of str): Alpha-sorted list of names
        """
        return sorted( self.mydict['name'].keys() )

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
        self._save_dict(self.mydict)

    def show_all(self):
        """ Produces a report on all currently-stored abbreviations.

        The report is displayed on STDOUT via a pager.
        """
        output = "\n"
        if self.mydict['name'].keys():
            output += "{:<50} {}\n".format("FULL NAME", "ABBREVIATION")
            for name in sorted(self.mydict['name'].keys(), key=lambda s: s.lower()):
                showname = self.utils.summarize( name, 50 )
                output += "{:<50} {}\n".format(showname, self.get_abbrv(name))
        else:
            print( "You don't have any abbreviations set up yet." )
        pydoc.pager( output )

    def show( self, name ):
        """ Produces a report on a single stored abbreviation.

        The report is displayed on STDOUT.  If we're reporting on 'all' 
        abbreviations, the report is displayed via a pager.
        """
        self._get_data()
        if name == 'all':
            self.show_all()
        elif name in self.mydict['name']:
            print( "{} is abbreviated as '{}'.".format(name, self.get_abbrv(name)) )
        else:
            print( "No abbreviation is currently set for {}".format(name) )

