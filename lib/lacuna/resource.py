
import re
import lacuna.bc

class PlanetaryResource():
    """ Base class for resource classes """
    def __init__( self, client, mydict:dict, *args, **kwargs ):
        self.client = client
        self.avail_list = []
        for k, v in mydict.items():
            setattr(self, k, v)
            type_match = re.search("^(\w+)_hour", k)
            if type_match:
                self.avail_list.append( type_match.group(1) )

        self.avail_list.sort()

class PlanetaryFood(PlanetaryResource):
    """ The food being produced and currently stored.

    Attributes:
        algae_hour      24,
        algae_stored    322,
        bean_hour       1,
        bean_stored     2,
        ...
        avail_list      List (sorted) of all available foods on the planet:
                        [ algae, bean, ... ]
    """

class PlanetaryOre(PlanetaryResource):
    """ The ore being produced and currently stored.

    Attributes:
        anthracite_hour     24,
        anthracite_stored   322,
        bauxite_hour        1,
        bauxite_stored      2,
        ...
        avail_list      List (sorted) of all available ores on the planet:
                        [ anthracite, bauxite, ... ]
    """

class StoredResources(PlanetaryResource):
    """ The resources stored on this planet.

    Attributes:
        water:      100,
        anthracite: 200,
        bauxite:    300,
        ...
    """




