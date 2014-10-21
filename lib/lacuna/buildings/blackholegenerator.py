
from lacuna.bc import LacunaObject
from lacuna.building import Building

"""
    Several BHG methods include a 'target' argument.  This is a dict, 
    formatted as:

        "target":{
            "body_id" : "12345",
            "body_name" : "mars",

            "star_id" : "12345",
            "star_name" : "sol",

            "zone" : "0|0",

            "x": 0,
            "y": 0,
        },

    You'll only send one of these, except in the case where you're sending 
    coordinates, in which case you'll send both 'x' and 'y'.

    Not all of the target keys listed above will be appropriate for all calls; 
    eg sending 'star_name' to a call to 'jump_zone' doesn't make any sense.
"""

class blackholegenerator(Building):
    path = 'blackholegenerator'

    def __init__( self, client, body_id:int = 0, building_id:int = 0 ):
        super().__init__( client, body_id, building_id )

    @LacunaObject.set_empire_status
    @Building.call_building_meth
    def get_actions_for( self, target:dict, **kwargs ):
        """ Returns all available BHG actions for the given target.

        Actually returns all BHG actions, but any that aren't possible for the 
        current target will have a 'reason' listed.

        Retval contains key 'tasks'.  The example shown is the 'Make Asteroid' 
        task, given a zone as a target, and displays a non-empty 'reason'.
                {   'base_fail': 10,
                    'dist': -1,
                    'essentia_cost': None,
                    'min_level': 10,
                    'name': 'Make Asteroid',
                    'occupied': 0,
                    'range': 450,
                    'reason': 'You can only make an asteroid from a planet.',
                    'recovery': 259200,
                    'side_chance': 25,
                    'subsidy_mult': 0.75,
                    'success': 0,
                    'throw': 1009,
                    'types': ['habitable planet', 'gas giant'],
                    'waste_cost': 50000000
                },
        """
        pass

    @LacunaObject.set_empire_status
    @Building.call_building_meth
    def subsidize_cooldown( self, **kwargs ):
        """ Spends 2E to subsidize the BHG's current cooldown period.

        Retval includes keys 'tasks', as documented in get_actions_for(), and 
        'task_options', a dict:
            {
                'asteroid_types': [1, 2, ... 26],
                'planet_types': [1, 2, .., 40],
                'zones': ['-1|-1', '-1|-2', ... '5|5']
            }
        That's probably not terribly useful, but it's there.

        Raises ServerError 1010 if the BHG is not currently in cooldown mode.
        """
        pass


    @LacunaObject.set_empire_status
    @Building.call_building_named_meth
    def generate_singularity( self, named_args:dict, **kwargs ):
        """ Performs one of the several actions possible via BHG.  See 
        get_actions_for() for a list of legal actions.

        Arguments must be passed in a dict.  The server method does support 
        positional arguments, but that form is deprecated, and does not 
        support subsidizing the action, so this method is purposely not 
        supporting positional arguments at all.

        Format for named_args:
            {   "target"        : { "body_name" : "mars" },
                "task_name"     : "Change Type",
                "params"        : { "newtype" : 33 },
                "subsidize"     : 1     }

        Setting subsidize to 1 spends E to subsidize the action.  Setting 
        subsidize to a 0 is very much not recommended.  When you do this, you 
        take the chance that the BHG action will fail, causing catastrophic 
        results up to destroying the BHG and replacing it with a fissure.

        Retval includes a key 'effect':
                'effect': {
                    'side': {
                        'id': '121808',
                        'message': '2 decor items placed',
                                    'magnetite': 500,
                                    'methane': 500,
                                    'monazite': 500,
                                    'rutile': 500,
                                    'sulfur': 500,
                                    'trona': 500,
                                    'uraninite': 500,
                                    'zircon': 500
                        },
                    'ore_capacity': 21893730088,
                    'ore_hour': 2593539143,
                    'ore_stored': 21893730088,
                    'plots_available': 0,
                    'population': 30100000,
                    'propaganda_boost': '0',
                    'size': '72',
                    'star_id': "My Planet's Star's ID",
                    'star_name': "My Planet's Star's Name",
                    'station': {   'id': 'Integer SS ID',
                                    'name': 'Space Station Name',
                                    'x': 'SS x coord',
                                    'y': 'SS y coord'},
                    'surface_version': '2774',
                    'type': 'habitable planet',
                    'waste_capacity': 63944937008,
                    'waste_hour': 117395,
                    'waste_stored': 16747563792,
                    'water': 10768,
                    'water_capacity': 21893730088,
                    'water_hour': 1348906217,
                    'water_stored': 21893730088,
                    'x': 'x coord of planet containing BHG',
                    'y': 'y coord of planet containing BHG',
                    'zone': '0|0'
                },

            The 'side' dict specifies any side effects that occurred as a 
            result of your BHG use.  The rest of the information in 'effect' 
            is a little puzzling - it reflects the status of the planet where 
            the BHG you just used is located.
            If you, for example, used the BHG to change a foreign planet to a 
            different planet type, you might expect the information in 
            'effect' to relate to that target planet; this is not the case.

        Throws ServerError 1002 if the target can't be found, and 1010 if the 
        BHG is currently in cooldown mode.
        """
        pass



