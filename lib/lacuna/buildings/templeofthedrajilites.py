
from lacuna.bc import LacunaObject
from lacuna.building import Building

class templeofthedrajilites(Building):
    path = 'templeofthedrajilites'

    def __init__( self, client, body_id:int = 0, building_id:int = 0 ):
        super().__init__( client, body_id, building_id )

    @LacunaObject.set_empire_status
    @Building.call_building_meth
    def list_planets( self, star_id:int = 0, *args, **kwargs ):
        """ List planets around a given star.

        Arguments:
            star_id     Optional integer ID of a star.  Defaults to the star 
                        that the temple is orbiting.

        Retval includes key 'planets', a list of planet dicts:
            {'id': '12345', 'name': 'Earth'}
        """
        pass

    @LacunaObject.set_empire_status
    @Building.call_building_meth
    def view_planet( self, planet_id:int, *args, **kwargs ):
        """ View the surface of a specific planet.

        Arguments:
            planet_id   Required integer ID of a planet to view.

        Retval includes key 'map':
            'surface_image':    "surface-p12",
            'buildings':        List of building dicts:
                                {   "x":        1,
                                    "y":        -10,
                                    "image":    "rockyoutcrop1"     }
        """
        pass

