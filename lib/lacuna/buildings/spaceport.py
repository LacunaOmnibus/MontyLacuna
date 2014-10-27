
from lacuna.bc import LacunaObject
from lacuna.building import Building

"""

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

    @LacunaObject.set_empire_status
    @Building.call_naked_meth
    def send_ship( self, ship_id:int, target:dict, *args, **kwargs ):
        """ Sends a single ship to the indicated target.
        
        Requires a captcha if sending attack ships to an inhabited planet.

        Arguments:
            ship_id:    Integer ID of the ship to send
            target:     Dict, identical to the one in get_my_fleet_for()

        Retval includes key 'ship' (singular), identical to the 'incoming' key 
        of get_my_ships_for().
        """
        pass

    @LacunaObject.set_empire_status
    @Building.call_naked_meth
    def send_ship_types( self, from_body_id:int, target:dict, types:list, arrival:dict, *args, **kwargs ):
        """ See docs for send_my_ship_types.  """
        pass
        
    def send_my_ship_types( self, target:dict, types:list, arrival:dict, *args, **kwargs ):
        """ Sends ships of the indicated type to the target, to arrive at the 
        requested time.

        Requires a captcha if sending attack ships to an inhabited planet.

        Sugar method for send_ship_types() - saves you from having to send the 
        ID of the sending body.

        Arguments:
            target:     Dict, identical to the one in get_my_fleet_for()
            types:      List of shiptype dicts
            arrival:    Dict to specify arrival time

            Specifying types:
                You can specify ships to send not just by the shiptype, 
                but also by minimum attributes.  Set only the dict keys 
                you're interested in.
                types = [
                    {   "type" : "sweeper",
                        "speed" : 10166,
                        "stealth" : 10948,
                        "combat" : 33372,
                        "quantity" : 100        },
                    {   "type" : "surveyor",
                        "speed" : 9030,
                        "stealth" : 9030,
                        "combat" : 3220,
                        "quantity" : 10         }
                        ...
                ]

            Specifying arrival time:
                All dict keys must be set.  You likely don't care about 
                what second the ships arrive, but set it anyway.
                {   "day" : "23",
                    "hour" : "12",
                    "minute" : "01",
                    "second" : "30"     }

        Retval is identical to that for get_my_fleet_for().

        Raises ServerError 1009 if the specified arrival time is earlier than 
        the slowest ship in the group can manage at its top speed.
        """
        return self.send_ship_types( self.body_id, target, types, arrival )

    @LacunaObject.set_empire_status
    @Building.call_naked_meth
    def send_fleet( self, ship_ids:list, target:dict, fleet_speed:int = 0, *args, **kwargs ):
        """ Sends a fleet of ships at the target.  A fleet travels as a single 
        unit, so its maximum speed is the highest speed of its slowest ship.

        Arguments:
            ship_ids:       List of integer IDs of ships to send in the fleet
            target:         Dict, identical to the one in get_my_fleet_for()
            fleet_speed:    Optional integer; speed of the fleet.  If omitted 
                            or 0, the fleet will travel at maximum speed.
        """
        pass

    @LacunaObject.set_empire_status
    @Building.call_building_meth
    def recall_ship( self, ship_id:int, *args, **kwargs ):
        """ Recalls a single ship that's currently performing either the 
        'Defend' or 'Orbiting' tasks.

        If the ship being recalled is a Spy Shuttle, it will automatically 
        pick up as many idle spies from the planet it had been orbiting as it 
        can hold.

        Requires 'ship_id', the integer ID of the ship to be recalled.
        """
        pass

    @LacunaObject.set_empire_status
    @Building.call_building_meth
    def recall_all( self, *args, **kwargs ):
        """ Recalls all ships from the current planet that are on 'Defend' or 
        'Orbiting' tasks.
        Note there is no 'target' argument here; this is not recalling all 
        ships orbiting a specific target - this is recalling ALL ships from 
        this planet that are orbiting anywhere.

        Retval includes 'ships', a list of dicts of ships that have been 
        recalled.  These ships are identical to the 'incoming' key of 
        get_my_ships_for(), with the addition of:

            "from" : {  # This is the planet the ships are being recalled from
               "id" : "id-goes-here",
               "type" : "body",
               "name" : "Earth"
            },
            "to" : {    # This is the planet you're recalling the ships back to.
               "id" : "id-goes-here",
               "type" : "star",
               "name" : "Sol"
            }

        Raises NO error if there are no ships currently orbiting, but the 
        'ships' retval will be an empty list.
        """
        pass

    @LacunaObject.set_empire_status
    @Building.call_building_meth
    def name_ship( self, ship_id:int, name:str, *args, **kwargs ):
        """ Rename a ship.
        Up to 30 characters are allowed.  "No profanity or funky characters" 
        (that's from the API docu - use your head.)

        Raises ServerError 1005 if the ship name violates the rules.
        """
        pass

    @LacunaObject.set_empire_status
    @Building.call_building_meth
    def scuttle_ship( self, ship_id:int, *args, **kwargs ):
        """ Scuttles (deletes) a ship.  The ship must be docked.

        Raises ServerError 1013 if the ship is not docked.
        """
        pass

    @LacunaObject.set_empire_status
    @Building.call_building_meth
    def mass_scuttle_ship( self, ship_ids:list, *args, **kwargs ):
        """ Scuttles (deletes) a list of ships.  All ships to be scuttled must 
        be docked.

        If any ships in the list are not docked, no error is raised.  In that 
        case, any ships in the list that _were_ docked will be scuttled; the 
        non-docked ships are simply ignored.
        """
        pass

    @LacunaObject.set_empire_status
    @Building.call_building_meth
    def view_ships_travelling( self, *args, **kwargs ):
        """ Shows all ships travelling from this planet.

        "Travelling" contains two of the letter "l".

        Retval includes:
            number_of_ships_travelling: Integer
            ships_travelling:           List of ship dicts
        """
        pass


    @LacunaObject.set_empire_status
    @Building.call_building_meth
    def view_ships_orbiting( self, *args, **kwargs ):
        """ Shows all FOREIGN ships currently orbiting THIS planet.

        Any orbiting ships whose stealth level is too high will not be shown.  
        The formula for determining whether a spaceport can see a ship is:
            350 * (spaceport level) > (ship's stealth)

        If the orbiting ship is your own (or allied?), you'll be able to see 
        it regardless of stealth level.

        "Orbiting" contains one of the letter "t".

        Retval includes:
            number_of_ships:    Integer
            ships:              List of ship dicts

        Note those retval key names carefully.  It's "number_of_ships", not 
        "number_of_ships_orbiting" - these key names are inconsistent with 
        those returned by view_ships_travelling().
        """
        pass

    @LacunaObject.set_empire_status
    @Building.call_naked_meth
    def prepare_send_spies( self, on_body_id:int, to_body_id:int, *args, **kwargs ):
        """ Gathers the info needed to call send_spies().

        Arguments:
            on_body_id: Integer ID of the body the spies are currently on
            to_body_id: Integer ID of the body to which you wish to send the spies

        Retval includes:
            ships:  List of dicts of ships capable of carrying spies:
                        {   "id" : "id-goes-here",
                            "name" : "CS4",
                            "hold_size" : 1100,
                            "berth_level" : 1,
                            "speed" : 400,
                            "type" : "cargo_ship",
                            "estimated_travel_time" : 3600, # in seconds    },
            spies:  List of dicts of spies whose home is the current planet:
                        {   "id" : "id-goes-here",
                            "level" : 12,
                            "name" : "Jack Bauer",
                            "assigned_to" : {
                                "body_id" : "id-goes-here",
                                "name" : "Earth"
                            },      },
        """
        pass

    @LacunaObject.set_empire_status
    @Building.call_naked_meth
    def send_spies( self, on_body_id:int, to_body_id:int, ship_id:int, spy_ids:list, *args, **kwargs ):
        """ Sends spies to a target.

        Arguments:
            on_body_id:         Integer ID of the body the spies are currently 
                                on.
            to_body_id:         Integer ID of the body to which you wish to 
                                send the spies.
            ship_id:            Integer ID of the ship to carry the spies.
            spy_ids:            List of integer IDs of spies to send.

        Retval includes:
            spies_sent:         List of integer IDs of spies sent.
            spies_not_sent:     List of integer IDs of spies not sent.  This
                                should only have contents if you're cheating.
            ship:               Dict describing the transport ship

        """
        pass

    @LacunaObject.set_empire_status
    @Building.call_naked_meth
    def prepare_fetch_spies( self, on_body_id:int, to_body_id:int, *args, **kwargs ):
        """ Fetches spies back home again.

        Arguments:
            on_body_id:         Integer ID of the body the spies are currently 
                                on (the foreign planet).
            to_body_id:         Integer ID of the body to which you wish to 
                                send the spies (their home planet)
        
        Retval is the same as that for prepare_send_spies().
        """
        pass

    @LacunaObject.set_empire_status
    @Building.call_naked_meth
    def fetch_spies( self, on_body_id:int, to_body_id:int, ship_id:int, spy_ids:list, *args, **kwargs ):
        """ Fetches spies back home again.

        Arguments are the same as for send_spies().  But remember that, like 
        prepare_fetch_spies(), on_body_id is the body the spies are on now 
        (foreign), and to_body_id is the body they're being fetched to (your 
        planet, their home).

        Retval includes 'ship', identical to that for send_spies().
        """
        pass

    @LacunaObject.set_empire_status
    @Building.call_building_meth
    def view_battle_logs( self, page_number:int = 1, *args, **kwargs ):
        """ View battle logs.

        Arguments:
            page_number:    Optional nteger number of page to view.  25 log 
                            entries displayed per page.  Defaults to 1.

        Retval includes:
            number_of_logs: Integer total number of entries in the logbook.
            battle_log:     List of battle log dicts:
                            {   "date" : "06 21 2011 22:54:37 +0600",
                                "attacking_body" : "Romulus",
                                "attacking_empire" : "Romulans",
                                "attacking_unit" : "Sweeper 21",
                                "defending_body" : "Kronos",
                                "defending_empire" : "Klingons",
                                "defending_unit" : "Shield Against Weapons",
                                "victory_to" : "defender"       },
        """
        pass


    ### 
    ### Non-API methods
    ###

    def get_task_ships_for( self, target:dict, type:str, task:str = 'available', quantity:int = 1 ):
        """ Returns a list of ships assigned to a specific task.  
                target = { 'star_name': 'Sol' }
                list = get_task_ships_for( target, 'available', 'sweeper', 10 )

        There are sugar methods available for each of the possible tasks; it 
        should be move convenient to use those.
                target = { 'star_name': 'Sol' }
                available_list          = get_available_ships_for( target, 'sweeper', 10 )
                docked_list             = get_docked_ships_for( target, 'sweeper', 10 )
                incoming_list           = get_incoming_ships_for( target, 'sweeper', 10 )
                mining_list             = get_mining_ships_for( target, 'sweeper', 10 )
                orbiting_list           = get_orbiting_ships_for( target, 'sweeper', 10 )
                supply_chain_list       = get_supply_chain_ships_for( target, 'sweeper', 10 )
                unavailable_list        = get_unavailable_ships_for( target, 'sweeper', 10 )
                waiting_on_trade_list   = get_waiting_on_trade_ships_for( target, 'sweeper', 10 )
                waste_chain_list        = get_waste_chain_ships_for( target, 'sweeper', 10 )

        In each case, the arguments are:
            target:     Same as get_my_fleet_for()
            type:       Type of ship (eg placebo5, smuggler_ship, etc)
            quantity:   Optional integer number of ships to return.  Defaults to 1.
        """
        rv = self.get_my_ships_for( target )
        ships = [] 
        cnt = 0
        for i in rv[task]:
            if i['type'] == type:
                ships.append( i )
                cnt += 1
                if cnt >= quantity:
                    break
        if not 'id' in ships[0]:
            raise KeyError("Unable to find any available", type, "ship.")
        return ships

    def get_available_ships_for( self, target:dict, type:str, quantity:int = 1 ):
        return self.get_task_ships_for( target, type, 'available', quantity )

    def get_defend_ships_for( self, target:dict, type:str, quantity:int = 1 ):
        return self.get_task_ships_for( target, type, 'defend', quantity )

    def get_docked_ships_for( self, target:dict, type:str, quantity:int = 1 ):
        return self.get_task_ships_for( target, type, 'docked', quantity )

    def get_incoming_ships_for( self, target:dict, type:str, quantity:int = 1 ):
        return self.get_task_ships_for( target, type, 'incoming', quantity )

    def get_mining_ships_for( self, target:dict, type:str, quantity:int = 1 ):
        return self.get_task_ships_for( target, type, 'mining_plantforms', quantity )

    def get_orbiting_ships_for( self, target:dict, type:str, quantity:int = 1 ):
        return self.get_task_ships_for( target, type, 'orbiting', quantity )

    def get_supply_chain_ships_for( self, target:dict, type:str, quantity:int = 1 ):
        return self.get_task_ships_for( target, type, 'supply chain', quantity )

    def get_travelling_ships_for( self, target:dict, type:str, quantity:int = 1 ):
        return self.get_task_ships_for( target, type, 'travelling', quantity )

    def get_unavailable_ships_for( self, target:dict, type:str, quantity:int = 1 ):
        return self.get_task_ships_for( target, type, 'unavailable', quantity )

    def get_waiting_on_trade_ships_for( self, target:dict, type:str, quantity:int = 1 ):
        return self.get_task_ships_for( target, type, 'waiting on trade', quantity )

    def get_waste_chain_ships_for( self, target:dict, type:str, quantity:int = 1 ):
        return self.get_task_ships_for( target, type, 'waste chain', quantity )

    def get_spies_back( self, from_id, ship_name = '' ):
        """ Fetches all spies currently posted to a planet back home again.

            on_body_id = 12345
            sp.get_spies_back( on_body_id )

        Arguments:
            on_body_id: Integer ID of the body from which you want to retrieve 
                        your spies.
            ship_name:  Optional; name of the ship you want to use to retrieve 
                        your spies.  If not sent, the first available ship will 
                        be used.

        Retval includes key 'ship':
                {   "id" : "id-goes-here",
                    "name" : "CS4",
                    "hold_size" : 1100,
                    "berth_level" : 1,
                    "speed" : 400,
                    "type" : "cargo_ship",
                    "date_arrives" : "01 31 2010 13:09:05 +0600", ...    }, 
        """
        prep_rv = self.prepare_fetch_spies( from_id, self.body_id )

        ship_id = 0
        if ship_name:
            for ship in prep_rv['ships']:
                if ship['name'] == ship_name:
                    ship_id = ship['id']
                    break
        else:
            ship_id = prep_rv['ships'][0]['id']     # No ship name specified.  Use the first one available.

        if int(ship_id) <= 0:
            raise KeyError("No ships matching your criteria are available to fetch spies.")

        spy_ids = []
        for i in prep_rv['spies']:
            if i['based_from']['body_id'] == self.body_id and i['assigned_to']['body_id'] == from_id:
                spy_ids.append( i['id'] )
        fetch_rv = self.fetch_spies( target_planet.id, my_planet.id, ship_id, spy_ids )
        return fetch_rv

