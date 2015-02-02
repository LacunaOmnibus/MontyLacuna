
import operator

import lacuna.bc
import lacuna.building
import lacuna.exceptions as err
import lacuna.ship
import lacuna.spy

class spaceport(lacuna.building.MyBuilding):
    """
    Multiple spaceport buildings on a single planet work together as a single 
    unit.  So calling :py:meth:`view_all_ships` on one spaceport building will 
    return exactly the same list as calling it on a different spaceport 
    building (on the same planet).

    Since it usually doesn't matter which spaceport you get, you'll generally 
    grab one by doing::

        >>> sp = my_planet.get_buildings_bytype( 'spaceport', 1, 1, 100 )[0]
        Minimum level 1, only get 1, make sure its efficiency is at 100%.  
        Even though we're only asking for one ship, get_buildings_bytype() 
        always returns a list, so grab off the first ([0]) element.

    """

    path = 'spaceport'
    """ The name of the TLE module that will process our requests.  Don't 
    fool with this.  """

    def __init__( self, client, body_id:int = 0, building_id:int = 0 ):
        super().__init__( client, body_id, building_id )

    @lacuna.building.MyBuilding.call_returning_meth
    def view( self, *args, **kwargs ):
        """ View the spaceport.

        Returns a tuple:
            - docked_ships -- Dict; summary of counts of ships currently at dock
            - docks_available -- Integer number of unused docks that can be filled
            - docks_max -- Integer total number of docks across all spaceports
            
            docked_ships dict::

                {   "probe": 3,
                    "cargo_ship": 0,
                    etc         }

        """
        docked_ships    = 0
        docks_avail     = 0
        max_ships       = 0

        if 'docked_ships' in kwargs['rslt']:
            docked_ships = self.get_type(kwargs['rslt']['docked_ships'])
        if 'docks_available' in kwargs['rslt']:
            docks_avail = self.get_type(kwargs['rslt']['docks_available'])
        if 'max_ships' in kwargs['rslt']:
            max_ships = self.get_type(kwargs['rslt']['max_ships'])

        return (
            docked_ships,
            docks_avail,
            max_ships,
        )

    @lacuna.building.MyBuilding.call_returning_meth
    def view_all_ships( self, paging:dict={}, filter:dict={}, sort:str='type', *args, **kwargs ):
        """ Show all ships based from this planet, regardless of their task.

        Arguments:
            - paging -- Optional dict of paging criteria with the keys:
                - ``page_number`` -- page number to view
                - ``items_per_page`` -- number of items per page
                - ``no_paging`` -- Boolean.  Mutually exclusive with the other two 
                  keys.  If sent with a True value, all ships will be returned, 
                  un-paginated.
            - filter -- A dict of filter critera, with the keys:
                - ``task`` -- One of ``Building``, ``Defend``, ``Docked``, 
                  ``Mining``, ``Orbiting``, ``Supply Chain``, ``Travelling``, 
                  ``Waiting on Trade``, or ``Waste Chain``.
                - ``type`` -- Any of the existing ship types (eg "placebo5", 
                  "scow_fast", etc)
                - ``tag`` -- ``Colonization``, ``Exploration``, 
                  ``Intelligence``, ``Mining``, ``Trade``, ``War`` 
            - sort -- A string to specify what to sort the results on.
                - Valid options: ``combat``, ``name``, ``speed``, ``stealth``, 
                  ``task``, ``type``.
                - Defaults to ``type``.

        Filter critera are joined with 'or', not 'and'.  So this filter dict may 
        not be what you really mean::

            {   'type': 'supply_pod3',
                'task': 'Docked'    }

        Instead of telling you about just the Supply Pod IIIs that are 
        currently docked, it's going to tell you about all your Supply Pod 
        IIIs, as well as all of the other ships that are currently Docked, 
        which may be more than you were expecting.

        Returns a tuple:
            - ships -- list of :class:`lacuna.ship.ExistingShip` objects.
            - number_of_ships -- is the total number that result from your filter, ignoring your pagin
        """

        ship_list = []
        for i in kwargs['rslt']['ships']:
            ship_list.append( lacuna.ship.ExistingShip(self.client, i) )
        return( 
            ship_list, 
            self.get_type(kwargs['rslt']['number_of_ships'])
        )

    @lacuna.building.MyBuilding.call_returning_meth
    def view_foreign_ships( self, page_number:int = 1, *args, **kwargs ):
        """ Shows information on incoming foreign ships.

        Shows 25 ships per page.  "page_number" lets you select which page to 
        show.

        Returns a tuple:
            - ships -- List of :class:`lacuna.ship.IncomingShip` objects
            - number_of_ships -- Integer count of incoming ships
        """
        ship_list = []
        for i in kwargs['rslt']['ships']:
            ship_list.append( lacuna.ship.IncomingShip(self.client, i) )
        return( 
            ship_list, 
            self.get_type(kwargs['rslt']['number_of_ships'])
        )

    @lacuna.building.MyBuilding.call_naked_returning_meth
    def _get_fleet_for( self, from_body_id:int, target:dict, *args, **kwargs ):
        """ This method is included because it's documented in the TLE API. 
        """
        ship_list = []
        for i in kwargs['rslt']['ships']:
            ship_list.append( lacuna.ship.ExistingShip(self.client, i) )
        return ship_list

    def get_my_fleet_for( self, target:dict, *args, **kwargs ):
        """ Gets ships available for fleet action to the target.

        Arguments:
            - target -- :ref:`standard target dict <gloss_target>`

        Returns a list of :class:`lacuna.ship.FleetShip` objects.
                    
        Raises :class:`lacuna.exceptions.ServerError` 1002 if the requested 
        body_id does not exist.
        """
        ### This method is syntactic sugar for calling _get_fleet_for, which 
        ### requires that the sending body ID be passed.  Since that sending  
        ### body ID is an attribute of the spaceport object itself, 
        ### specifically sending it as an argument is silly.
        return self._get_fleet_for( self.body_id, target )

    @lacuna.building.MyBuilding.call_naked_returning_meth
    def _get_ships_for( self, from_body_id:int, target:dict, *args, **kwargs ):
        """ See docs for :py:meth:`get_my_ships_for`."""

        inc_list = []
        for i in kwargs['rslt']['incoming']:
            inc_list.append( lacuna.ship.IncomingShip(self.client, i) )
        avail_list = []
        for i in kwargs['rslt']['available']:
            avail_list.append( lacuna.ship.ExistingShip(self.client, i) )
        unavail_list = []
        for i in kwargs['rslt']['unavailable']:
            unavail_list.append( lacuna.ship.UnavailableShip(self.client, i['reason'], i['ship']) )
        orbit_list = []
        if 'orbiting' in kwargs['rslt']:
            for i in kwargs['rslt']['orbiting']:
                orbit_list.append( lacuna.ship.ExistingShip(self.client, i) )
        mining_list = []
        if 'mining_platforms' in kwargs['rslt']:
            for i in kwargs['rslt']['mining_platforms']:
                mining_list.append( MiningPlatform(self.client, i) )
        return(
            inc_list, avail_list, unavail_list, orbit_list, mining_list,
            self.get_type(kwargs['rslt']['fleet_send_limit'])
        )

    def get_my_ships_for( self, target:dict, *args, **kwargs ):
        """ Gets ships available to send to a target, as well as a list of 
        incoming ships for some reason.

        This method returns a lot of tuples, and you're often only going to be 
        interested in one of them.  If that's the case, see instead 
        :py:meth:`get_task_ships_for`.

        Arguments:
            - target -- :ref:`standard target dict <gloss_target>`

        Returns a tuple:
            - incoming -- List of :class:`lacuna.ship.IncomingShip` objects
            - available -- List of :class:`lacuna.ship.ExistingShip` objects
            - unavailable -- List of :class:`lacuna.ship.UnavailableShip` 
              objects
            - orbiting -- List of :class:`lacuna.ship.ExistingShip` objects
            - mining_platforms -- List of :class:`MiningPlatform` objects
            - fleet_send_limit -- Always integer 20.

        """
        return self._get_ships_for( self.body_id, target )

    @lacuna.building.MyBuilding.call_naked_returning_meth
    def send_ship( self, ship_id:int, target:dict, *args, **kwargs ):
        """ Sends a single ship to the indicated target.
        
        Requires a captcha if sending attack ships to an inhabited planet.

        Arguments:
            - ship_id -- Integer ID of the ship to send
            - target -- :ref:`standard target dict <gloss_target>`

        Returns a :class:`lacuna.ship.IncomingShip` object for the single sent 
        ship.
        """
        return lacuna.ship.IncomingShip(self.client, kwargs['rslt']['ship'])

    @lacuna.bc.LacunaObject.set_empire_status
    @lacuna.building.MyBuilding.call_naked_meth
    def _send_ship_types( self, from_body_id:int, target:dict, types:list, arrival:dict, *args, **kwargs ):
        """ See docs for send_my_ship_types.  """
        pass
        
    def send_my_ship_types( self, target:dict, types:list, arrival:dict, *args, **kwargs ):
        """ Sends ships of the indicated type to the target, to arrive at the 
        requested time.

        Requires a captcha if sending attack ships to an inhabited planet.

        Arguments
            - target -- :ref:`standard target dict <gloss_target>`
            - types -- List of shiptype dicts.  See below.
            - arrival -- Dict to specify arrival time.  See below.

        Shiptype dicts
            You can specify ships to send not just by the shiptype, 
            but also by minimum attributes.  Set only the dict keys 
            you're interested in::

                types = [{  "type" : "sweeper",
                            "speed" : 10166,
                            "stealth" : 10948,
                            "combat" : 33372,
                            "quantity" : 100        },
                    {       "type" : "surveyor",
                            "speed" : 9030,
                            "stealth" : 9030,
                            "combat" : 3220,
                            "quantity" : 10         }, { more of the same }, ]

        Arrival time dicts
            All dict keys must be set.  You likely don't care about 
            what second the ships arrive, but set it anyway::

                {   "day" : "23",
                    "hour" : "12",
                    "minute" : "01",
                    "second" : "30"         }

        Return is identical to that for get_my_fleet_for().

        Raises :class:`lacuna.exceptions.ServerError` 1009 if the specified 
        arrival time is earlier than the slowest ship in the group can manage 
        at its top speed.
        """
        ### Sugar method for _send_ship_types() - saves you from having to 
        ### send the ID of the sending body.
        return self._send_ship_types( self.body_id, target, types, arrival )

    @lacuna.bc.LacunaObject.set_empire_status
    @lacuna.building.MyBuilding.call_naked_meth
    def send_fleet( self, ship_ids:list, target:dict, fleet_speed:int = 0, *args, **kwargs ):
        """ Sends a fleet of ships at the target.  A fleet travels as a single 
        unit, so its maximum speed is the highest speed of its slowest ship.

        Arguments:
            - ship_ids -- List of integer IDs of ships to send in the fleet
            - target -- :ref:`standard target dict <gloss_target>`
            - fleet_speed -- Optional integer; speed of the fleet.  If omitted or 0, the fleet will travel at maximum speed.
        """
        pass

    @lacuna.bc.LacunaObject.set_empire_status
    @lacuna.building.MyBuilding.call_building_meth
    def recall_ship( self, ship_id:int, *args, **kwargs ):
        """ Recalls a single ship that's currently performing either the 
        'Defend' or 'Orbiting' tasks.

        Arguments:
            - ship_id -- Integer ID of the ship to recall.

        If the ship being recalled is a Spy Shuttle, it will automatically 
        pick up as many idle spies from the planet it had been orbiting as it 
        can hold.
        """
        pass

    @lacuna.building.MyBuilding.call_returning_meth
    def recall_all( self, *args, **kwargs ):
        """ Recalls all ships from the current planet that are on 'Defend' or 
        'Orbiting' tasks.
        Note there is no 'target' argument here; this is not recalling all 
        ships orbiting a specific target - this is recalling *all* ships from 
        this planet that are orbiting anywhere.

        Returns a list of :class:`lacuna.ship.IncomingShip` objects, with the 
        following additional attributes::

            returning_from:    {  # This is the planet the ships are being recalled from
                                    "id" : "id-goes-here",
                                    "type" : "body",
                                    "name" : "Earth"
                                },
            to:                 {    # This is the planet you're recalling the ships back to.
                                    "id" : "id-goes-here",
                                    "type" : "star",
                                    "name" : "Sol"
                                }

        Raises no error if there are no ships currently orbiting, but the 
        'ships' retval will be an empty list.
        """
        ship_list = []
        ### At least on PT, the retval from the server here is ridiculous and 
        ### not as documented.  The ['ships'] key in the retval that we're 
        ### actually getting is a list of hashrefs:
        ###
        ###    ships = [
        ###     { 'ship' => { the actual ship hashref} },
        ###     { 'ship' => { the actual ship hashref} },
        ###     etc
        ###    ]
        ###
        ### The TLE documentation mentions 'ships' as a straight-up list of 
        ### ship hashrefs, but says nothing about 'ship', but that's what 
        ### we're getting.
        ### I don't know if this is a bug in the documentation or a bug in the 
        ### code, but since it's so utterly ridiculous I'm guessing it's a bug 
        ### in the code - the docu makes sense.
        ### In the meantime, deal with what we've actually got.
        ###
        ### While we're at it, Python is none to happy about my trying to 
        ### create an attribute called 'from' - I assume 'from' is a reserved 
        ### word.  So copy it to 'returning_from'.
        for i in kwargs['rslt']['ships']:
            i['ship']['returning_from'] = i['ship']['from'] 
            ship_list.append( lacuna.ship.IncomingShip(self.client, i['ship']) )
        return ship_list

    @lacuna.bc.LacunaObject.set_empire_status
    @lacuna.building.MyBuilding.call_building_meth
    def name_ship( self, ship_id:int, name:str, *args, **kwargs ):
        """ Rename a ship.

        Arguments:
            - ship_id -- Integer ID of the ship to rename.

        Up to 30 characters are allowed.  "No profanity or funky characters" 
        (that's from the API docu - use your head.)

        Raises :class:`lacuna.exceptions.ServerError` 1005 if the ship name 
        violates the rules.
        """
        pass

    @lacuna.bc.LacunaObject.set_empire_status
    @lacuna.building.MyBuilding.call_building_meth
    def scuttle_ship( self, ship_id:int, *args, **kwargs ):
        """ Scuttles (deletes) a ship.  The ship must be docked.

        Arguments:
            - ship_id -- Integer ID of the ship to scuttle.

        Raises :class:`lacuna.exceptions.ServerError` 1013 if the ship is not docked.
        """
        pass

    @lacuna.bc.LacunaObject.set_empire_status
    @lacuna.building.MyBuilding.call_building_meth
    def mass_scuttle_ship( self, ship_ids:list, *args, **kwargs ):
        """ Scuttles (deletes) a list of ships.  All ships to be scuttled must 
        be docked.

        Arguments:
            - ship_ids -- List of integer ship IDs.

        If any ships in the list are not docked, no error is raised.  In that 
        case, any ships in the list that _were_ docked will be scuttled; the 
        non-docked ships are simply ignored.
        """
        pass

    @lacuna.building.MyBuilding.call_returning_meth
    def view_ships_travelling( self, *args, **kwargs ):
        """ Shows all ships travelling from this planet.

        "Travelling" contains *two* of the letter "l".

        Returns a tuple:
            - ships -- List of :class:`lacuna.ship.TravellingShip` objects
            - number -- Integer count of ships in the air
        """
        ship_list = []
        for i in kwargs['rslt']['ships_travelling']:
            ship_list.append( lacuna.ship.TravellingShip(self.client, i) )
        return(
            ship_list, 
            self.get_type(kwargs['rslt']['number_of_ships_travelling'])
        )


    @lacuna.building.MyBuilding.call_returning_meth
    def view_ships_orbiting( self, *args, **kwargs ):
        """ Shows all FOREIGN ships currently orbiting THIS planet, dependent 
        upon the stealth levels of those orbiting ships.

        "Orbiting" contains *one* of the letter "t".

        Returns a tuple:
            - ships -- List of :class:`lacuna.ship.ForeignOrbiting` objects
            - number_of_ships -- Integer
        """
        ### Returned keys here are 'ships' and 'number_of_ships' - these names 
        ### are inconsistent with the names returned from the TLE call to 
        ### view_ships_travelling.
        ship_list = []
        for i in kwargs['rslt']['ships']:
            ship_list.append( lacuna.ship.ForeignOrbiting(self.client, i) )
        return(
            ship_list, 
            self.get_type(kwargs['rslt']['number_of_ships'])
        )

    @lacuna.building.MyBuilding.call_naked_returning_meth
    def prepare_send_spies( self, on_body_id:int, to_body_id:int, *args, **kwargs ):
        """ Gathers the info needed to call :py:meth:`send_spies`.

        Arguments:
            - on_body_id -- Integer ID of the body the spies are currently on
            - to_body_id -- Integer ID of the body to which you wish to send the spies

        Returns a tuple:
            - ships -- List of :class:`lacuna.ship.ExistingShip` objects
            - spies -- List of :class:`lacuna.spy.Spy` objects
        """
        ship_list = []
        for i in kwargs['rslt']['ships']:
            ship_list.append( lacuna.ship.ExistingShip(self.client, i) )
        spy_list = []
        for i in kwargs['rslt']['spies']:
            spy_list.append( lacuna.spy.Spy(self.client, i) )
        return(
            ship_list, 
            spy_list
        )

    @lacuna.building.MyBuilding.call_naked_returning_meth
    def send_spies( self, on_body_id:int, to_body_id:int, ship_id:int, spy_ids:list, *args, **kwargs ):
        """ Sends spies to a target.

        Arguments:
            - on_body_id -- Integer ID of the body the spies are currently on.
            - to_body_id -- Integer ID of the body to which you wish to send the spies.
            - ship_id -- Integer ID of the ship to carry the spies.
            - spy_ids -- List of integer IDs of spies to send.

        Returns a tuple:
            - spies_sent -- List of IDs of sent spies (not Spy objects)
            - spies_not_sent -- List of IDs of sent spies (not Spy objects).  
              This should only have contents if you're cheating (that's per the 
              TLE API docs; I don't know what it means).
            - ship -- :class:`lacuna.ship.TravellingShip` object
        """
        sent_list = []
        for id in kwargs['rslt']['spies_sent']:
            sent_list.append( id )
        not_sent_list = []
        for id in kwargs['rslt']['spies_not_sent']:
            not_sent_list.append( id )
        ship = lacuna.ship.TravellingShip(self.client, kwargs['rslt']['ship'])
        return(
            sent_list,
            not_sent_list,
            ship
        )

    @lacuna.building.MyBuilding.call_naked_returning_meth
    def prepare_fetch_spies( self, on_body_id:int, to_body_id:int, *args, **kwargs ):
        """ Fetches spies back home again.

        Arguments:
            - on_body_id -- Integer ID of the body the spies are currently on (the foreign planet).
            - to_body_id -- Integer ID of the body to which you wish to send the spies (their home planet)
        
        Returns a tuple:
            - ship_list -- List of :class:`lacuna.ship.ExistingShip` objects
            - spy_list -- List of :class:`lacuna.spy.Spy` objects
        """
        ship_list = []
        for i in kwargs['rslt']['ships']:
            ship_list.append( lacuna.ship.ExistingShip(self.client, i) )
        spy_list = []
        for i in kwargs['rslt']['spies']:
            spy_list.append( lacuna.spy.Spy(self.client, i) )
        return(
            ship_list,
            spy_list
        )

    @lacuna.building.MyBuilding.call_naked_returning_meth
    def fetch_spies( self, on_body_id:int, to_body_id:int, ship_id:int, spy_ids:list, *args, **kwargs ):
        """ Fetches spies back home again.

        Arguments:
            - on_body_id -- Integer ID of the body the spies are currently on 
              (the foreign planet).
            - to_body_id -- Integer ID of the body to which you wish to send the 
              spies (their home planet)
        
        Returns the :class:`lacuna.ship.TravellingShip` object of the ship 
        fetching the spies.
        """
        return lacuna.ship.TravellingShip(self.client, kwargs['rslt']['ship'])

    @lacuna.building.MyBuilding.call_returning_meth
    def view_battle_logs( self, page_number:int = 1, *args, **kwargs ):
        """ View battle logs.

        Arguments:
            - page_number -- Optional integer number of page to view.  25 log 
              entries displayed per page.  Defaults to 1.

        Returns a tuple:
            - battle_log -- List of :class:`BattleLog` objects
            - number_of_logs -- Integer total number of entries in the logbook.
        """
        mylist = []
        for i in kwargs['rslt']['battle_log']:
            mylist.append( BattleLog(self.client, i) )
        return(
            mylist, 
            self.get_type(kwargs['rslt']['number_of_logs'])
        )


    ### 
    ### Non-API methods
    ###

    def get_task_ships_for( self, target:dict, task:str = 'available' ):
        """ Get ships assigned to a specific task.  

        Arguments:
            - target -- :ref:`standard target dict <gloss_target>`
            - task -- String; ships performing this task will be returned.  One 
              of ``available``, ``incoming``, ``orbiting``, ``mining_platforms``, 
              ``unavailable``.

        Returns a list of ships assigned to a specific task.  
        """
        inc, avail, unavail, orbit, mining, fleet_limit = self.get_my_ships_for( target )
        if task == 'available':
            return avail
        elif task == 'incoming':
            return inc
        elif task == 'orbiting':
            return orbit
        elif task == 'mining_platforms':
            return mining
        elif task == 'unavailable':
            return unavail
        else:
            raise SyntaxError("A valid task must be passed to get_task_ships_for().")
            
    def get_spies_back( self, from_id:int, ship_name:str = '' ):
        """ Fetches all spies currently posted to a planet back home again.

        Arguments:
            - on_body_id -- Integer ID of the body from which you want to 
              retrieve your spies.
            - ship_name -- Optional; name of the ship you want to use to 
              retrieve your spies.  If not sent, the fastest available ship will 
              be used.

        Returns a tuple:
            - ship -- :class:`lacuna.ship.TravellingShip` object
            - spy_ids -- List of integer IDs of spies being fetched (NOT a list 
              of Spy objects).

        **Warning** - the returned list of spy_ids will only ever contain a maximum 
        of 100 spies.  In the situation where you've sent hundreds of spies from 
        multiple planets all to the same target (eg to defend a space station 
        that's under attack), the spies from this planet may not be included in 
        that list.

        What you need to do in this case is to just fetch the spies who _are_ 
        showing up in that list, wait for the ship to actually pick them up and 
        remove them from the target planet, then try again.

        Raises :class:`lacuna.exceptions.MissingResourceError` if no spies can 
        be found to be picked up.  This is usually because of the warning 
        mentioned above.

        Raises :class:`lacuna.exceptions.NoAvailableShipsError` if you don't 
        have any ships capable of grabbing all of the spies on the target 
        planet in one shot, or if you don't have any spies on foreign soil 
        ready to be picked up (remember that a spy has to be Idle to be picked 
        up).
        """
        ships, spies = self.prepare_fetch_spies( from_id, self.body_id )

        if len(ships) <= 0:
            raise err.NoAvailableShipError("No ships are available to pick up spies.")

        ship_id = 0
        if ship_name:
            for ship in ships:
                if ship.name == ship_name:
                    ship_id = ship.id
                    break
        else:
            ships.sort( key=operator.attrgetter('speed'), reverse=True )

            ship = ''
            for s in ships:
                if hasattr(s, 'max_occupants'):
                    if s.max_occupants > len(spies):
                        ship = s
                        break
            if not ship:
                raise err.NoAvailableShipError("You have no ships capable of carrying all of your spies.")
            ship_id = ships.pop().id

        spy_ids = []
        for i in spies:
            if i.based_from.body_id == self.body_id and i.assigned_to.body_id == from_id:
                spy_ids.append( i.id )
        if len(spy_ids):
            ship = self.fetch_spies( from_id, self.body_id, ship_id, spy_ids )
        else:
            raise err.MissingResourceError("I couldn't find any spies to pick up.")

        return(
            ship,
            spy_ids
        )

class BattleLog(lacuna.bc.SubClass):
    """
    Attributes::

        date                "06 21 2011 22:54:37 +0600",
        attacking_body      "Romulus",
        attacking_empire    "Romulans",
        attacking_unit      "Sweeper 21",
        defending_body      "Kronos",
        defending_empire    "Klingons",
        defending_unit      "Shield Against Weapons",
        victory_to          "defender"
    """

class MiningPlatform(lacuna.bc.SubClass):
    """ A mining platform is a mining platform ship that has successfully 
    arrived at an asteroid and converted itself into a mining platform.  The 
    platform itself is no longer actually a ship, and does not have a name or ID
    of its own.

    This class exists in the spaceport module because this is the only place 
    that this format is used.

    Attributes::

        empire_id       ID of your empire, NOT of the ship
        empire_name     Name of your empire, NOT of the ship
    """
