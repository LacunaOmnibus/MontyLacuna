
import lacuna.bc
import lacuna.body

class Ship(lacuna.bc.SubClass):
    """ Base class for ships.

    Different types of ship objects have varying attributes depending on what 
    state the ship is in.

    In some cases, a hostile ship will only be visisble to you if its stealth 
    level is low enough compared to your SpacePort level.  The formula for 
    determining that is::

        350 * SpacePort Level >= Ship Stealth

    If you're trying to detect ships to a space station, the formula for 
    beating stealth is::

        525 * PoliceStation Level >= Ship Stealth

    A number of ships contain an attribute ``origin``.  In the original API, 
    that attribute was named ``from``.  However, ``from`` is a Python reserved 
    word, so in those cases ``from`` has been changed to ``origin``.
    """
    def __init__(self, client, mydict:dict):
        if 'from' in mydict:
            ### Can't have an attribute named 'from'.
            mydict['origin'] = mydict['from']
            del mydict['from']
        super().__init__(client, mydict)

class BuildingShip(Ship):
    """ A ship being built (currently in the shipyard queue).

    Attributes::

        id               "1234",
        type             "spy_pod",
        type_human       "Spy Pod",
        date_completed   "01 31 2010 13:09:05 +0600"
    """

class Excavator(Ship):
    """ These aren't truly ships anymore, they're excavator sites.  The id is 
    the id of the site that's currently being excavated (the site_id).

    Attributes::

        id              "id-goes-here",
        body            Body object
        artifact        5,
        glyph           30,
        plan            7,
        resource        53
        date_landed     Date excav started at location
    """
    def __init__( self, client, mydict:dict, *args, **kwargs ):
        mydict['body'] = lacuna.body.Body(client, mydict['body'])
        super().__init__( client, mydict )


class ExistingShip(Ship):
    """ An existing ship is one of your own ships that has finished building.  
    It's taking up dock space in a spaceport, but it does not appear in a build 
    queue.

    Attributes::

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
        max_occupants   120                             # attribute will always exist, but will 
                                                        # sometimes be '0'.
        origin          lacuna.body.ShipDest object
        to              lacuna.body.ShipDest object     # Will only appear if the ship is currently
                                                        # travelling somewhere:
        orbiting        lacuna.ship.ShipHub object
    """
    def __init__(self, client, mydict):
        if not 'max_occupants' in mydict:
            mydict['max_occupants'] = 0
        if 'to' in mydict:
            mydict['to'] = lacuna.body.ShipDest(client, mydict['to'] )
        if 'from' in mydict:
            mydict['from'] = lacuna.body.ShipDest(client, mydict['from'] )
        if 'orbiting' in mydict:
            mydict['orbiting'] = lacuna.body.ShipHub(client, mydict['orbiting'] )
        super().__init__(client, mydict)

class FleetShip(Ship):
    """ A FleetShip is an existing docked ship that's ready to be added to a 
    fleet action against a specific target (``spaceport.get_my_fleet_for()``)

    Attributes::

        type                    "sweeper",
        type_human              "Sweeper",
        speed                   10166,
        stealth                 10948,
        combat                  33372,
        quantity                103,
        estimated_travel_time   "3654",
    """

class ForeignOrbiting(Ship):
    """ A ship currently orbiting your planet.

    Attributes::

        id              "id-goes-here",
        name            "SS3",
        type            "spy_shuttle",
        type_human      "Spy Shuttle",
        date_arrived    "02 01 2010 10:08:33 +0600",
        origin          {   "id" : "id-goes-here",
                            "name" : "Mars",
                            "empire" : {    "id" : "id-goes-here",
                                            "name" : "Martians"  }  }

    """

class IncomingShip(Ship):
    """ How much information you can see about an incoming ship depends upon 
    its origin, the level of the spaceport that's looking at the ship, and how 
    high the ship's stealth level is.

    Attributes if the ship is from a friendly empire, or its stealth level is low enough 
    to be seen by your spaceport::

        id             "id-goes-here",
        name           "CS3",
        type_human     "Cargo Ship",
        type           "cargo_ship",
        date_arrives   "02 01 2010 10:08:33 +0600",
        can_recall     "0",
        can_scuttle    "0",
        origin          {   "id"    "id-goes-here",
                            "name"  "Earth",
                            "empire {   "id"    "id-goes-here",
                                        "name"  "Earthlings"    }    }

    Attributes if the ship is from a hostile empire (anyone not in your alliance), and your 
    spaceport is not high enough level to see past its stealth, you'll only get::

        date_arrives   '24 10 2014 04:35:39 +0000',
        origin          {},
        id              '45549844',
        name            'Unknown',
        type            'unknown',
        type_human      'Unknown'

    Each ship is evaluated separately, so it's possible that a given spaceport 
    will be able to see some, but not all, of the incomings.
    """

class IncomingToBodyShip(Ship):
    """ An IncomingShip is what you can see from your Space Port or Police 
    Station, while an IncomingToBodyShip is the much reduced information you 
    can get from a MyBody object.

    Attributes::

        id              "id-goes-here",
        date_arrives    "01 31 2010 13:09:05 +0600",
        is_own          1 or 0,
        is_ally         1 or 0
    """


class PotentialShip(Ship):
    """ A PotentialShip does not yet exist in any form; this is a ship that is 
    able to be built (returned from a call to shipyard.get_buildable()):

    Attributes::

        can             1,       # can it be built or not
        combat          0,
        hold_size       1000,
        max_occupants   2,
        reason          null,    # if it can't an array ref will be here with the exception for why not
        speed           1000,    # 100 roughly equals 1 star in 1 hour
        stealth         1500
        type            placebo
        cost            {   "seconds" : 900,
                            "food" : 1100,
                            "water" : 1000,
                            "energy" : 1200,
                            "ore" : 1200,
                            "waste" : 100,  },
    """
    def __init__( self, client, mydict:dict, *args, **kwargs ):
        for k, v in mydict['attributes'].items():
            setattr(self, k, v)
        del mydict['attributes']
        super().__init__( client, mydict, *args, **kwargs )

class TradeableShip(Ship):
    """ A TradeableShip is an existing docked ship that's ready to be added to 
    a trade as merchandise. (trading.get_ships())

    Attributes::

        id                      1234,
        type                    "smuggler_ship",
        name                    "My Trade Smug",
        estimated_travel_time   "3654" (or 'unknown'),

    Several get_trade_ships()-type methods include an optional target argument.  
    If that argument is passed in, we can know the estimated travel time to the 
    target.  Without that argument, 'estimated_travel_time' will be 'unknown'.
    """
    def __init__( self, client, mydict:dict, *args, **kwargs ):
        super().__init__( client, mydict, *args, **kwargs )
        if not hasattr(self, 'estimated_travel_time'):
            self.estimated_travel_time = 'unknown'

class TradeTransportShip(Ship):
    """ A TradeShip is an existing docked ship that's ready to be used as the 
    transport vehicle to add a trade to the Trade Ministry.  
    (trade.get_trade_ships())

    Attributes::

        id                      1234,
        type                    "smuggler_ship",
        name                    "My Trade Smug",
        estimated_travel_time   "3654",
    """

class TravellingShip(Ship):
    """ A TravellingShip is a ship owned by your empire, currently in the air
    between two points.

    Attributes::

        id              "id-goes-here",
        type            "probe",
        type_human      "Probe",
        date_arrives    "01 31 2010 13:09:05 +0600",
        origin          {   "id" : "id-goes-here",
                            "type" : "body",
                            "name" : "Earth"    },
        to              {   "id" : "id-goes-here",
                            "type" : "star",
                            "name" : "Sol"      }
    """

class UnavailableShip(Ship):
    """ An UnavailableShip is an existing docked ship that's not able to be 
    sent to a specific target for some reason.

    Attributes::

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
            ### reason is a list:
            ###     [ 1009, "Cannot send a detonator to a star" ]
        mydict['reason'] = reason
        super().__init__( client, mydict, *args, **kwargs )

class ChainShip(Ship):
    """ A ChainShip is owned by your empire and is either on or capable of 
    being added to a Waste Chain or a Supply Chain.

    Attributes::

        id              "id-goes-here",
        type            "scow",
        task            "Docked", "Supply Chain", or "Waste Chain".
        name            "My Garbage Scow",
        speed           600
        hold_size       1234800


    For ``task``, the TLE documentation says the task is "Resource Chain", but 
    it does return "Supply Chain", not "Resource Chain".
    """

