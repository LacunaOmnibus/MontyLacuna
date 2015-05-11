
import lacuna, lacuna.binutils.libbin, lacuna.types
import lacuna.exceptions as err
from lacuna.abbreviations import Abbreviations
import argparse, operator, os, pickle, re, sys

class SetBodyAbbrv(lacuna.binutils.libbin.Script):
    """ Sets body abbreviations.
    """

    def __init__(self):
        self.version = '0.1'
        parser = argparse.ArgumentParser(
            description = 'Sets an abbreviation for a full body name.',
            epilog      = "Full docs can be found at http://tmtowtdi.github.io/MontyLacuna/scripts/abbrv.html",
        )
        parser.add_argument( 'name', 
            metavar     = '<body>',
            action      = 'store',
            help        = "The full name of the body to abbreviate or check on.  Use 'all' if you're showing abbreviations and want to see them all."
        )
        parser.add_argument( 'abbrv', 
            metavar     = '<abbreviation>',
            action      = 'store',
            help        = "The abbreviation to use.",
        )
        super().__init__(parser)
        self.abbrv = Abbreviations(self.client)

class ShowBodyAbbrv(lacuna.binutils.libbin.Script):
    """ Displays body abbreviations.
    """
    def __init__(self):
        self.version = '0.1'
        parser = argparse.ArgumentParser(
            description = "Shows the abbrevation for a full body name.  The name 'all' can be passed to see all abbrevations.",
            epilog      = "Full docs can be found at http://tmtowtdi.github.io/MontyLacuna/scripts/abbrv.html",
        )
        parser.add_argument( 'name', 
            metavar     = '<body>',
            action      = 'store',
            help        = "The full name of the body to abbreviate or check on.  Use 'all' if you're showing abbreviations and want to see them all."
        )
        super().__init__(parser)
        self.abbrv = Abbreviations(self.client)

class DelBodyAbbrv(lacuna.binutils.libbin.Script):
    """ Deletes body abbreviations.
    """
    def __init__(self):
        self.version = '0.1'
        parser = argparse.ArgumentParser(
            description = "Deletes the abbrevation for a full body name.",
            epilog      = "Full docs can be found at http://tmtowtdi.github.io/MontyLacuna/scripts/abbrv.html",
        )
        parser.add_argument( 'name', 
            metavar     = '<body>',
            action      = 'store',
            help        = "The full name of the body to abbreviate or check on.  Use 'all' if you're showing abbreviations and want to see them all."
        )
        super().__init__(parser)
        self.abbrv = Abbreviations(self.client)

