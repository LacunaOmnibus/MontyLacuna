
### Search on CHECK

import lacuna, lacuna.binutils.libbin
from lacuna.plan import OwnedPlan
import lacuna.exceptions as err
import argparse, os, re, sys

class StarterKit():
    """ Base class for starter kits
    """
    def __init__( self, client, price:float, plans:list ):
        self.client = price
        self.price  = price
        self.plans  = plans

    def update_all_levels( self, level:int = 1, ebl:int = 0  ):
        for p in self.plans:
            p.level = level
            p.extra_build_level = ebl

class ResKit( StarterKit ):
    def __init__( self, client, price:float = 0.1 ):
        plans = [
            OwnedPlan( client, {'name': 'Algae Pond', 'level': 1, 'extra_build_level': 0, 'quantity': 1} ),
            OwnedPlan( client, {'name': 'Amalgus Meadow', 'level': 1, 'extra_build_level': 0, 'quantity': 1} ),
            OwnedPlan( client, {'name': 'Beeldeban Nest', 'level': 1, 'extra_build_level': 0, 'quantity': 1} ),
            OwnedPlan( client, {'name': 'Denton Brambles', 'level': 1, 'extra_build_level': 0, 'quantity': 1} ),
            OwnedPlan( client, {'name': 'Geo Thermal Vent', 'level': 1, 'extra_build_level': 0, 'quantity': 1} ),
            OwnedPlan( client, {'name': 'Lapis Forest', 'level': 1, 'extra_build_level': 0, 'quantity': 1} ),
            OwnedPlan( client, {'name': 'Malcud Field', 'level': 1, 'extra_build_level': 0, 'quantity': 1} ),
            OwnedPlan( client, {'name': 'Natural Spring', 'level': 1, 'extra_build_level': 0, 'quantity': 1} ),
            OwnedPlan( client, {'name': 'Volcano', 'level': 1, 'extra_build_level': 0, 'quantity': 1} ),
        ]
        super().__init__( client, price, plans );

class StorageKit( StarterKit ):
    def __init__( self, client, price:float = 0.1 ):
        plans = [
            OwnedPlan( client, {'name': 'Interdimensional Rift', 'level': 1, 'extra_build_level': 0, 'quantity': 1} ),
            OwnedPlan( client, {'name': 'Ravine', 'level': 1, 'extra_build_level': 0, 'quantity': 1} ),
        ]
        super().__init__( client, price, plans );

class MilitaryKit( StarterKit ):
    """ These aren't all necessarily military, but have some relation to either 
    offense or defense.
    """
    def __init__( self, client, price:float = 0.1 ):
        plans = [
            OwnedPlan( client, {'name': 'Citadel of Knope', 'level': 1, 'extra_build_level': 0, 'quantity': 1} ),
            OwnedPlan( client, {'name': 'Crashed Ship Site', 'level': 1, 'extra_build_level': 0, 'quantity': 1} ),
            OwnedPlan( client, {'name': "Gratch's Gauntlet", 'level': 1, 'extra_build_level': 0, 'quantity': 1} ),
            OwnedPlan( client, {'name': 'Kalavian Ruins', 'level': 1, 'extra_build_level': 0, 'quantity': 1} ),
        ]
        super().__init__( client, price, plans );

class UtilityKit( StarterKit ):
    def __init__( self, client, price:float = 0.1 ):
        plans = [
            OwnedPlan( client, {'name': 'Black Hole Generator', 'level': 1, 'extra_build_level': 0, 'quantity': 1} ),
            OwnedPlan( client, {'name': 'Library of Jith', 'level': 1, 'extra_build_level': 0, 'quantity': 1} ),
            OwnedPlan( client, {'name': 'Oracle of Anid', 'level': 1, 'extra_build_level': 0, 'quantity': 1} ),
            OwnedPlan( client, {'name': 'Pantheon of Hagness', 'level': 1, 'extra_build_level': 0, 'quantity': 1} ),
            OwnedPlan( client, {'name': 'Temple of the Drajilites', 'level': 1, 'extra_build_level': 0, 'quantity': 1} ),
        ]
        super().__init__( client, price, plans );

class BeachKit( StarterKit ):
    def __init__( self, client, price:float = 0.1 ):
        plans = [
            OwnedPlan( client, {'name': 'Beach [1]', 'level': 1, 'extra_build_level': 0, 'quantity': 1} ),
            OwnedPlan( client, {'name': 'Beach [2]', 'level': 1, 'extra_build_level': 0, 'quantity': 1} ),
            OwnedPlan( client, {'name': 'Beach [3]', 'level': 1, 'extra_build_level': 0, 'quantity': 1} ),
            OwnedPlan( client, {'name': 'Beach [4]', 'level': 1, 'extra_build_level': 0, 'quantity': 1} ),
            OwnedPlan( client, {'name': 'Beach [5]', 'level': 1, 'extra_build_level': 0, 'quantity': 1} ),
            OwnedPlan( client, {'name': 'Beach [6]', 'level': 1, 'extra_build_level': 0, 'quantity': 1} ),
            OwnedPlan( client, {'name': 'Beach [7]', 'level': 1, 'extra_build_level': 0, 'quantity': 1} ),
            OwnedPlan( client, {'name': 'Beach [8]', 'level': 1, 'extra_build_level': 0, 'quantity': 1} ),
            OwnedPlan( client, {'name': 'Beach [9]', 'level': 1, 'extra_build_level': 0, 'quantity': 1} ),
            OwnedPlan( client, {'name': 'Beach [10]', 'level': 1, 'extra_build_level': 0, 'quantity': 1} ),
            OwnedPlan( client, {'name': 'Beach [11]', 'level': 1, 'extra_build_level': 0, 'quantity': 1} ),
            OwnedPlan( client, {'name': 'Beach [12]', 'level': 1, 'extra_build_level': 0, 'quantity': 1} ),
            OwnedPlan( client, {'name': 'Beach [13]', 'level': 1, 'extra_build_level': 0, 'quantity': 1} ),
        ]
        super().__init__( client, price, plans );

class DecoKit( StarterKit ):
    def __init__( self, client, price:float = 0.1 ):
        plans = [
            OwnedPlan( client, {'name': 'Crater', 'level': 1, 'extra_build_level': 0, 'quantity': 1} ),
            OwnedPlan( client, {'name': 'Grove of Trees', 'level': 1, 'extra_build_level': 0, 'quantity': 1} ),
            OwnedPlan( client, {'name': 'Lagoon', 'level': 1, 'extra_build_level': 0, 'quantity': 1} ),
            OwnedPlan( client, {'name': 'Lake', 'level': 1, 'extra_build_level': 0, 'quantity': 1} ),
            OwnedPlan( client, {'name': 'Patch of Sand', 'level': 1, 'extra_build_level': 0, 'quantity': 1} ),
            OwnedPlan( client, {'name': 'Rocky Outcropping', 'level': 1, 'extra_build_level': 0, 'quantity': 1} ),
        ]
        super().__init__( client, price, plans );

class ComboKit( StarterKit ):
    def __init__( self, kits:list, force_combo_price:float = 0 ):
        self.price = force_combo_price if force_combo_price else 0
        for k in kits:
            if not force_combo_price:
                self.price += k.price
            for p in k.plans:
                self.plans.append( p )

class FullBasicKit( ComboKit ):
    """ A combination of the ResKit and StorageKit
    """
    def __init__( self, client, price:float = 0.1 ):
        super().__init__( [ResKit(client), StorageKit(client)], 0.1 )

class BigKit( ComboKit ):
    """ A combination of ResKit, StorageKit, MilitaryKit, and UtilityKit
    """
    def __init__( self, client, price:float = 0.1 ):
        super().__init__( [ResKit(client), StorageKit(client), MilitaryKit(client), UtilityKit(client)], 0.1 )


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
        parser.add_argument( 'kit', 
            metavar     = '<name>',
            action      = 'store',
            default     = 'res',
            choices     = [
                            'resource', 'res',
                            'storage', 'store', 'stor',
                            'military', 'mil',
                            'utility', 'util', 'ute',
                            'deco',
                            'fullbasic', 'full_basic', 'full',
                            'big'
                          ],
            help        = "Which kit should we post?  See the online docs for a list of kit names.  Defaults to 'res'."
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
            help        = "What level plans should be in your kit?  Most kits use level 1 plans by default."
        )
        parser.add_argument( '--ebl', 
            metavar     = '<extra build level>',
            action      = 'store',
            help        = "Do you want your plans to include an extra build level (the 'x' in a '1+x' plan)?  Most kits use no extra build level by default."
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

        self._set_kit()
        self._set_planet()
        self._set_trade()

    def _set_kit( self ):
        m_bea   = re.compile("^bea", re.I)
        m_big   = re.compile("^big", re.I)
        m_dec   = re.compile("^dec", re.I)
        m_ful   = re.compile("^ful", re.I)
        m_mil   = re.compile("^mil", re.I)
        m_res   = re.compile("^res", re.I)
        m_stor  = re.compile("^stor", re.I)
        m_ute   = re.compile("^ut", re.I)

        if m_res.match(self.args.kit):
            self.kit = ResKit( self.client, self.args.price )
        elif m_stor.match(self.args.kit):
            self.kit = StorageKit( self.client, self.args.price )
        elif m_mil.match(self.args.kit):
            self.kit = MilitaryKit( self.client, self.args.price )
        elif m_ute.match(self.args.kit):
            self.kit = UtilityKit( self.client, self.args.price )
        elif m_dec.match(self.args.kit):
            self.kit = DecoKit( self.client, self.args.price )
        elif m_bea.match(self.args.kit):
            self.kit = BeachKit( self.client, self.args.price )
        elif m_ful.match(self.args.kit):
            self.kit = FullBasicKit( self.client, self.args.price )
        elif m_big.match(self.args.kit):
            self.kit = BigKit( self.client, self.args.price )

        if not self.kit:
            raise KeyError("What are you doing, Dave?  That's not a legal kit and I don't know how you managed that.")

        if self.args.level or self.args.ebl:
            self.kit.update_all_levels( self.args.level, self.args.ebl )

    def _set_planet( self ):
        self.client.cache_on( 'post_kits', 3600 )
        self.planet = self.client.get_body_byname( self.args.name )
        self.client.cache_off()

    def _set_trade( self ):
        """ Sets self.trade to either a trade ministry or SST object, depending 
        on what the user asked for.  Requires that _set_planet() already be 
        called.
        """
        if self.args.sst:
            self.trade = self.planet.get_buildings_bytype( 'transporter', 1, 1, 100 )[0]
        else:
            self.trade = self.planet.get_buildings_bytype( 'trade', 1, 1, 100 )[0]

    def post_kit(self):
        """ Actually posts the chosen kit to the chosen trade building.
        """
        pass
        ### CHECK
        ### neither of the post_*() methods below work (or exist) yet.
        #if type(self.trade) is lacuna.buildings.callable.trade.trade:
        #    self.post_tm_trade()
        #elif type(self.trade) is lacuna.buildings.callable.trade.transporter:
        #    self.post_sst_trade()


    def validate_plans(self):
        """ Checks that you actually have on-hand the plans required by the 
        current kit.  Requires that _set_kit() and _set_trade() already be 
        called.

        Raises :class:`lacuna.exceptions.MissingResourceError` if your kit 
        requires a plan you haven't got in stock.
        """
        def getkey(plan):
            ebl = plan.extra_build_level
            key = plan.name + ':' + str(plan.level) + ':' + str(ebl)
            return key

        plans, space = self.trade.get_plan_summary()
        gotplans = {}
        for p in plans:
            key = getkey(p)
            gotplans[ key ] = 1
        for p in self.kit.plans:
            key = getkey(p)
            if not key in gotplans:
                raise err.MissingResourceError("Your kit requires a {}+{} {} plan, but you don't have one on hand."
                    .format(p.level, p.extra_build_level, p.name)
                )
        return True


