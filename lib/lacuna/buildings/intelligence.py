
from lacuna.bc import LacunaObject
from lacuna.building import MyBuilding
from lacuna.spy import IntelView, MissionResult, Spy

class intelligence(MyBuilding):
    path = 'intelligence'

    def __init__( self, client, body_id:int = 0, building_id:int = 0 ):
        super().__init__( client, body_id, building_id )

    @MyBuilding.call_returning_meth
    def view( self, *args, **kwargs ):
        """ View stats on current spy numbers, as well as costs to train new 
        spies.

        Returns a single IntelView object.
        """
        return IntelView(self.client, kwargs['rslt']['spies'])


    @LacunaObject.set_empire_status
    @MyBuilding.call_building_meth
    def train_spy( self, *args, quantity:int = 1, **kwargs ):
        """ Trains one or more spies.  "Train", in this case, means "create".
        The "quantity" argument defaults to 1.

        Returns a dict including the keys:
            - trained -- Integer number added to the training queue.  Always included in retval, but may be set to 0.
            - not_trained -- Integer number not added to the training queue.  Only appears in retval if its value is non-zero.
            - reason_not_trained -- Dict containing the reason that "not_trained" is set.  Only appears in retval if "not_trained" appears.  Includes:
                - code -- 1011,
                - message -- "Not enough food to train a spy."
        """
        pass

    @MyBuilding.call_returning_meth
    def view_spies( self, page_number:int = 1, *args, **kwargs ):
        """ Returns info on one page (up to 30) spies.  There are a maximum of 
        three pages of spy data.  
        
        To get info on all of your spies at once, see also view_all_spies().

        Returns a list of up to 30 Spy objects.
        """
        spy_list = []
        for i in kwargs['rslt']['spies']:
            spy_list.append( Spy(self.client, i) )
        return spy_list

    @MyBuilding.call_returning_meth
    def view_all_spies( self, *args, **kwargs ):
        """ Returns information on all of the spies controlled from this 
        planet.

        Returns a list of up to 90 Spy objects.
        """
        spy_list = []
        for i in kwargs['rslt']['spies']:
            spy_list.append( Spy(self.client, i) )
        return spy_list

    @LacunaObject.set_empire_status
    @MyBuilding.call_building_meth
    def burn_spy( self, spy_id:int, *args, **kwargs ):
        """ Burns (deletes) an existing spy. """
        pass

    @LacunaObject.set_empire_status
    @MyBuilding.call_building_meth
    def name_spy( self, spy_id:int, name:str, *args, **kwargs ):
        """ Renames an existing spy."""
        pass

    @MyBuilding.call_returning_meth
    def assign_spy( self, spy_id:int, assignment:str, *args, **kwargs ):
        """ Assigns a spy to a task.
        
        Possible assignments for each spy can be found by calling view_spies() 
        or view_all_spies().  A full list of all assignments can be found at 
        https://us1.lacunaexpanse.com/api/Intelligence.html#assignment

        Requires captcha.

        Returns a tuple:
            - spy -- Spy object
            - mission_result -- MissionResult object
        """
        spy     = Spy( self.client, kwargs['rslt']['spy'] )
        rslt    = MissionResult( self.client, kwargs['rslt']['mission'] )
        return( spy, rslt )

    @LacunaObject.set_empire_status
    @MyBuilding.call_building_meth
    def subsidize_training( self, *args, **kwargs ):
        """ Subsidizes training of all spies currently in the queue.

        Costs 1 E per spy.
        """
        pass

