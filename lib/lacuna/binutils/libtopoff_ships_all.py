
import lacuna, lacuna.binutils.libbin
import argparse, os, sys

class TopoffShips(lacuna.binutils.libbin.Script):

    def __init__(self):
        self.version = '0.1'
        parser = argparse.ArgumentParser(
            description = 'Topoff a certain ship type on all of your planets.  Commonly used to keep up with excavators.',
            epilog      = "EXAMPLE: python bin/topoff_ships_all.py -level 30 sweeper 20",
        )
        parser.add_argument( 'type', 
            metavar     = '<shiptype>',
            action      = 'store',
            help        = "Type of ship to build (eg 'scow_mega')."
        )
        parser.add_argument( 'num', 
            metavar     = '<count>',
            action      = 'store',
            type        = int,
            default     = 1,
            help        = "Minimum number of ships of this type each planet should have on hand.  Defaults to 1."
        )
        parser.add_argument( '--level', 
            metavar     = '<lvl>',
            dest        = 'min_lvl',
            action      = 'store',
            type        = int,
            default     = 1,
            help        = 'Minimum shipyard level to use for building.  Defaults to 1.'
        )
        super().__init__(parser)

