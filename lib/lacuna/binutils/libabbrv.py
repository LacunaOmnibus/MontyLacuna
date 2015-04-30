
import lacuna, lacuna.binutils.libbin, lacuna.types
import lacuna.exceptions as err
import argparse, operator, os, pickle, re, sys


### Much of the code in here should be moved out to an Abbrv class that 
### doesn't require libbin.Script, so I can get at the abbreviations set by 
### this script elsewhere.
###
### Eventually I'm going to have enough abbreviations that showing them all 
### will scroll the screen.  Need to find some sort of pager for that.


class SetBodyAbbrv(lacuna.binutils.libbin.Script):
    """ Sets and displays body abbreviations.
    """

    def __init__(self):
        self.version = '0.1'

        parser = argparse.ArgumentParser(
            description = 'CHECK',
            epilog      = "Full docs can be found at http://tmtowtdi.github.io/MontyLacuna/scripts/abbrv.html",
        )
        parser.add_argument( '--do', 
            action      = 'store',
            help        = "Choices are 'show', 'set', 'delete'.",
            choices     = ['show', 'set', 'delete']
        )
        parser.add_argument( '--abbrv', 
            metavar     = '<abbreviation>',
            action      = 'store',
            help        = "The abbreviation to use.",
        )
        parser.add_argument( 'name', 
            metavar     = '<body>',
            action      = 'store',
            help        = "The full name of the body to abbreviate or check on.  Use 'all' if you're showing abbreviations and want to see them all."
        )
        super().__init__(parser)

        self.set_vardir()
        self.set_statefile()
        self.do_eet()

    def do_eet(self):
        if self.args.do == 'show':
            self.show_abbrv()
        elif self.args.do == 'set':
            self.save_abbrv()
        elif self.args.do == 'delete':
            self.delete_abbrv()
        else:
            raise KeyError("What are you doing, Dave?")

    def show_abbrv( self ):
        mydict = self.get_data()
        if self.args.name == 'all':
            self.show_all_abbrvs()
        elif self.args.name in mydict['name']:
            print( "{} is abbreviated as '{}'.".format(self.args.name, mydict['name'][self.args.name]) )
        else:
            print( "No abbreviation is currently set for {}".format(self.args.name) )

    def show_all_abbrvs(self):
        mydict = self.get_data()
        spaces = ' '*10
        if mydict['name'].keys():
            print( '' )
            print( "{}{}".format(spaces, "CURRENTLY SET ABBREVIATIONS") )
            for name in sorted(mydict['name'].keys()):
                print( "{}{:<30} {}".format(spaces, name, mydict['name'][name]) )
        else:
            print( "You don't have any abbreviations set up yet." )

    def save_abbrv( self ):
        mydict = self.get_data()
        if self.args.name == 'all':
            raise KeyError( "Don't use 'all' when setting an abbreviation, silly." )
        mydict['abbrv'][ self.args.abbrv ]  = self.args.name
        mydict['name'][ self.args.name ]    = self.args.abbrv
        self.put_data(mydict)
        print( "{} can now be abbreviated as '{}'.".format(self.args.name, self.args.abbrv) )

    def delete_abbrv( self ):
        mydict = self.get_data()

        if self.args.name == 'all':
            yn = input("I'm about to delete all of your abbreviations - is that what you want [y/N]?")
            if not re.match('^y', yn, re.I):
                print( "OK, bailing!" )
                quit()
            else:
                mydict = self.init_dict();
        else:
            existing_abbrv = mydict['name'][ self.args.name ]
            if existing_abbrv:
                del mydict['abbrv'][existing_abbrv]
            if mydict['name'][self.args.name]:
                del mydict['name'][self.args.name]

        self.put_data(mydict)

    def set_vardir( self ):
        self.vardir =  os.path.abspath(self.bindir + "/../var")
        assert os.path.isdir(self.vardir) == True

    def set_statefile( self ):
        """ Get the path to the statefile.

        Returns:
            os.path: The path to the statefile
        """
        fn = self.client.empire.name + "_bodyabbrv.pkl"
        self.statefile = os.path.join(self.vardir, fn)

        if not os.path.isfile(self.statefile):
            mydict = self.init_dict()
            self.put_data(mydict)   # initialize statefile as pickle file with empty dict

    def init_dict(self):
        return { 'abbrv': {}, 'name': {} }

    def put_data( self, mydict:dict ):
        fh = open( self.statefile, "wb" )
        pickle.dump( mydict, fh )

    def get_data( self ):
        fh = open( self.statefile, "rb" )
        mydict = pickle.load(fh)
        return mydict

