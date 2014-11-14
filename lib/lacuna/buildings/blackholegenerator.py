
"""
    Several BHG methods include a 'target' argument.  This is the same target 
    argument used by the Space Port.  It's a dict that can contain:
    - body_id -- "12345",
    - body_name -- "mars",
    - star_id -- "12345",
    - star_name -- "sol",
    - zone -- "0|0",
    - x -- 0,
    - y -- 0,

    You'll only send one of those keys, except in the case where you're sending 
    coordinates, in which case you'll send both 'x' and 'y'.

    Not all of the target keys listed above will be appropriate for all calls; 
    eg sending 'star_name' to a call to 'jump_zone' doesn't make any sense.
"""

import lacuna.bc
from lacuna.building import MyBuilding

class blackholegenerator(MyBuilding):
    path = 'blackholegenerator'

    def __init__( self, client, body_id:int = 0, building_id:int = 0 ):
        super().__init__( client, body_id, building_id )

    @MyBuilding.call_returning_meth
    def get_actions_for( self, target:dict, **kwargs ):
        """ Returns all available BHG actions for the given target.

        Actually returns all BHG actions, but any that aren't possible for the 
        current target will have a 'reason' listed.

        Returns a list of BHGTask objects.
        """
        mylist = []
        for i in kwargs['rslt']['tasks']:
            mylist.append( BHGTask(self.client, i) )
        return mylist

    @lacuna.bc.LacunaObject.set_empire_status
    @MyBuilding.call_building_meth
    def subsidize_cooldown( self, **kwargs ):
        """ Spends 2E to subsidize the BHG's current cooldown period.

        Returns a tuple:
            - tasks -- List of BHGTask objects
            - task_options -- A single BHGTaskOptions object

        Raises ServerError 1010 if the BHG is not currently in cooldown mode.
        """
        tasks = []
        for i in kwargs['rslt']['tasks']:
            tasks.append( BHGTask(self.client, i) )
        opts = BHGTaskOptions(self.client, kwargs['rslt']['task_options'])
        return( tasks, opts )


    @MyBuilding.call_named_returning_meth
    def generate_singularity( self, named_args:dict, **kwargs ):
        """ Performs one of the several actions possible via BHG.  See 
        get_actions_for() for a list of legal actions.

        Arguments must be passed in a dict.  The server method does support 
        positional arguments, but that form is deprecated, and does not 
        support subsidizing the action, so this method is purposely not 
        supporting positional arguments at all.

        Format for named_args:

::

            {   "target"        : { "body_name" : "mars" },
                "task_name"     : "Change Type",
                "params"        : { "newtype" : 33 },
                "subsidize"     : 1     }

        Setting subsidize to 1 spends E to subsidize the action.  Setting 
        subsidize to a 0 is very much not recommended.  When you do this, you 
        take the chance that the BHG action will fail, causing catastrophic 
        results up to destroying the BHG and replacing it with a fissure.

        Returns a single BHGEffect object.

        Throws ServerError 1002 if the target can't be found, and 1010 if the 
        BHG is currently in cooldown mode.
        """
        return BHGEffect(self.client, kwargs['rslt']['effect'])


class BHGTask(lacuna.bc.SubClass):
    """
    Attributes:
        >>> 
        base_fail       10,
        dist            134.1
        essentia_cost   None,
        min_level       10,
        name            'Make Asteroid',
        occupied        0,
        range           450,
        reason          'You can only make an asteroid from a planet.',
        recovery        259200,
        side_chance     25,
        subsidy_mult    0.75,
        success         0,
        throw           1009,
        types           ['habitable planet', 'gas giant'],
        waste_cost      50000000
    """

class BHGTaskOptions(lacuna.bc.SubClass):
    """
    Attributes:
        >>> 
        asteroid_types  [1, 2, ... 26],
        planet_types    [1, 2, .., 40],
        zones           ['-1|-1', '-1|-2', ... '5|5']
    """


class BHGEffect(lacuna.bc.SubClass):
    """
    Attributes:
        >>> 
        ore_capacity        21893730088,
        ore_hour            2593539143,
        ore_stored          21893730088,
        plots_available     0,
        population          30100000,
        propaganda_boost        '0',
        size                '72',
        star_id             "My Planet's Star's ID",
        star_name           "My Planet's Star's Name",
        surface_version     '2774',
        type                'habitable planet',
        waste_capacity      63944937008,
        waste_hour          117395,
        waste_stored        16747563792,
        water               10768,
        water_capacity      21893730088,
        water_hour          1348906217,
        water_stored        21893730088,
        x                   'x coord of planet containing BHG',
        y                   'y coord of planet containing BHG',
        zone                '0|0',

    The 'side' dict specifies any side effects that occurred as a result 
    of your BHG use.  I believe this will only be set if the BHG usage 
    produced a side effect.
    - id -- '121808',
    - message -- '2 decor items placed',
    - name -- 'Name of affected planet',  },

    The 'fail' dict is listed in the TLE docu as "fail: { ... }", so I 
    don't know what it's supposed to contain.  It'll only be set if the 
    BHG usage failed for some reason.

    The 'target' dict will contain different keys depending upon what was 
    done.

    This first example is what's documented in the TLE API docu:
        - class -- 'Lacuna::DB::Result::Map::Body::Asteroid::A2',
        - id -- 'body id',
        - name -- 'name of planet effected',
        - old_class -- 'Lacuna::DB::Result::Map::Body::Planet::P9',
        - old_size -- Size before change,
        - message -- 'Made Asteroid',
        - size -- Size of body after effect
        - type -- 'asteroid', 'gas giant', 'habitable planet', or 'space station'
        - variance -- -1, 0, or 1
        - waste -- 'Zero', 'Random', or 'Filled'

    This is what I got back after trying to change a p35 into a p35:
        - id -- '467277',
        - message -- 'Fizzle',
        - name -- 'Opriogee 2'

    This is what I got back after changing a p35 into a p33:
        - class -- 'Lacuna::DB::Result::Map::Body::Planet::P33',
        - id -- '467277',
        - message -- 'Changed Type',
        - name -- 'Opriogee 2',
        - old_class -- 'Lacuna::DB::Result::Map::Body::Planet::P35'

    ...So use your head, and check your keys.
    """

