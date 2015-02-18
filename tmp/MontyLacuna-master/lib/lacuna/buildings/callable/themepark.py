
import lacuna.bc
import lacuna.building

class themepark(lacuna.building.MyBuilding):
    path = 'themepark'

    def __init__( self, client, body_id:int = 0, building_id:int = 0 ):
        super().__init__( client, body_id, building_id )

    @lacuna.building.MyBuilding.call_returning_meth
    def view( self, *args, **kwargs ):
        """ Get details about the park and whether it can be operated or not.

        Returns a :class:`ParkView` object for this Theme Park.
        """
        lacuna.building.MyBuilding._write_building_status( self, kwargs['rslt'] )
        view = ParkView( self.client, kwargs['rslt']['themepark'] )
        return view

    @lacuna.building.MyBuilding.call_returning_meth
    def operate( self, *args, **kwargs ):
        """ Runs the theme park.

        Requires at least 1000 of each of 5 distinct food types to start a 
        non-running theme park for one hour.  Returns happiness - the more 
        distinct food types you have, and the higher the level of the park, 
        the more happiness is returned.

        Once the theme park has already started running, you may call 
        :meth:`operate` again.  This will extend the length of operation by 
        another hour, returning the appropriate happiness.  But for the >= 2nd 
        operation, you must have at least as much food on hand as you had the 
        first time you started the park.  The :class:`ParkView` object's 
        ``food_type_count`` attribute will tell you how many food types are 
        required to extend operations.

        Returns a :class:`ParkView` object.
        """
        lacuna.building.MyBuilding._write_building_status( self, kwargs['rslt'] )
        view = ParkView( self.client, kwargs['rslt']['themepark'] )
        return view

class ParkView(lacuna.bc.SubClass):
    """
    Attributes::

        can_operate         1 or 0
        reason              [   1011,
                                "This Theme Park was started with 12 types of 
                                food so you need at least 12 types of food to 
                                continue its operation."    ]
        food_type_count     Integer number of food types required to extend
                            operations.

        "reason" will only be set if "can_operate" is 0.

        "food_type_count" will be the integer number of food types required 
        (at least 500 of each) to extend operations by another hour.  If the 
        park is not currently in operation, this will be 5.

    """
    def __init__( self, client, mydict:dict, *args, **kwargs ):
        super().__init__(client, mydict)
        if not hasattr(self, 'food_type_count'):
            ### If the park isn't currently in operation, we don't actually 
            ### get a food_type_count key in the hash returned from TLE at 
            ### all.  Force it to the minimum number of food types required to 
            ### start a currently-non-running park.
            self.food_type_count = 5

