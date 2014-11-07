
import re
import lacuna.bc

class PlanetaryResource():
    """ Base class for resource classes.

    Attributes:
        all_foods       List of all foods in the game
        all_ores        List of all ores in the game
        all_resources   List of all resources in the game
                        This is a join of all_foods and all_ores, along with 
                        "water" and "energy".
        RES             Amount of RES we have stored up.
        RES_hour        Amount of RES we're producing per hour
                        "anthracite_hour", "wheat_hour", etc

    """
    def __init__( self, client, mydict:dict, *args, **kwargs ):
        self.client = client

        self.all_foods = [
            "algae", "apple", "bean", "beetle", "burger", "bread", "cheese", 
            "chip", "cider", "corn", "fungus", "lapis", "meal", "milk", 
            "pancake", "pie", "potato", "root", "shake", "soup", "syrup",
            "wheat",
        ]
        self.all_ores = [
            "anthracite", "bauxite", "beryl", "chromite", "chalcopyrite",
            "fluorite", "galena", "goethite", "gold", "gypsum", "halite",
            "kerogen", "magnetite", "methane", "monazite", "rutile", "sulfur",
            "trona", "uraninite", "zircon",
        ]
        self.all_resources = self.all_foods + self.all_ores + [ "water", "energy" ]

        ### Iterate through our exhaustive list of all resources instead of 
        ### iterating through mydict, which only lists resources > 0.  This 
        ### way, everything is listed, even if its value is 0.
        for i in self.all_resources:
            ### Sometimes we get "water", and sometimes we get "water_stored".  
            ### It's confusing and inconsistent.  Strip the "_stored".
            if i in mydict:
                setattr( self, i, mydict[i] )
            elif i+"_stored" in mydict:
                setattr( self, i, int(mydict[i+"_stored"]) )
            else:
                setattr( self, i, 0 )

            if i+"_hour" in mydict:
                setattr( self, i+"_hour", int(mydict[i+"_hour"]) )
            else:
                setattr( self, i+"_hour", 0 )

class PlanetaryFood(PlanetaryResource):
    """ The food being produced and currently stored.

    Attributes:
        algae_hour      24,     # amount being produced
        algae           322,    # amount being stored
        bean_hour       1,
        bean            2,
        ...
        avail_list      List (sorted) of all available foods on the planet:
                        [ algae, bean, ... ]
    """

class PlanetaryOre(PlanetaryResource):
    """ The ore being produced and currently stored.

    Attributes:
        anthracite_hour     24,
        anthracite          322,
        bauxite_hour        1,
        bauxite             2,
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

