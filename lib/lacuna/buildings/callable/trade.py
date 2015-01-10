
import lacuna.bc
import lacuna.trading
import lacuna.ship

class trade(lacuna.trading.TradeBldg):
    """ Trade Ministry 

    I'm to the point were replicating every single TLE method is 
    getting boring.

    I'm really doing this to learn Python.  On top of that, I can't see 
    anybody ever wanting to script some of the methods in here, so I'm just 
    not bothering with them.

    - create_supply_chain()
    - delete_supply_chain()
    - update_supply_chain()
    - update_waste_chain()
    - add_supply_ship_to_fleet()
    - add_waste_ship_to_fleet()
    - remove_supply_ship_from_fleet()
    - remove_waste_ship_from_fleet()
    - report_abuse()
    """

    path = 'trade'

    def __init__( self, client, body_id:int = 0, building_id:int = 0 ):
        super().__init__( client, body_id, building_id )

    @lacuna.trading.TradeBldg.call_returning_meth
    def add_to_market( self, offer:dict, ask:int, options:dict = {}, *args, **kwargs ):
        """ Adds a trade to the market.

        Arguments::

            offer       List of dicts of items to offer for trade.  See below for
                        more details.
                            {   'type':         'bauxite',
                                'quantity':     10000   },
            ask         Integer price in E you're asking for this trade, between 
                        0.1 and 100.
            options     Dict of 'options' to modify the trade.  The only option, 
                        which is not an option at all since it's required, is 
                        the ID of the ship you want to use to transport your 
                        trade.
                            { 'ship_id':    12345   }
                        Use get_trade_ships() to find appropriate ship IDs.

        *offer*

        There are five types of items you can offer for trade, each with 
        their own required keys for their offer dicts::

            resources
                {   'type':         'bauxite',
                    'quantity':     10000   },
            glyphs
                {   'type':         'glyph',
                    'name':         'bauxite',
                    'quantity':     10000   },
            plans
                {   'type':                 'plan',
                    'plan_type':            'Permanent_AlgaePond',  # see get_plan_summary()
                    'level':                1,
                    'extra_build_level':    3,                      # If > 1, 'level' must be 1.
                    'quantity':             10000   },
            prisoners
                {   'type':         'prisoner',
                    'prisoner_id':  12345   },
            ships
                {   'type':     'ship',
                    'ship_id':  12345   },

        Returns the ID of the trade just added.
        """
        return self.get_type(kwargs['rslt']['trade_id'])

    @lacuna.trading.TradeBldg.call_returning_meth
    def get_trade_ships( self, target_id:int = 0, *args, **kwargs ):
        """ Returns a list of ships available to be used as trade transports.

        These are *not* ships available to be traded; these are ships that are 
        available to carry trades.

        Arguments
            - target_id -- Optional ID of the target receiving the trade.  If 
              included, the ships' estimated_travel_time attribute will be set.

        Returns a list of :class:`lacuna.ship.TradeTransportShip` objects.
        """
        ship_list = []
        for i in kwargs['rslt']['ships']:
            ship_list.append( lacuna.ship.TradeTransportShip(self.client, i) )
        return ship_list

    @lacuna.trading.TradeBldg.call_returning_meth
    def get_waste_ships( self, target_id:int = 0, *args, **kwargs ):
        """ Returns a list of waste ships either currently on or available for 
        waste disposal duty.

        Returns a list of :class:`lacuna.ship.ChainShip` objects.
        """
        ship_list = []
        for i in kwargs['rslt']['ships']:
            ship_list.append( lacuna.ship.ChainShip(self.client, i) )
        return ship_list

    @lacuna.trading.TradeBldg.call_returning_meth
    def get_supply_ships( self, target_id:int = 0, *args, **kwargs ):
        """ Returns a list of supply ships either currently on or available for 
        supply disposal duty.

        Returns a list of :class:`lacuna.ship.ChainShip` objects.
        """
        ship_list = []
        for i in kwargs['rslt']['ships']:
            ship_list.append( lacuna.ship.ChainShip(self.client, i) )
        return ship_list

    @lacuna.trading.TradeBldg.call_returning_meth
    def view_supply_chains( self, *args, **kwargs ):
        """ Returns a list of SupplyChain objects """
        mylist = []
        for i in kwargs['rslt']['supply_chains']:
            mylist.append( WasteChain(self.client, i) )
        return(
            mylist,
            self.get_type(kwargs['rslt']['max_supply_chains'])
        )

    @lacuna.trading.TradeBldg.call_returning_meth
    def view_waste_chains( self, *args, **kwargs ):
        """ Returns a list of WasteChain objects """
        mylist = []
        for i in kwargs['rslt']['waste_chain']:
            mylist.append( WasteChain(self.client, i) )
        return mylist

    def view_waste_chain( self, *args, **kwargs ):
        """ The actual TLE method is plural, but there's only one waste chain 
        per planet, and the key returned is singular.  So give the user a 
        break and let them call this method with or without the s.
        """
        return self.view_waste_chains()

    @lacuna.trading.TradeBldg.call_returning_meth
    def push_items( self, target_id:int, items:list, options:dict, *args, **kwargs ):
        """ Pushes items to another of your planets.

        Arguments:
            - target_id -- Integer ID of the body to send resources to.
            - items -- List of item dicts.  See add_to_market().
            - options -- Required (not optional) dict.  See add_to_market().

        Returns a single :class:`lacuna.ship.TravellingShip` object.
        """
        return lacuna.ship.TravellingShip(self.client, kwargs['rslt']['ship'])


class Chain(lacuna.bc.SubClass):
    """ Chain base class """
    pass

class SupplyChain(Chain):
    """
    Attributes::

        id                      "id-goes-here",
        body                    {   "id" : "id-goes-here",
                                    "name" : "Mars",
                                    "x" : 0,
                                    "y" : -123,
                                    ...      },
        building_id             1234567,        # ID of the Trade Min.  Yeah I dunno either.
        resource_hour           10000000,
        resource_type           'water',
        percent_transferred     95,
        stalled                 0,
    """

class WasteChain(Chain):
    """
    Attributes::

        id                      "id-goes-here",
        star                    {   "id" : "id-goes-here",
                                    "name" : "Mars",
                                    "x" : 0,
                                    "y" : -123,
                                    ...     },
        waste_hour              10000000,
        percent_transferred     95,
    """

