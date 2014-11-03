
import lacuna.bc
import lacuna.building
import lacuna.empire

class libraryofjith(lacuna.building.MyBuilding):
    path = 'libraryofjith'

    def __init__( self, client, body_id:int = 0, building_id:int = 0 ):
        super().__init__( client, body_id, building_id )


    @lacuna.building.MyBuilding.call_returning_meth
    def research_species( self, empire_id:int, *args, **kwargs ):
        """ Returns information on the species of the indicated empire.

        Returns a lacuna.empire.Species object.
        """
        species = lacuna.empire.Species(self.client, kwargs['rslt']['species'])
        return species
