
import lacuna.bc
import lacuna.building
import lacuna.ship
import lacuna.spy
import lacuna.plan
import lacuna.glyph


class TradeBldg(lacuna.building.MyBuilding):
    """ Base class for trade and transporter buildings.  """

    def __init__( self, client, body_id:int = 0, building_id:int = 0 ):
        super().__init__( client, body_id, building_id )

    @lacuna.building.MyBuilding.call_returning_meth
    def get_ships( self, *args, **kwargs ):
        """ Get ships available to be added to a trade as merchandise.

        These are *not* ships available to carry trade cargo.  These are ships 
        that are available *as* cargo - these ships can be traded, but can't 
        necessarily carry a trade.

        Returns a tuple:
            - ships -- List of :class:`lacuna.ship.TradeableShip` objects.
            - space_used -- Amount of cargo space used by each ship.  Always 
              10000.
        """
        mylist = []
        for i in kwargs['rslt']['ships']:
            mylist.append( lacuna.ship.TradeableShip(self.client, i) )
        return(
            mylist,
            self.get_type(kwargs['rslt']['cargo_space_used_each'])
        )

    @lacuna.building.MyBuilding.call_returning_meth
    def get_prisoners( self, *args, **kwargs ):
        """ Get prisoners available to be added to a trade as merchandise.

        Returns a tuple:
            - prisoners -- List of :class:`lacuna.spy.Prisoner` objects.
            - space_used -- Amount of cargo space used by each prisoner.  
              Always 350.
        """
        mylist = []
        for i in kwargs['rslt']['prisoners']:
            mylist.append( lacuna.spy.Prisoner(self.client, i) )
        return(
            mylist,
            self.get_type(kwargs['rslt']['cargo_space_used_each'])
        )

    @lacuna.building.MyBuilding.call_returning_meth
    def get_plan_summary( self, *args, **kwargs ):
        """ Get plans available to be added to a trade as merchandise.

        Returns a tuple:
            - plans -- List of :class:`lacuna.plan.OwnedPlan` objects.
            - space_used -- Amount of cargo space used by each prisoner.  
              Always 10000.
        """
        mylist = []
        for i in kwargs['rslt']['plans']:
            mylist.append( lacuna.plan.OwnedPlan(self.client, i) )
        return(
            mylist,
            self.get_type(kwargs['rslt']['cargo_space_used_each'])
        )

    @lacuna.building.MyBuilding.call_returning_meth
    def get_glyph_summary( self, *args, **kwargs ):
        """ Get glyphs available to be added to a trade as merchandise.

        Returns:
            glyphs (tuple):
                - glyphs -- List of :class:`lacuna.glyph.OwnedGlyph` objects.
                - space_used -- Amount of cargo space used by each prisoner.  
                  Always 10000.
        """
        mylist = []
        for i in kwargs['rslt']['glyphs']:
            mylist.append( lacuna.glyph.OwnedGlyph(self.client, i) )
        return(
            mylist,
            self.get_type(kwargs['rslt']['cargo_space_used_each'])
        )

    @lacuna.building.MyBuilding.call_returning_meth
    def view_my_market( self, page_number:int = 1, *args, **kwargs ):
        """ Shows the trades you currently have offered.

        Args:
            page_number (int): page number to view.  25 trades 
                               shown per page.  Defaults to 1. 
        Returns:
            trades_details (tuple):
                - trades -- List of :class:`lacuna.trading.ExistingTrade` objects
                - count -- Total number of trades you have up
                - page_number -- The page that the "trades" list appeared on.  
                  Same value that you passed as an argument, or 1.
        """
        mylist = []
        for i in kwargs['rslt']['trades']:
            mylist.append( ExistingTrade(self.client, i) )
        return(
            mylist,
            self.get_type(kwargs['rslt']['trade_count']),
            self.get_type(kwargs['rslt']['page_number']),
        )

    @lacuna.bc.LacunaObject.set_empire_status
    @lacuna.building.MyBuilding.call_building_meth
    def withdraw_from_market( self, trade_id:int, *args, **kwargs ):
        """ Withdraws one of your trades from the market.  If the trade had been 
        on the SST market, refunds your 1 E posting cost.

        Args:
            trade_id (int): ID of the trade to withdraw
        """
        pass

    @lacuna.building.MyBuilding.call_returning_meth
    def view_market( self, page_number:int = 1, filter:str = '', *args, **kwargs ):
        """ Shows the trades you currently have offered.

        Args:
            page_number (int): page number to view.  25 trades shown per page.  Defaults to 1.
            filter (str): narrow down the types of trades returned.
        Returns:
            trades (tuple):
                - trades -- List of :class:`lacuna.trading.ExistingTrade` objects
                - count -- Total number of trades you have up
                - page_number -- The page that the "trades" list appeared on.  
                  Same value that you passed as an argument, or 1.

        - Valid values for the ``filter`` argument:
            - energy
            - food
            - glyph
            - ore
            - plan
            - prisoner
            - ship
            - waste
            - water 
        """
        mylist = []
        for i in kwargs['rslt']['trades']:
            mylist.append( ExistingTrade(self.client, i) )
        return(
            mylist,
            self.get_type(kwargs['rslt']['trade_count']),
            self.get_type(kwargs['rslt']['page_number']),
        )


    @lacuna.bc.LacunaObject.set_empire_status
    @lacuna.building.MyBuilding.call_building_meth
    def accept_from_market( self, trade_id:int, *args, **kwargs ):
        """ Accepts a trade from the market.  When buying from the SST market, 
        an additional 1 E processing cost is automatically charged in addition
        to the 'ask' price displayed for the trade.

        Requires captcha.

        Requires 'trade_id', integer ID of the trade to purchase.
        """
        pass


    @lacuna.building.MyBuilding.call_returning_meth
    def get_stored_resources( self, *args, **kwargs ):
        """ Get resources stored onsite and available for trading.

        Returns a :class:`lacuna.resource.StoredResources` object.
        """
        return lacuna.resource.StoredResources(self.client, kwargs['rslt']['resources'])


class ExistingTrade(lacuna.bc.SubClass):
    """ Trades that exist on either the Trade or SST market, either posted by 
    you or another empire.

    Object Attributes::

        id              "id-goes-here",
        date_offered    "01 31 2010 13:09:05 +0600",
        ask             25,     # essentia
        offer           List of items
                            [   "Level 21 spy named Jack Bauer (prisoner)",
                                "4,000 bauxite",
                                "gold glyph"     ]
        empire          Info on offering empire.  Will only exist if this is a
                        trade offered by somebody else - your own trades do not
                        include this.
                            {   "id" : "id-goes-here",
                                "name" : "Earthlings"   }
        # These will only be available for trades on the Trade Ministry.  The
        # SST deliveries are instant, so this information doesn't pertain to
        # the SST.
        body            Dict - info on the sending body
                            {   "id" : "id-goes-here" }
        delivery        Dict - info on delivery time (in seconds)
                            {   "duration" : "4600" }
                                    
    """

class MercTrade(lacuna.bc.SubClass):
    """
    Object Attributes::

        origin          :class:`lacuna.mercenariesguild.MercTradeOrigin` object
        date_offered    "01 31 2010 13:09:05 +0600",
        id              "id-goes-here",
        ask             25,                         # essentia cost
        offer           "Level 9 spy named Jack Bauer (Mercenary Transport) 
                        Offense: 875, Defense: 875, Intel: 2, Mayhem: 0, 
                        Politics: 0, Theft: 0, Mission Count Offensive: 0 
                        Defensive: 2)",
        offer_summary   The first 32 characters of self.offer, plus "..."
                        eg "Level 9 spy named Jack Bauer (Me..."
    """
    def __init__(self, client, mydict:dict):
        self.origin = MercTradeOrigin( client, mydict )
        del mydict['body']
        del mydict['empire']

        ### offer is documented as being a list with a single string element.  
        ### I have no idea why it'd be a list with only a single string.  If 
        ### that's really what it is, the join is meaningless, but if it's 
        ### ever more than a single element, the join deals with it.
        self.offer = " ".join(mydict['offer'])
        self.offer_summary = self.offer[0:32] + '...'
        super().__init__(client, mydict)


class MercTradeOrigin(lacuna.bc.SubClass):
    """
    Object Attributes::

        body_id         ID of the sending body
        empire_id       ID of the sending empire
        empire_name     Name of the sending empire
    """
    def __init__(self, client, mydict:dict):
        self.client         = client
        self.body_id        = mydict['body']['id']
        self.empire_id      = mydict['empire']['id']
        self.empire_name    = mydict['empire']['name']

