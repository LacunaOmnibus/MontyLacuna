
import lacuna.bc
import lacuna.building
import lacuna.spy
import lacuna.trading

class mercenariesguild(lacuna.building.MyBuilding):
    path = 'mercenariesguild'

    def __init__( self, client, body_id:int = 0, building_id:int = 0 ):
        super().__init__( client, body_id, building_id )

    @lacuna.building.MyBuilding.call_returning_meth
    def view_market( self, page_number:int = 1, *args, **kwargs ):
        """ Displays a page of trades, up to 25 trades per page.

        Arguments:
            - page_number -- Integer page number to view.  Defaults to 1.

        Returns a tuple:
            - trades -- List of lacuna.trading.MercTrade objects
            - trade_count -- Integer total number of trades.  This is not the 
              number of trades on the current page; this is the total number of 
              trades available across all pages.
            - page_number -- Integer number of the page you're currently viewing.

        - :class:`lacuna.trading.MercTrade`
        """
        mylist = []
        for i in kwargs['rslt']['trades']:
            mylist.append( lacuna.trading.MercTrade(self.client, i) )
        return(
            mylist,
            self.get_type(kwargs['rslt']['trade_count']),
            self.get_type(kwargs['rslt']['page_number']),
        )
        pass

    @lacuna.bc.LacunaObject.set_empire_status
    @lacuna.building.MyBuilding.call_building_meth
    def accept_from_market( self, trade_id:int, *args, **kwargs ):
        """ Accept (purchase) a trade from the market.

        Arguments:
            - trade_id -- Integer ID of the trade to accept.

        Requires captcha.

        Raises :class:`lacuna.exceptions.ServerError` 1009 if your Intelligence 
        Ministry already has the maximum number of spies it can hold.
        """
        pass

    @lacuna.building.MyBuilding.call_returning_meth
    def get_spies( self, *args, **kwargs ):
        """ Gets a list of your spies that are available to be added as trades.

        Returns a list of :class:`lacuna.spy.Merc` objects.
        """
        ### The TLE docu says it also returns 'cargo_space_used_each', but I'm 
        ### not getting that back in rslt at all.  A spy should take up 350 
        ### units of cargo space (but again, that's from TLE docu.)
        mylist = []
        for i in kwargs['rslt']['spies']:
            mylist.append( lacuna.spy.Merc(self.client, i) )
        return mylist

    @lacuna.building.MyBuilding.call_returning_meth
    def get_trade_ships( self, target_body_id:int = 0, *args, **kwargs ):
        """ Returns a list of ships currently onsite that can be used to add a
        mercenary trade.

        Arguments:
            - target_body_id -- Optional integer ID of the body we plan to send 
              the trade to.

        If ``target_body_id`` is included, the trade ships returned will include 
        ``estimated_travel_time``, the number of seconds the trip will take.  If 
        ``target_body_id`` is not passed in, then the ``estimated_travel_time`` 
        attribute of  the returned objects will be "unknown".

        Returns a list of :class:`lacuna.ship.TradeableShip` objects.

        The only ship type acceptable for adding mercenary trades is a spy pod, 
        so those are the only ships that will be included in the returned list.
        """
        mylist = []
        for i in kwargs['rslt']['ships']:
            mylist.append( lacuna.ship.TradeableShip(self.client, i) )
        return mylist

    @lacuna.building.MyBuilding.call_returning_meth
    def add_to_market( self, spy_id:int, ask:float, ship_id:int = 0, *args, **kwargs ):
        """ Adds a spy to the mercs market.

        Arguments:
            - spy_id  -- Required  - Integer ID of the spy to add.
            - ask     -- Required  - Integer amount of E to charge.  Between 1-99
            - ship_id -- Optional  - Integer ID of the ship to use for the 
              trade.  Obtainable via :py:meth:`get_trade_ships`.  If not sent, a 
              trade ship will be chosen for you if one is available.  This must 
              be the ID of a spy pod.

        Returns the integer ID of the trade you just created.

        Raises :class:`lacuna.exceptions.ServerError` 1011 if you do not have 
        any spy pods available.
        """
        return self.get_type(kwargs['rslt']['trade_id'])

    @lacuna.building.MyBuilding.call_returning_meth
    def view_my_market( self, page_number:int = 1, *args, **kwargs ):
        """ Shows the trades you have offered.

        Arguments:
            - page_number -- Integer page number to view.  Defaults to 1.

        Returns a tuple:
            - trades -- List of lacuna.trading.ExistingTrade objects
            - trade_count -- Integer total number of trades you have on the market.
            - page_number -- Integer page number you're looking at.  Will only be greater than 1 if you have more than 25 trades.

        - :class:`lacuna.trading.ExistingTrade`
        """
        mylist = []
        for i in kwargs['rslt']['trades']:
            mylist.append( lacuna.trading.ExistingTrade(self.client, i) )
        return(
            mylist,
            self.get_type(kwargs['rslt']['trade_count']),
            self.get_type(kwargs['rslt']['page_number']),
        )
        pass

    @lacuna.bc.LacunaObject.set_empire_status
    @lacuna.building.MyBuilding.call_building_meth
    def withdraw_from_market( self, trade_id:int, *args, **kwargs ):
        """ Removes one of your trades from the market.

        Arguments:
            - trade_id -- Integer ID of the trade to withdraw.

        """
        pass

    @lacuna.building.MyBuilding.call_building_meth
    def report_abuse( self, trade_id:int, *args, **kwargs ):
        """ Reports a trade for abuse.

        Arguments:
            - trade_id -- Integer ID of the trade to report.

        What's done with these reports is not documented.

        The TLE API docu says this returns a dict containing a normal ``status`` 
        key, but in practice, on PT at least, it's returning just an empty 
        string.
        """
        pass

