
import lacuna, lacuna.binutils.libbin
import argparse, os, sys

class CHECK(lacuna.binutils.libbin.Script):

    def __init__(self):
        self.version = '0.1'
        parser = argparse.ArgumentParser(
            description = 'I SHOW UP ABOVE THE OPTIONS SECTION IN HELP',
            epilog      = 'I SHOW UP BELOW THE OPTIONS SECTION IN HELP',
        )
        ###
        ### lacuna.binutils.libbin.Script gives you config_file and 
        ### config_section arguments automatically.  Add any others you need 
        ### for this particular script.
        ###
        ### The 'planet' and 'quiet' arguments included below are commonly 
        ### included, but not always.  Remove em if you don't want em.
        ###
        parser.add_argument( 'name', 
            metavar     = '<planet>',
            action      = 'store',
            help        = 'All spies from this planet will be recalled.'
        )
        super().__init__(parser)

        ###
        ### If your script requires a real, not sitter, password, use the 
        ### __init__ call below instead of the one above. Otherwise, remove 
        ### the line below.
        ###
        #super().__init__(parser, 'real')   

