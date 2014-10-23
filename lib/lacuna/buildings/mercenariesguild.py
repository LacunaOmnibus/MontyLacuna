
from lacuna.bc import LacunaObject
from lacuna.building import Building

class mercenariesguild(Building):
    path = 'mercenariesguild'

    def __init__( self, client, body_id:int = 0, building_id:int = 0 ):
        super().__init__( client, body_id, building_id )

    @LacunaObject.set_empire_status
    @Building.call_building_meth
    def view_market( self, page_number:int = 1, *args, **kwargs ):
        """ Displays a page of trades, up to 25 trades per page.

        Retval includes:
            "trade_count":  Integer total number of trades.  This is not the
                            number of trades on the current page; this is the
                            TOTAL number of trades available across all pages.
            "page_number":  Integer number of the page you're currently viewing.
            "trades":       List of trade dicts:
                    {
                        "date_offered" : "01 31 2010 13:09:05 +0600",
                        "id" : "id-goes-here",
                        "ask" : 25,     # essentia
                        "offer" : [
                            "Level 9 spy named Jack Bauer (Mercenary Transport) Offense: 875, Defense: 875, Intel: 2, Mayhem: 0, Politics: 0, Theft: 0, Mission Count Offensive: 0 Defensive: 2)",
                        ],
                        "body" : {
                            "id" : "id-goes-here"         # use with get_trade_ships() to determine travel time
                        },
                        "empire" : {
                            "id" : "id-goes-here",
                            "name" : "Earthlings"
                        }
                    },
        """
        pass

    @LacunaObject.set_empire_status
    @Building.call_building_meth
    def accept_from_market( self, trade_id:int, *args, **kwargs ):
        """ Accept (purchase) a trade from the market.

        Requires captcha.
        """
        pass

    @LacunaObject.set_empire_status
    @Building.call_building_meth
    def get_spies( self, *args, **kwargs ):
        """ Gets a list of your spies that are available to be added as trades.

        Retval includes 'spies', a list of dicts:
                [
                    {
                        "id" : "id-goes-here",
                        "name" : "Jack Bauer",
                        "level" : "9"
                    },
                    ...
                ],
        """
        pass

    @LacunaObject.set_empire_status
    @Building.call_building_meth
    def get_trade_ships( self, *args, **kwargs ):
        """ Returns a list of ships currently onsite that can be used to add a
        mercenary trade.

        The only ship type acceptable for adding mercenary trades is a spy pod.

        Retval includes 'ships', a list of dicts:
                {
                "id" : "id-goes-here",
                "type" : "spy_pod",
                "name" : "Spy Pod 5",
                "estimated_travel_time" : 3600, # in seconds, one way
                ...
                },
        """
        pass

    @LacunaObject.set_empire_status
    @Building.call_building_meth
    def add_to_market( self, spy_id:int, ask:float, ship_id:int = 0, *args, **kwargs ):
        """ Adds a spy to the mercs market.

        Arguments:
            spy_id  - Required  - Integer ID of the spy to add.
            ask     - Required  - Integer amount of E to charge.  Between 1-99
            ship_id - Optional  - Integer ID of the ship to use for the trade.
                                  Obtainable via get_trade_ships().  If not 
                                  sent, a trade ship will be chosen for you if 
                                  one is available.
                                  This must be the ID of a spy pod.

        Retval includes key 'trade_id', the integer ID of the trade you just
        created.

        Raises ServerError 1011 if you do not have any spy pods available.
        """
        pass

    @LacunaObject.set_empire_status
    @Building.call_building_meth
    def view_my_market( self, page_number:int = 1, *args, **kwargs ):
        """ Shows the trades you have offered.

        Retval includes:
            "page_number":  Integer page number you're looking at.  Will only be 
                            greater than 1 if you have more than 25 trades.
            "trade_count":  Integer total number of trades you have on the market.
            "trades":       List of dicts:
                    {
                        "date_offered" : "01 31 2010 13:09:05 +0600",
                        "id" : "id-goes-here",
                        "ask" : 25,     # essentia
                        "offer" : [
                            "Level 9 spy named Jack Bauer (Mercenary Transport) Offense: 875, Defense: 875, Intel: 2, Mayhem: 0, Politics: 0, Theft: 0, Mission Count Offensive: 0 Defensive: 2)",
                        ]
                    },
        """
        pass

    @LacunaObject.set_empire_status
    @Building.call_building_meth
    def withdraw_from_market( self, trade_id:int, *args, **kwargs ):
        """ Removes one of your trades from the market."""
        pass


