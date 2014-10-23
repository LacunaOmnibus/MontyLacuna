
from lacuna.bc import LacunaObject
from lacuna.building import Building

"""

LEFT OFF AT SEND_SHIP() - complete from there on (inclusive)


Remember that multiple spaceport buildings on a single planet work together as a 
single unit.  So calling view_all_ships() on one spaceport building will return 
exactly the same list as calling it on a different spaceport building (on the 
same planet).

view() retval includes:
    "max_ships":        Integer maximum ships that can be stored
    "docks_available":  Integer; how many more ships can be stored
    "docked_ships":     Dict; summary of counts of ships currently at dock:
                    {   "probe": 3
                        "cargo_ship": 0
                        ...     }
"""

class spaceport(Building):
    path = 'spaceport'

    def __init__( self, client, body_id:int = 0, building_id:int = 0 ):
        super().__init__( client, body_id, building_id )

    @LacunaObject.set_empire_status
    @Building.call_building_meth
    def view_all_ships( self, paging:dict={}, filter:dict={}, sort:str='type', *args, **kwargs ):
        """ Show all ships on the planet.

        All three arguments are optional.  If sent, they are:
            "filter"
                A dict of filter critera, which can contain the keys 'task', 
                    'type', and/or 'tag'.
                    "task":     Building, Defend, Docked, Mining, Orbiting, 
                                Supply Chain, Travelling, Waiting on Trade, 
                                Waste Chain
                    "type":     Any of the existing ship types (eg "placebo5", 
                                "scow_fast", etc)
                    "tag":      Colonization, Exploration, Intelligence, Mining, 
                                Trade, War
                Filter critera are joined with 'or', not 'and'.
                So this filter dict may not be what you really mean:
                    {   'type': 'supply_pod3',
                        'task': 'Docked'    }
                Instead of telling you about just the Supply Pod IIIs that are 
                currently docked, it's going to tell you about all your Supply
                Pod IIIs, as well as all of the other ships that are currently 
                Docked, which may be more than you were expecting.

            "paging"
                A dict of paging criteria
                    "no_paging":        If true, all ships will be returned, and 
                                        all other paging options will be ignored.
                    "page_number":      Integer page number to view
                    "items_per_page":   Integer number of items per page

            "sort"
                A string to specify what to sort the results on.  Defaults to 
                'type'.  Valid options:
                    combat, name, speed, stealth, task, type
                    
        Retval contains:
            "number_of_ships":  This is the total number that result from 
                                your filter, ignoring your pagin
            "ships":             a list of ship dicts:
                {
                    "id" : "id-goes-here",
                    "name" : "CS3",
                    "type_human" : "Cargo Ship",
                    "type" : "cargo_ship",
                    "task" : "Travelling",
                    "speed" : "400",
                    "fleet_speed" : "0",
                    "stealth" : "0",
                    "hold_size" : "1200",
                    "berth_level" : "1",
                    "date_started" : "01 31 2010 13:09:05 +0600",
                    "date_available" : "02 01 2010 10:08:33 +0600",
                    "date_arrives" : "02 01 2010 10:08:33 +0600",
                    "can_recall" : "0",
                    "can_scuttle" : "1",
                    "from" : {
                    "id" : "id-goes-here",
                    "type" : "body",
                    "name" : "Earth"
                    },
                    "to" : {
                    "id" : "id-goes-here",
                    "type" : "body",
                    "name" : "Mars"
                    }
                },
        """
        pass

    @LacunaObject.set_empire_status
    @Building.call_building_meth
    def view_foreign_ships( self, page_number:int = 1, *args, **kwargs ):
        """ Shows information on incoming foreign ships.

        Shows 25 ships per page.  "page_number" lets you select which page to 
        show.

        Retval includes
            "number_of_ships":  Integer count of incoming ships
            "ships":            List of incoming ship dicts
                The format of the ship dicts depends upon whether your 
                spaceport is of high enough level to see past the incoming 
                ship's stealth rating.

                If so:
                    {   'date_arrives': '24 10 2014 01:56:16 +0000',
                        'from': {   'empire': {'id': '-9', 'name': 'DeLambert'},
                                    'id': '71654',
                                    'name': 'DeLambert-15-71654'},
                        'id': '15988444',
                        'name': 'Galleon 26',
                        'type': 'galleon',
                        'type_human': 'Galleon'},
                If not:
                    {   'date_arrives': '24 10 2014 04:35:39 +0000',
                        'from': {},
                        'id': '45549844',
                        'name': 'Unknown',
                        'type': 'unknown',
                        'type_human': 'Unknown'}

                Each ship is evaluated separately, so it's possible that a 
                given spaceport will be able to see some, but not all, of the 
                incomings.
        """
        pass

    @LacunaObject.set_empire_status
    @Building.call_naked_meth
    def get_fleet_for( self, from_body_id:int, target:dict, *args, **kwargs ):
        """ See docs for get_my_fleet_for().  """
        pass

    def get_my_fleet_for( self, target:dict, *args, **kwargs ):
        """ Gets ships available for fleet action to the target.

        'target' is a dict in one of the following forms:
                { "body_name" : "Earth" }
                { "body_id" : "id-goes-here" }
                { "star_name" : "Sol" }
                { "star_id" : "id-goes-here" }
                { "x" : 4, "y" : -3 }

        Retval includes 'ships', a list of ship dicts:
                {   'combat': 0,
                    'estimated_travel_time': '793',
                    'quantity': '10',
                    'speed': 4058,
                    'stealth': 0,
                    'type': 'hulk_fast',
                    'type_human': 'Hulk Fast'},
                    
        This method is syntactic sugar for calling get_fleet_for(), which 
        requires that the sending body ID be passed.  Since that sending 
        body ID is an attribute of the spaceport object itself, specifically 
        sending it as an argument is silly.

        Raises ServerError 1002 if the requested body_id does not exist.
        """
        return self.get_fleet_for( self.body_id, target )


    @LacunaObject.set_empire_status
    @Building.call_naked_meth
    def get_ships_for( self, from_body_id:int, target:dict, *args, **kwargs ):
        """ See docs for get_my_ships_for()."""
        pass

    def get_my_ships_for( self, target:dict, *args, **kwargs ):
        """ Gets ships available to send to a target, as well as a list of 
        incoming ships for some reason.

        'target' is a dict, identical to that required by get_my_fleet_for().

        As with get_my_fleet_for(), this method is sugar for the actual API
        method.

        Retval includes a whole bunch of stuff:
            "fleet_send_limit"  - Always integer 20.

            "incoming" - List of dicts of ships currently travelling from the 
                          spaceport's planet to the target
                           {   'berth_level': '25',
                                'can_recall': 0,
                                'can_scuttle': 0,
                                'combat': '0',
                                'date_arrives': '23 10 2014 22:54:12 +0000',
                                'date_available': '23 10 2014 22:54:12 +0000',
                                'date_started': '23 10 2014 22:24:27 +0000',
                                'fleet_speed': '0',
                                'from': {'id': '184926', 'name': 'bmots rof 1.1', 'type': 'body'},
                                'hold_size': '176400000',
                                'id': '35514278',
                                'max_occupants': 0,
                                'name': 'Scow Mega 30',
                                'payload': ['176,400,000 waste'],
                                'speed': '451',
                                'stealth': '0',
                                'task': 'Travelling',
                                'to': {'id': '65281', 'name': 'SMA bmots 001', 'type': 'star'},
                                'type': 'scow_mega',
                                'type_human': 'Scow Mega' }

            "available" - List of dicts of ships that can be sent to the target.  
                          Format is the same as 'incoming' EXCEPT:
                            - date_available and date_started both exist as 
                              datetime stamps, but they appear to be the dates 
                              that manufacture was begun and then complete.  
                              They're often far in the past.
                            - The date_arrives, from, and to keys are missing
                            - The payload key exists, but is an empty list.
                            - Added is a key 'estimated_travel_time', which is 
                              the integer seconds travel time from here to the
                              target.

            "unavailable" - List of dicts of ships that cannot be sent to the 
                            target and the reasons they cannot be sent.  Each 
                            dict contains:
                        {
                            'reason': [   1009,
                                        'Use the "push" feature in the Trade Ministry to '
                                        'send this ship to another planet.'     ],
                            'ship': { dict identical to 'available' }
                        },

            "orbiting" - list of dicts of ships currently orbiting the target.  
                         Format is the same as 'available' with the addition of
                         the key 'orbiting' (yes, 'orbiting' will be in there 
                         twice), containing info on the target being orbited:
                         {      'id': '468699',
                                'name': '--=Tatooine=--',
                                'type': 'body',
                                'x': '-301',
                                'y': '126'}

            "mining_platforms" - list of small dicts with info on local mining 
                                  platforms.  This does not exist unless the 
                                  target is an asteroid.
                                {   empire_id   =>  "id-goes-here",
                                    empire_name => "The Peeps From Across The Street"   },
        """
        return self.get_ships_for( self.body_id, target )






