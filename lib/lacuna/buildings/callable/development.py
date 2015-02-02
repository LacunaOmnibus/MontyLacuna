
import lacuna.building

class development(lacuna.building.MyBuilding):
    path = 'development'

    def __init__( self, client, body_id:int = 0, building_id:int = 0 ):
        super().__init__( client, body_id, building_id )

    @lacuna.building.MyBuilding.call_returning_meth
    def subsidize_build_queue( self, **kwargs ):
        """ Spends E to immediately finish all buildings currently in the 
        build queue.

        Unlike subsidize_one_build() below, this method will ALWAYS spend at 
        least 1 E.  Even if your build queue is empty, 1 E will be spent.  So 
        be careful.

        Returns
            - essentia_spent -- Integer cost of subsidy
        """
        return self.get_type(kwargs['rslt']['essentia_spent'])

    @lacuna.building.MyBuilding.call_named_returning_meth
    def subsidize_one_build( self, named_args:dict, **kwargs ):
        """ Spends E to immediately finish a single build in the build queue.

        Arguments:
            - named_args -- Dict containing the ID of the building in the queue
              whose build you want to cancel. ``{ 'scheduled_id': 12345 }``

        It's usually cheaper per building to subsidize the entire build queue 
        than to subsidize a single building.  So if your build queue only 
        contains a single building being upgraded, call build_queue() instead 
        of subsidize_one_build().

        Returns
            - essentia_spent -- Integer cost of subsidy

        Raises :class:`lacuna.exceptions.ServerError` 1000 if the specified 
        building is not currently being built or upgraded.
        """
        return self.get_type(kwargs['rslt']['essentia_spent'])

    @lacuna.building.MyBuilding.call_named_returning_meth
    def cancel_build( self, named_args:dict, **kwargs ):
        """ Removes a single building upgrade from the build queue.
        Any resources that were spent to start the upgrade are lost.

        Arguments:
            - named_args -- Dict containing the ID of the building in the queue
              whose build you want to cancel. ``{ 'scheduled_id': 12345 }``

        Returns a tuple:
            - build_queue -- list of lacuna.building.InBuildQueue objects
            - subsidy_cost -- integer cost to subsidize the entire remaining build queue, now that this building's upgrade has been cancelled.
        """
        mylist = []
        for i in kwargs['rslt']['build_queue']:
            mylist.append( lacuna.building.InBuildQueue(i) )
        return(
            mylist,
            self.get_type(kwargs['rslt']['subsidy_cost'])
        )

