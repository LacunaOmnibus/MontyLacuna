
import lacuna, lacuna.binutils.libbin
from lacuna.plan import OwnedPlan
import lacuna.exceptions as err
import argparse, os, re, sys

class StarterKit():
    """ Base class for starter kits
    """
    def __init__( self, client, price:float, plans:list ):
        self.client = client
        self.price  = price
        self.plans  = plans

    def update_all_levels( self, ebl:int = 0  ):
        """ Changes the extra build level for all plans included in the kit.

        Arguments:
            - ebl -- Integer extra build level.
        """
        for p in self.plans:
            p.extra_build_level = ebl if ebl else 0

    def add_plan( self, name, ebl = 0, quantity = 1 ):
        """ Adds a plan to the kit.
        
        Arguments:
            - name -- String name of the plan to add (eg "Algae Pond").
            - ebl -- Optional integer.  The extra build level for the plan.
            - quantity -- Optional integer.  The number of plans of this type to include.
        """
        self.plans.append( OwnedPlan(self.client, {'name': name, 'level': 1, 'extra_build_level': ebl, 'quantity': quantity}) )

    def del_plan( self, name, ebl = 0, quantity = 1 ):
        """ Deletes a plan from the kit.

        Arguments:
            - name -- String name of the plan to remove (eg "Algae Pond").
            - ebl -- Optional integer.  The extra build level setting of the plan to remove.
            - quantity -- Optional integer.  The quantity value on the plan to remove.
        """
        self.plans = [p for p in self.plans if p.name != name or p.extra_build_level != ebl or p.quantity != quantity ]

class ResKit( StarterKit ):
    def __init__( self, client, price:float = 0.1 ):
        plans = [
            OwnedPlan( client, {'name': 'Algae Pond',       'level': 1, 'extra_build_level': 0, 'quantity': 1} ),
            OwnedPlan( client, {'name': 'Amalgus Meadow',   'level': 1, 'extra_build_level': 0, 'quantity': 1} ),
            OwnedPlan( client, {'name': 'Beeldeban Nest',   'level': 1, 'extra_build_level': 0, 'quantity': 1} ),
            OwnedPlan( client, {'name': 'Denton Brambles',  'level': 1, 'extra_build_level': 0, 'quantity': 1} ),
            OwnedPlan( client, {'name': 'Geo Thermal Vent', 'level': 1, 'extra_build_level': 0, 'quantity': 1} ),
            OwnedPlan( client, {'name': 'Lapis Forest',     'level': 1, 'extra_build_level': 0, 'quantity': 1} ),
            OwnedPlan( client, {'name': 'Malcud Field',     'level': 1, 'extra_build_level': 0, 'quantity': 1} ),
            OwnedPlan( client, {'name': 'Natural Spring',   'level': 1, 'extra_build_level': 0, 'quantity': 1} ),
            OwnedPlan( client, {'name': 'Volcano',          'level': 1, 'extra_build_level': 0, 'quantity': 1} ),
        ]
        super().__init__( client, price, plans );

class StorageKit( StarterKit ):
    def __init__( self, client, price:float = 0.1 ):
        plans = [
            OwnedPlan( client, {'name': 'Interdimensional Rift',    'level': 1, 'extra_build_level': 0, 'quantity': 1} ),
            OwnedPlan( client, {'name': 'Ravine',                   'level': 1, 'extra_build_level': 0, 'quantity': 1} ),
        ]
        super().__init__( client, price, plans );

class MilitaryKit( StarterKit ):
    """ These aren't all necessarily military, but have some relation to either 
    offense or defense.
    """
    def __init__( self, client, price:float = 0.1 ):
        plans = [
            OwnedPlan( client, {'name': 'Citadel of Knope',     'level': 1, 'extra_build_level': 0, 'quantity': 1} ),
            OwnedPlan( client, {'name': 'Crashed Ship Site',    'level': 1, 'extra_build_level': 0, 'quantity': 1} ),
            OwnedPlan( client, {'name': "Gratch's Gauntlet",    'level': 1, 'extra_build_level': 0, 'quantity': 1} ),
            OwnedPlan( client, {'name': 'Kalavian Ruins',       'level': 1, 'extra_build_level': 0, 'quantity': 1} ),
        ]
        super().__init__( client, price, plans );

class UtilityKit( StarterKit ):
    def __init__( self, client, price:float = 0.1 ):
        plans = [
            OwnedPlan( client, {'name': 'Black Hole Generator',     'level': 1, 'extra_build_level': 0, 'quantity': 1} ),
            OwnedPlan( client, {'name': 'Library of Jith',          'level': 1, 'extra_build_level': 0, 'quantity': 1} ),
            OwnedPlan( client, {'name': 'Oracle of Anid',           'level': 1, 'extra_build_level': 0, 'quantity': 1} ),
            OwnedPlan( client, {'name': 'Pantheon of Hagness',      'level': 1, 'extra_build_level': 0, 'quantity': 1} ),
            OwnedPlan( client, {'name': 'Temple of the Drajilites', 'level': 1, 'extra_build_level': 0, 'quantity': 1} ),
        ]
        super().__init__( client, price, plans );

class BeachKit( StarterKit ):
    def __init__( self, client, price:float = 0.1 ):
        plans = [
            OwnedPlan( client, {'name': 'Beach [1]',    'level': 1, 'extra_build_level': 0, 'quantity': 1} ),
            OwnedPlan( client, {'name': 'Beach [2]',    'level': 1, 'extra_build_level': 0, 'quantity': 1} ),
            OwnedPlan( client, {'name': 'Beach [3]',    'level': 1, 'extra_build_level': 0, 'quantity': 1} ),
            OwnedPlan( client, {'name': 'Beach [4]',    'level': 1, 'extra_build_level': 0, 'quantity': 1} ),
            OwnedPlan( client, {'name': 'Beach [5]',    'level': 1, 'extra_build_level': 0, 'quantity': 1} ),
            OwnedPlan( client, {'name': 'Beach [6]',    'level': 1, 'extra_build_level': 0, 'quantity': 1} ),
            OwnedPlan( client, {'name': 'Beach [7]',    'level': 1, 'extra_build_level': 0, 'quantity': 1} ),
            OwnedPlan( client, {'name': 'Beach [8]',    'level': 1, 'extra_build_level': 0, 'quantity': 1} ),
            OwnedPlan( client, {'name': 'Beach [9]',    'level': 1, 'extra_build_level': 0, 'quantity': 1} ),
            OwnedPlan( client, {'name': 'Beach [10]',   'level': 1, 'extra_build_level': 0, 'quantity': 1} ),
            OwnedPlan( client, {'name': 'Beach [11]',   'level': 1, 'extra_build_level': 0, 'quantity': 1} ),
            OwnedPlan( client, {'name': 'Beach [12]',   'level': 1, 'extra_build_level': 0, 'quantity': 1} ),
            OwnedPlan( client, {'name': 'Beach [13]',   'level': 1, 'extra_build_level': 0, 'quantity': 1} ),
        ]
        super().__init__( client, price, plans );

class DecoKit( StarterKit ):
    def __init__( self, client, price:float = 0.1 ):
        plans = [
            OwnedPlan( client, {'name': 'Crater',               'level': 1, 'extra_build_level': 0, 'quantity': 1} ),
            OwnedPlan( client, {'name': 'Grove of Trees',       'level': 1, 'extra_build_level': 0, 'quantity': 1} ),
            OwnedPlan( client, {'name': 'Lagoon',               'level': 1, 'extra_build_level': 0, 'quantity': 1} ),
            OwnedPlan( client, {'name': 'Lake',                 'level': 1, 'extra_build_level': 0, 'quantity': 1} ),
            OwnedPlan( client, {'name': 'Patch of Sand',        'level': 1, 'extra_build_level': 0, 'quantity': 1} ),
            OwnedPlan( client, {'name': 'Rocky Outcropping',    'level': 1, 'extra_build_level': 0, 'quantity': 1} ),
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

class PrettyKit( ComboKit ):
    """ A combination of BeachKit and DecoKit
    """
    def __init__( self, client, price:float = 0.1 ):
        super().__init__( [BeachKit(client), DecoKit(client)], 0.1 )

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

class CustomKit( StarterKit ):
    """ A kit defined by the user.

    Arguments:
        - derived_from -- Optional, any other kit class.  If sent, your custom 
          kit will start out containing the same plans as are found in that 
          other kit class.  From there, you can add or remove plans as needed.
        - price -- Optional float.
    """
    def __init__( self, client, derived_from:StarterKit = '', price:float = 0.1 ):
        plans = derived_from.plans if derived_from else []
        super().__init__(client, price, plans)

class PostStarterKit(lacuna.binutils.libbin.Script):
    """ Post a starter/noob kit to either the TM or SST.
    """

    def __init__( self ):
        self.version = '0.1'
        parser = argparse.ArgumentParser(
            description = 'Posts one of several starter kits to either the Trade Ministry or the SST on a specific planet.  See the online documentation for a list of the different types of kits available.',
            epilog      = "Full docs can be found at http://tmtowtdi.github.io/MontyLacuna/scripts/post_starter_kit.html",
        )
        parser.add_argument( 'name', 
            metavar     = '<planet>',
            action      = 'store',
            help        = "Post a kit from this planet."
        )
        parser.add_argument( '--kit', 
            metavar     = '<name>',
            action      = 'store',
            choices     = [
                            'resources', 'resource', 'res',
                            'storage', 'store', 'stor',
                            'military', 'mil',
                            'utility', 'util', 'ute',
                            'decoration', 'deco',
                            'beach',
                            'pretty',
                            'fullbasic', 'full_basic', 'full',
                            'big',
                            'halls10',  'hall10',  'h10',
                            'halls100', 'hall100', 'h100',
                          ],
            help        = "Which kit should we post?  If you omit this option, you MUST define a custom kit per the docs.  Choices are 'res', 'stor', 'mil', 'ute', 'deco', 'beach', 'pretty', 'full', 'big', 'h10', 'h100'.  See the online documentation for full explanations of each."
        )
        parser.add_argument( '--ebl', 
            metavar     = '<extra build level>',
            action      = 'store',
            help        = "Do you want your plans to include an extra build level (the 'x' in a '1+x' plan)?  Most kits use no extra build level (1+0) by default."
        )
        parser.add_argument( '--price', 
            metavar     = '<price>',
            action      = 'store',
            type        = float,
            default     = 0.1,
            help        = "How much should we charge for your kit?  Defaults to 0.1."
        )
        parser.add_argument( '-sst', '--sst', 
            action      = 'store_true',
            help        = "By default, we post kits to the Trade Ministry.  If you pass this argument, we'll post to the SST instead.  CAUTION you will be charged 1 E per kit posted for using this option."
        )
        super().__init__(parser)

        ### Both are set by validate_plans()
        self.plan_size = 0
        self.type_translator = {}

        ### If the user requested a pre-rolled named kit using command-line 
        ### args, set it here.  If not, it'll need to be set programmatically 
        ### by the calling script.
        self._set_kit_from_args()

        if self.args.ebl:
            self.kit.update_all_levels( self.args.ebl )

        self._set_planet()
        self._set_trade_building()

    def _set_kit_from_args( self ):
        if not self.args.kit:
            return

        m_bea   = re.compile("^bea", re.I)
        m_big   = re.compile("^big", re.I)
        m_dec   = re.compile("^dec", re.I)
        m_ful   = re.compile("^ful", re.I)
        m_mil   = re.compile("^mil", re.I)
        m_pre   = re.compile("^pre", re.I)
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
        elif m_pre.match(self.args.kit):
            self.kit = PrettyKit( self.client, self.args.price )
        elif m_ful.match(self.args.kit):
            self.kit = FullBasicKit( self.client, self.args.price )
        elif m_big.match(self.args.kit):
            self.kit = BigKit( self.client, self.args.price )
        elif m_h10.match(self.args.kit):
            self.kit = Halls10Kit( self.client, self.args.price )
        elif m_h100.match(self.args.kit):
            self.kit = Halls100Kit( self.client, self.args.price )

    def _set_planet( self ):
        self.client.cache_on( 'my_colonies', 3600 )
        self.planet = self.client.get_body_byname( self.args.name )
        self.client.cache_off()

    def _set_trade_building( self ):
        """ Sets self.trade to either a trade ministry or SST object, depending 
        on what the user asked for.
        """
        if self.args.sst:
            self.trade = self.planet.get_buildings_bytype( 'transporter', 1, 1, 100 )[0]
        else:
            self.trade = self.planet.get_buildings_bytype( 'trade', 1, 1, 100 )[0]

    def post_kit(self):
        """ Posts the chosen kit to the chosen trade building.
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
                        self.kit.price,
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
        return self.trade.add_to_market( offer, self.kit.price )

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
                    'level':                1,
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
        """ Checks that you have on-hand the plans required by the 
        current kit.

        Raises :class:`lacuna.exceptions.MissingResourceError` if your kit 
        requires a plan you haven't got in stock or if you haven't set up a kit 
        yet.
        """
        if not hasattr(self, 'kit'):
            raise err.MissingResourceError("No kit has been set to validate.")

        def getkey(plan):
            ebl = plan.extra_build_level if plan.extra_build_level else 0
            key = plan.name + ':' + str(ebl)
            return key

        plans, self.plan_size = self.trade.get_plan_summary()
        gotplans = {}
        for p in plans:
            self.type_translator[ p.name ] = p.plan_type
            key = getkey(p)
            gotplans[ key ] = 1
        for p in self.kit.plans:
            key = getkey(p)
            if not key in gotplans:
                raise err.MissingResourceError("Your kit requires a 1+{} {} plan, but you don't have one on hand."
                    .format(p.extra_build_level, p.name)
                )
        return True


