
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
            p.level = level if level else 1
            p.extra_build_level = ebl if ebl else 0

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

class Halls10Kit( StarterKit ):
    def __init__( self, client, price:float = 0.1 ):
        plans = [
            OwnedPlan( client, {'name': 'Halls of Vrbansk', 'level': 1, 'extra_build_level': 0, 'quantity': 10} )
        ]
        super().__init__( client, price, plans );

class Halls100Kit( StarterKit ):
    def __init__( self, client, price:float = 0.1 ):
        plans = [
            OwnedPlan( client, {'name': 'Halls of Vrbansk', 'level': 1, 'extra_build_level': 0, 'quantity': 100} )
        ]
        super().__init__( client, price, plans );

class ComboKit( StarterKit ):
    def __init__( self, kits:list, force_combo_price:float = 0 ):
        self.price = force_combo_price if force_combo_price else 0
        self.plans = []
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
            description = 'Posts one of several starter kits to either the Trade Ministry or the SST on a specific planet.  See the online documentation for a list of the different types of kits available.',
            epilog      = "EXAMPLE: CHECK python bin/post_starter_kit.py Earth resources",
        )
        parser.add_argument( 'name', 
            metavar     = '<planet>',
            action      = 'store',
            help        = "Post a kit from this planet."
        )
        parser.add_argument( 'kit', 
            metavar     = '<name>',
            action      = 'store',
            choices     = [
                            'resources', 'resource', 'res',
                            'storage', 'store', 'stor',
                            'military', 'mil',
                            'utility', 'util', 'ute',
                            'decoration', 'deco',
                            'beach',
                            'fullbasic', 'full_basic', 'full',
                            'big'
                            'halls10',  'hall10',  'h10',
                            'halls100', 'hall100', 'h100',
                          ],
            help        = "Which kit should we post?  See the online docs for a list of kit names."
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
        parser.add_argument( '-sst', '--sst', 
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

        self.plan_size = 0      # set by validate_plans()

        ### The plan named "Algae Pond" is of type "Permanent_AlgaePond", 
        ### which is what we have to send.  This will translate "Algae Pond" 
        ### to the required "Permanent_AlgaePond".  Set by validate_plans()
        self.type_translator = {}

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
        m_h10   = re.compile("^h\w*10$", re.I)
        m_h100  = re.compile("^h\w*100$", re.I)
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
        elif m_h10.match(self.args.kit):
            self.kit = Halls10Kit( self.client, self.args.price )
        elif m_h100.match(self.args.kit):
            self.kit = Halls100Kit( self.client, self.args.price )

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
        id = None
        if type(self.trade) is lacuna.buildings.callable.trade.trade:
            trade_id = self._post_tm_trade()
        elif type(self.trade) is lacuna.buildings.callable.transporter.transporter:
            trade_id = self._post_sst_trade()
        return trade_id

    def _post_tm_trade(self):
        offer, size = self._make_offer()
        ship = self._find_fastest_ship(size)
        return self.trade.add_to_market(
                        offer,
                        self.args.price,
                        { 'ship_id': ship.id }
                    )

    def _post_sst_trade(self):
        offer, size = self._make_offer()
        sst_max = self.trade.view()
        if sst_max < size:
            raise err.InsufficientResourceError(
                "Your SST has a max trade of {,}, but your kit's size is {,}."
                .format( sst_max, size )
            )
        return self.trade.add_to_market( offer, self.args.price )

    def _make_offer(self):
        """ Creates the 'offer' list of dicts required by both the TM and SST.

        Returns a tuple:
            - offer -- list of dicts containing your trade item details
            - size -- integer total size of the trade
        """
        offer = [] 
        size = 0
        for p in self.kit.plans:
            size += (self.plan_size * p.quantity)
            offer.append(
                {
                    'type':                 'plan',
                    'plan_type':            self.type_translator[ p.name ],
                    'level':                p.level,
                    'extra_build_level':    p.extra_build_level,
                    'quantity':             p.quantity,
                }
            )
        return(offer, size)

    def _find_fastest_ship(self, size:int):
        """ Finds the fastest trade ship available that's capable of carrying 
        your kit.

        Arguments:
            - size -- Integer size of your kit
        """
        fastest = 0
        ship    = ''
        ships   = self.trade.get_trade_ships()
        for s in ships:
            if s.hold_size > size and s.task == 'Docked' and s.speed > fastest:
                ship = s
                fastest = s.speed
        if not ship:
            raise err.MissingResourceError("You haven't got a trade ship capable of carrying your kit.")
        return ship

    def validate_plans(self):
        """ Checks that you actually have on-hand the plans required by the 
        current kit.  Requires that _set_kit() and _set_trade() already be 
        called.

        Raises :class:`lacuna.exceptions.MissingResourceError` if your kit 
        requires a plan you haven't got in stock.
        """
        def getkey(plan):
            ebl = plan.extra_build_level if plan.extra_build_level else 0
            lvl = plan.level if plan.level else 1
            key = plan.name + ':' + str(lvl) + ':' + str(ebl)
            return key

        if self.args.level and int(self.args.level) > 1 and self.args.ebl:
            raise KeyError("There's no such thing as a {}+{} plan.".format(self.args.level, self.args.ebl))

        plans, self.plan_size = self.trade.get_plan_summary()
        gotplans = {}
        for p in plans:
            self.type_translator[ p.name ] = p.plan_type
            key = getkey(p)
            gotplans[ key ] = 1
        for p in self.kit.plans:
            key = getkey(p)
            if not key in gotplans:
                raise err.MissingResourceError("Your kit requires a {}+{} {} plan, but you don't have one on hand."
                    .format(p.level, p.extra_build_level, p.name)
                )
        return True


