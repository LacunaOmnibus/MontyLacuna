

from lacuna.bc import LacunaObject
from lacuna.trading import TradeBldg
from lacuna.ship import TravellingShip

class transporter(TradeBldg):
    """
        As noted in trade.py, copying every method that's never going to be used 
        is getting old, so I'm skipping the following:

        - trade_one_for_one()
        - report_abuse()
    """

    path = 'transporter'

    def __init__( self, client, body_id:int = 0, building_id:int = 0 ):
        super().__init__( client, body_id, building_id )

    @TradeBldg.call_returning_meth
    def view( self, *args, **kwargs ):
        """ The only building-specific bit of data in the SST's view() call 
        is the integer maximum number of items this SST can support in a single 
        trade.

        So this view() call returns that single integer.
        """
        TradeBldg.write_building_status( self, kwargs['rslt'] )
        return kwargs['rslt']['transport']['max']

    @TradeBldg.call_returning_meth
    def add_to_market( self, offer:dict, ask:int, *args, **kwargs ):
        """ Spends 1 E to add a trade to the SST market.

        The only difference between this and trade.add_trade() is that the SST 
        has no 'options' argument.

        Arguments::

            offer       List of dicts of items to offer for trade.  See below for
                        more details.
                            {   'type':         'bauxite',
                                'quantity':     10000   },
            ask         Integer price in E you're asking for this trade, between 
                        0.1 and 100.

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
        return kwargs['rslt']['trade_id']

    @LacunaObject.set_empire_status
    @TradeBldg.call_building_meth
    def push_items( self, target_id:int, items:list, *args, **kwargs ):
        """ Pushes items to another of your planets.  The target planet must 
        also have an SST built (though its level doesn't matter).

        Arguments:
            - target_id -- Integer ID of the body to send resources to.
            - items -- List of item dicts.  See add_to_market().

        Returns a single TravellingShip object.
        """

