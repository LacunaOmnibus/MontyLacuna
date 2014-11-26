
import re
import lacuna.bc
import lacuna.body

class PlanetaryResource(lacuna.bc.SubClass):
    """ Base class for resource classes.

    Attributes::

        all_foods       List of all foods in the game
        all_ores        List of all ores in the game
        all_resources   List of all resources in the game
                        This is a join of all_foods and all_ores, along with 
                        "water" and "energy".
        RES             Amount of RES we have stored up (eg "wheat")
        RES_hour        Amount of RES we're producing per hour
                        (eg "wheat_hour")

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
        self.all_resources = self.all_foods + self.all_ores + [ "water", "energy", "waste" ]

        ### Iterate through our exhaustive list of all resources instead of 
        ### iterating through mydict, which only lists resources > 0.  This 
        ### way, everything is listed, even if its value is 0.
        for i in self.all_resources:
            ### Sometimes we get "water", and sometimes we get "water_stored".  
            ### It's confusing and inconsistent.  Strip the "_stored".
            if i in mydict:
                setattr( self, i, int(mydict[i]) )
            elif i+"_stored" in mydict:
                setattr( self, i, int(mydict[i+"_stored"]) )
            else:
                setattr( self, i, 0 )

            if i+"_hour" in mydict:
                setattr( self, i+"_hour", int(mydict[i+"_hour"]) )
            else:
                setattr( self, i+"_hour", 0 )


    def my_ores(self):
        """ Generator.  Iterate through all of the ores in the current object:

        >>> ores = <PlanetaryOre object>
        >>> for name, quantity in ores.my_ores():
        >>>     print( "name: {}, quantity: {:,}".format(name, quantity) )
        name: anthracite, quantity: 1,200
        (no bauxite on this planet, so it's not listed)
        name: beryl, quantity: 2,200
        ...
        """
        for i in self.all_ores:
            if hasattr(self, i):
                yield(i, eval('self.'+i))


    def my_foods(self):
        """ Generator.  Iterate through all of the foods in the current object:

        >>> foods = <PlanetaryFood object>
        >>> for name, quantity in foods.my_foods():
        >>>     print( "name: {}, quantity: {:,}".format(name, quantity) )
        name: algae, quantity: 1,200
        (no apple on this planet, so it's not listed)
        name: bean, quantity: 2,200
        ...
        """
        for i in self.all_foods:
            if hasattr(self, i):
                yield(i, eval('self.'+i))


    def my_hourly_ores(self):
        """ Generator.  Iterate through all of the hourly rates of ore 
        production in the current object:

        >>> ores = <PlanetaryOre object>
        >>> for name, quantity in ores.my_hourly_ores():
        >>>     print( "name: {}, quantity: {:,}".format(name, quantity) )
        name: anthracite_hour, quantity: 1,200
        (no bauxite production on this planet, so it's not listed)
        name: beryl_hour, quantity: 2,200
        ...
        """
        for i in self.all_ores:
            attr = i+"_hour"
            if hasattr(self, attr):
                yield(i, eval('self.'+attr))


    def my_hourly_foods(self):
        """ Generator.  Iterate through all of the hourly rates of food 
        production in the current object:

        >>> foods = <PlanetaryFood object>
        >>> for name, quantity in foods.my_hourly_foods():
        >>>     print( "name: {}, quantity: {:,}".format(name, quantity) )
        name: algae_hour, quantity: 1,200
        (no apple production on this planet, so it's not listed)
        name: bean_hour, quantity: 2,200
        ...
        """
        for i in self.all_foods:
            attr = i+"_hour"
            if hasattr(self, attr):
                yield(i, eval('self.'+attr))

class PlanetaryFood(PlanetaryResource):
    """ The food being produced and currently stored.

    Attributes::

        algae_hour      24,     # amount being produced
        algae           322,    # amount being stored
        bean_hour       1,
        bean            2,
            ...etc...
        avail_list      List (sorted) of all available foods on the planet:
                        [ algae, bean, ... ]
    """

class PlanetaryOre(PlanetaryResource):
    """ The ore being produced and currently stored.

    Attributes::

        anthracite_hour     24,
        anthracite          322,
        bauxite_hour        1,
        bauxite             2,
            ...etc...
        avail_list      List (sorted) of all available ores on the planet:
                        [ anthracite, bauxite, ... ]
    """

class StoredResources(PlanetaryResource):
    """ The resources stored on this planet.

    Attributes::

        water:      100,
        anthracite: 200,
        bauxite:    300,
        etc
    """

class AvailableOre(PlanetaryResource):
    """ The ore available on the planet.  Varies by planet type.

    Attributes::

        anthracite: 200,
        bauxite:    300,
        etc
    """


class BuildCost(PlanetaryResource):
    """ How much it'll cost to build a building

    Attributes::

        food        500,
        water       500,
        energy      500,
        waste       500,    # is added to your storage, not spent like the other resources
        ore         1000,
        time        1200,   # in seconds
    """


class Production(PlanetaryResource):
    """ How much a building produces (or will produce upon build/upgrade)

    Attributes::

        food_hour       1500,
        energy_hour     -144,
        ore_hour        -1310,
        water_hour      -1100,
        waste_hour      133,
        happiness_hour  0,
    """


class SupplyChain(lacuna.bc.SubClass):
    """
    Attributes::

        id                      "id-goes-here",
        from_body               lacuna.body.SimpleBody object
        from_body               {   "id" : "id-goes-here",
                                    "name" : "Mars",
                                    "x" : 0,
                                    "y" : -123,
                                    "image" : "station",     },
        resource_hour           10000000,
        resource_type           'water',
        percent_transferred     95,
        stalled                 0,
    """
    def __init__(self, client, mydict:dict):
        if 'from_body' in mydict:
            self.from_body = lacuna.body.SimpleBody(client, mydict['from_body'])
            del mydict['from_body']
        super().__init__(client, mydict)
        


