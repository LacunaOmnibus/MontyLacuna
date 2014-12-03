
import binutils.libbin
import argparse, lacuna, os, sys

class CHECK(binutils.libbin.Script):

    def __init__(self):
        self.version = '0.1'
        parser = argparse.ArgumentParser(
            description = 'I SHOW UP ABOVE THE OPTIONS SECTION IN HELP',
            epilog      = 'I SHOW UP BELOW THE OPTIONS SECTION IN HELP',
        )
        ###
        ### binutils.libbin.Script gives you config_file and config_section 
        ### arguments automatically.  Add any others you need for this 
        ### particular script.
        ###
        parser.add_argument( 'name', 
            metavar     = '<planet>',
            action      = 'store',
            help        = 'All spies from this planet will be recalled.'
        )
        parser.add_argument( '--quiet', 
            dest        = 'quiet',
            action      = 'store_true',
            help        = "Silence all output."
        )
        super().__init__(parser)
        ###
        ### Only use this if your script requires a real, not sitter, password 
        ### (eg if your script is creating parliament propositions).  
        ### Otherwise, remove the next line entirely.
        ###
        #super().__init__(parser, 'real')   

