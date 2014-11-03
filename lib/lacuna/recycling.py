
from lacuna.bc import LacunaObject
from lacuna.building import MyBuilding

class RecycleBldg(MyBuilding):
    """ Base class for waste exchanger and recycler buildings.  """

    def __init__( self, client, body_id:int = 0, building_id:int = 0 ):
        super().__init__( client, body_id, building_id )

    @MyBuilding.call_returning_meth
    def view( self, *args, **kwargs ):
        """ Get ships available to be added to a trade as merchandise.

        Returns a single RecycleJob object.
        """
        return RecycleJob(self.client, kwargs['rslt']['recycle'])
        pass

    @LacunaObject.set_empire_status
    @MyBuilding.call_building_meth
    def recycle( self, water:int = 0, ore:int = 0, energy:int = 0, subsidize:int = 0, *args, **kwargs ):
        """ Convert existing waste into valuable resources.

        Arguments:
            water       Integer amount of waste to convert to water
            ore         Integer amount of waste to convert to ore
            energy      Integer amount of waste to convert to energy
            subsidize   Integer; set to 1 to spend 2 E to convert immediately 
                        (defaults to 0)

        The combined total of water, ore, and energy must be below max_recycle 
        (see view()), and also must be below the total amount of waste 
        currently held on the planet.
        """
        pass

    @LacunaObject.set_empire_status
    @MyBuilding.call_building_meth
    def subsidize_recycling( self, *args, **kwargs ):
        """ Spends 2 E to complete the current recycling job now.
        """
        pass

class RecycleJob():
    """ 
    Attributes:
        seconds_remaining       0,
        can                     1,
        seconds_per_resource    "2.138",    # to precalculate the time recycling will take
        max_recycle             12000,
        water                   0,
        energy                  0,
        ore                     0
    """
    def __init__( self, client, mydict:dict, *args, **kwargs ):
        self.client = client
        for k, v in mydict.items():
            setattr(self, k, v)

