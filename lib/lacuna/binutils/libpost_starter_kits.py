
import lacuna, lacuna.binutils.libbin
import lacuna.exceptions as err
import argparse, os, sys

class StarterKit():
    """ Base class for starter kits
    """
    def __init__( self, price:float, plans:dict ):
        self.price  = price
        self.plans  = plans

    def update_all_levels( self, level:int ):
        for plan in self.plans:
            self.plans[ plan ] = level

class ResKit( StarterKit ):
    def __init__( self, price:float = 0.1 ):
        plans = {
            'Algae Pond':       1,
            'Amalgus Meadow':   1,
            'Beeldeban Nest':   1,
            'Denton Brambles':  1,
            'Geo Thermal Vent': 1,
            'Lapis Forest':     1,
            'Malcud Field':     1,
            'Natural Spring':   1,
            'Volcano':          1,
        }
        super().__init__( price, plans );

class StorageKit( StarterKit ):
    def __init__( self, price:float = 0.1 ):
        plans = {
            'Interdimensional Rift':    1,
            'Ravine':                   1,
        }
        super().__init__( price, plans );

class MilitaryKit( StarterKit ):
    """ These aren't all necessarily military, but have some relation to either 
    offense or defense.
    """
    def __init__( self, price:float = 0.1 ):
        plans = {
            'Citadel of Knope':    1,
            'Crashed Ship Site':   1,
            "Gratch's Gauntlet":   1,
            'Kalavian Ruins':   1,
        }
        super().__init__( price, plans );

class UtilityKit( StarterKit ):
    def __init__( self, price:float = 0.1 ):
        plans = {
            'Black Hole Generator':     1,
            'Library of Jith':          1,
            'Oracle of Anid':           1,
            'Pantheon of Hagness':      1,
            'Temple of the Drajilites': 1,
        }
        super().__init__( price, plans );

class DecoKit( StarterKit ):
    def __init__( self, price:float = 0.1 ):
        plans = {
            'Beach [1]':            1,
            'Beach [2]':            1,
            'Beach [3]':            1,
            'Beach [4]':            1,
            'Beach [5]':            1,
            'Beach [6]':            1,
            'Beach [7]':            1,
            'Beach [8]':            1,
            'Beach [9]':            1,
            'Beach [10]':           1,
            'Beach [11]':           1,
            'Beach [12]':           1,
            'Beach [13]':           1,
            'Crater':               1,
            'Grove of Trees':       1,
            'Lagoon':               1,
            'Lake':                 1,
            'Patch of Sand':        1,
            'Rocky Outcropping':    1,
        }
        super().__init__( price, plans );

class ComboKit( StarterKit ):
    def __init__( self, kits:list, price:float = 0 ):
        self.price = price if price else 0
        for k in kits:
            if not price:
                self.price += k.price
            for plan, level in k.plans.items():
                self.plans[ plan ] = level


class PostStarterKit(lacuna.binutils.libbin.Script):
    """ Gather and report on spy data by planet.
    """

    def __init__(self):
        self.version = '0.1'
        parser = argparse.ArgumentParser(
            description = 'CHECK',
            epilog      = "EXAMPLE: CHECK python bin/spies_report.py Earth",
        )
        parser.add_argument( 'name', 
            metavar     = '<planet>',
            action      = 'store',
            help        = "Produce report on spies at this planet.  'all' to report on all planets."
        )
        parser.add_argument( '--num', 
            metavar     = '<num>',
            action      = 'store',
            default     = 1,
            help        = "How many kits should we post?  Defaults to 1."
        )
        parser.add_argument( '--level', 
            metavar     = '<level>',
            action      = 'store',
            default     = 1,
            help        = "What level plans should be in your kit?  Defaults to 1."
        )
        parser.add_argument( '--sst', 
            action      = 'store_true',
            help        = "By default, we post kits to the Trade Ministry.  If you pass this argument, we'll post to the SST instead.  CAUTION you will be charged 1 E per kit posted for using this option."
        )
        parser.add_argument( '--price', 
            metavar     = '<price>',
            action      = 'store',
            type        = float,
            default     = 0.1,
            help        = "How much should we charge for your kit?  Defaults to 0.1."
        )
        super().__init__(parser)

        if self.args.sst:
            self._set_sst()
        else:
            self._set_trademin()


    def _set_trademin( self ):
        """ Finds the Trade Ministry on the current planet.

        Raises :class:`lacuna.exceptions.NoSuchBuildingError` if the planet 
        being set does not have a working Trade Ministry.
        """
        self.trade = self.planet.get_buildings_bytype( 'trade', 1, 1, 100 )[0]

    def _set_sst( self ):
        """ Finds the Subspace Transporter on the current planet.

        Raises :class:`lacuna.exceptions.NoSuchBuildingError` if the planet 
        being set does not have a working Subspace Transporter.
        """
        self.trade = self.planet.get_buildings_bytype( 'transporter', 1, 1, 100 )[0]

