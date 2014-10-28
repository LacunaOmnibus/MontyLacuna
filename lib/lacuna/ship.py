
""" 
Different types of ship objects have varying attributes depending on what 
state the ship is in.

Several of the Ship subclasses are identical in code to the base class, but 
their attributes will be different, so separate classes exist to avoid 
confusion.
"""

class Ship():
    """ Base class """
    def __init__( self, client, mydict:dict, *args, **kwargs ):
        self.client = client
        for k, v in mydict.items():
            setattr(self, k, v)

class BuildingShip(Ship):
    """ A ship being built (currently in the shipyard queue):
             id               "1234",
             type             "spy_pod",
             type_human       "Spy Pod",
             date_completed   "01 31 2010 13:09:05 +0600"
    """
    def __init__( self, client, mydict:dict, *args, **kwargs ):
        super().__init__( client, mydict, *args, **kwargs )

class ExistingShip(Ship):
    """ An existing ship has finished building.  It's taking up dock space in a
    spaceport, but it does not appear in a build queue.

            id              "id-goes-here",
            name            "CS3",
            type_human      "Cargo Ship",
            type            "cargo_ship",
            task            "Travelling",
            speed           "400",
            fleet_speed     "0",
            stealth         "0",
            hold_size       "1200",
            berth_level     "1",
            date_started    "01 31 2010 13:09:05 +0600",
            date_available  "02 01 2010 10:08:33 +0600",
            date_arrives    "02 01 2010 10:08:33 +0600",
            can_recall      "0",
            can_scuttle     "1",
            from            {
                                "id" : "id-goes-here",
                                "type" : "body",
                                "name" : "Earth"
                            },

            You'll only get 'to' if the ship is currently travelling somewhere:
            to              {
                                "id" : "id-goes-here",
                                "type" : "body",
                                "name" : "Mars"
                            }

            You'll only get 'orbiting' if the ship is currently orbiting another
            planet:
            orbiting        {
                                "id" : "id-goes-here",
                                "type" : "body",
                                "name" : "Mars",
                                "x" : 4,
                                "y" : -3,
                            }
    """

class FleetShip(Ship):
    """ A FleetShip is an existing docked ship that's ready to be added to a 
    fleet action against a specific target (spaceport.get_my_fleet_for())
            type                    "sweeper",
            type_human              "Sweeper",
            speed                   10166,
            stealth                 10948,
            combat                  33372,
            quantity                103,
            estimated_travel_time   "3654",

    """

class IncomingShip(Ship):
    """ How much information you can see about an incoming ship depends upon 
    its origin, the level of the spaceport that's looking at the ship, and how 
    high the ship's stealth level is.

    The formula for determining whether a spaceport can see a given ship is:
        350 * SpacePort Level >= Ship Stealth

    If the ship is from a friendly empire, or its stealth level is low enough 
    to be seen by your spaceport:
            id             "id-goes-here",
            name           "CS3",
            type_human     "Cargo Ship",
            type           "cargo_ship",
            date_arrives   "02 01 2010 10:08:33 +0600",
            can_recall     "0",
            can_scuttle    "0",
            from            {   "id"    "id-goes-here",
                                "name"  "Earth",
                                "empire {   "id"    "id-goes-here",
                                            "name"  "Earthlings"    }    }

    If the ship is from a hostile empire (anyone not in your alliance), and your 
    spaceport is not high enough level to see past its stealth, you'll only get:
            date_arrives   '24 10 2014 04:35:39 +0000',
            from            {},
            id              '45549844',
            name            'Unknown',
            type            'unknown',
            type_human      'Unknown'

    Each ship is evaluated separately, so it's possible that a given spaceport 
    will be able to see some, but not all, of the incomings.
    """

class MiningPlatform(Ship):
    """ A mining platform is a mining platform ship that has successfully 
    arrived at an asteroid and converted itself into a mining platform.  The 
    platform itself is no longer actually a ship, and does not have a name or ID
    of its own.
            empire_id       ID of your empire, NOT of the ship
            empire_name     Name of your empire, NOT of the ship
    """

class PotentialShip(Ship):
    """ A PotentialShip does not yet exist in any form; this is a ship that is 
    able to be built (returned from a call to shipyard.get_buildable()):
            can             1,       # can it be built or not
            combat          0,
            hold_size       1000,
            max_occupants   2,
            reason          null,    # if it can't an array ref will be here with the exception for why not
            speed           1000,    # 100 roughly equals 1 star in 1 hour
            stealth         1500
            type            placebo
            cost    {
                "seconds" : 900,
                "food" : 1100,
                "water" : 1000,
                "energy" : 1200,
                "ore" : 1200,
                "waste" : 100,
            },
    """
    def __init__( self, client, mydict:dict, *args, **kwargs ):
        for k, v in mydict['attributes'].items():
            setattr(self, k, v)
        del mydict['attributes']
        super().__init__( client, mydict, *args, **kwargs )

class UnavailableShip(Ship):
    """ An UnavailableShip is an existing docked ship that's not able to be 
    sent to a specific target for some reason.
            type                    "sweeper",
            type_human              "Sweeper",
            speed                   10166,
            stealth                 10948,
            combat                  33372,
            quantity                103,
            estimated_travel_time   "3654",
            reason                  [   1009,
                                        "You can't send a detonator to a star"   ]
    """

    def __init__( self, client, reason:list, mydict:dict, *args, **kwargs ):
        """
            reason is a list:
                    [ 1009, "Cannot send a detonator to a star" ]
        """
        mydict['reason'] = reason
        super().__init__( client, mydict, *args, **kwargs )



