
import lacuna, lacuna.binutils.libbin, lacuna.types
import lacuna.exceptions as err
import argparse, operator, os, sys

class TrainableSpies():
    def __init__( self ):
        self.collection = {}     # spy_id: spy_object

    def add( self, spy ):
        self.collection[ spy.id ] = spy

    def delete(self, spy = None, id = None):
        if spy:
            del self.collection[ spy.id ]
        elif id:
            del self.collection[ id ]
        else:
            raise ValueError("del requires either a spy object or an integer spy ID.")

    def get_byid(self, id):
        return self.collection[ id ]

    def get_highest(self, skill, num = 90):
        """ Returns the num spies highest-ranked in skill.

        You're probably going to want a num of 90 most of the time.  
        Even if you only really want 10, the first 10 might be maxed in the 
        desired skill.  And the next 10 might be too, etc.
        Returns a list of spy objects.
        """
        return sorted( self.collection.values(), key=operator.attrgetter(skill), reverse=True )[0:num]

    def get_lowest(self, skill, num = 90):
        """ Returns the num spies lowest-ranked in skill.

        You're probably going to want a num of 90 most of the time.  
        Even if you only really want 10, the first 10 might be maxed in the 
        desired skill.  And the next 10 might be too, etc.
        Returns a list of spy objects.
        """
        return sorted( self.collection.values(), key=operator.attrgetter(skill), reverse=False )[0:num]


class Location():
    """
    Attributes::

        coll    TrainableSpies object
        bldgs   Dict.
                { 'intel': {
                                'obj': inteltraining object if the building exists on this colony,
                                'num': integer number of spies training here.
                            },
                    'mayhem': { same format as above, },
                    'politics': { same format as above, },  
                    'theft': { same format as above, },     }
    """
    def __init__( self, bldgs:dict ):
        self.coll   = TrainableSpies()
        self.bldgs  = bldgs

    def add_spy( self, spy ):
        self.coll.add( spy )

    def can_train( self, skill:str ):
        return True if skill in self.bldgs else False

    def add_train( self, skill:str ):
        self.bldgs[skill]['num'] += 1

    def num_training( self, skill:str ):
        if skill in self.bldgs:
            return self.bldgs[skill]['num']
        else:
            return 0


class TrainSpies(lacuna.binutils.libbin.Script):
    """ Train spies in bulk.
    """
    skills = [ 'intel', 'mayhem', 'politics', 'theft' ]

    def __init__(self):
        self.version = '0.1'

        parser = argparse.ArgumentParser(
            description = 'Assigns spies to a new training task, in bulk.',
            epilog      = "Full docs can be found at http://tmtowtdi.github.io/MontyLacuna/scripts/assign_spies.html",
        )
        parser.add_argument( 'name', 
            metavar     = '<planet>',
            action      = 'store',
            help        = "Train spies based on this planet.  Pass 'all' to train all planets' spies."
        )
        parser.add_argument( 'skill', 
            metavar     = '<skill>',
            action      = 'store',
            choices     = [ 'all' ] + self.skills,
            help        = "Skill the spies should be trained in.  One of 'intel', 'mayhem', 'politics', 'theft', or 'all'."
        )
        parser.add_argument( '--num', 
            metavar     = '<number>',
            action      = 'store',
            type        = int,
            default     = 10,
            help        = "Number of spies to train.  Defaults to 10."
        )
        parser.add_argument( '--lvl', 
            metavar     = '<level>',
            action      = 'store',
            choices     = [ 'good', 'bad' ],
            default     = 'good',
            help        = "Should we train the spies who already have a high level in this skill to get them to their max ('good'), or spies with the lowest level in this skill to get everybody at least partially up to speed ('bad')?  Defaults to 'good'."
        )
        parser.add_argument( '--fresh', 
            action      = 'store_true',
            help        = "Clears the cache from previous runs to ensure you're seeing fresh data.  Normally not needed for this script."
        )
        super().__init__(parser)

        self.planets    = []
        self.planet     = None      # set by set_planet
        self.intmin     = None      # set by set_intmin
        self.locations  = {}        # body name: Location object.  Set by _populate_locations()

        if self.args.fresh:
            self.client.cache_clear( 'my_colonies' )
            self.client.cache_clear( 'train_spies' )

        self._set_planets()


    def _set_planets( self ):
        self.client.cache_on( 'my_colonies', 3600 )
        self.planets = []
        if self.args.name == 'all':
            for colname in sorted( self.client.empire.colony_names.keys() ):
                self.planets.append(colname)
        else:
            self.planets = [self.args.name]
        self.client.cache_off()

    def _locate_spies( self ):
        """ Finds all Idle spies based on self.planet, and organizes them by their 
        current locations.  Populates self.locations.
        """
        self.client.cache_on( 'train_spies', 3600 )
        all_spies = self.intmin.view_all_spies()
        self.client.cache_off()

        for s in all_spies:
            if s.assignment != "Idle":
                self.client.user_logger.debug( "{} is doing {} so he's not trainable."
                    .format(s.name, s.assignment) )
                continue

            locname = s.assigned_to.name
            if locname not in self.planets:
                self.client.user_logger.debug( "{} is on {}, which is not one of my colonies, so he's not trainable."
                    .format(s.name, locname) )
                continue
            self._populate_locations( locname )

            if self.args.skill == 'all':
                if s.intel >= 2600 and s.mayhem >= 2600 and s.politics >= 2600 and s.theft >= 2600:
                    self.client.user_logger.debug( "{} is fully maxed in all skills, so he's not trainable."
                        .format(s.name) )
                    continue
            else:
                if getattr(s, self.args.skill) >= 2600:
                    self.client.user_logger.debug( "{} is fully maxed in {}, so he's not trainable."
                        .format(s.name, self.args.skill) )
                    continue

            self.client.user_logger.debug( "YAY! {} is trainable." .format(s.name) )
            if self.locations[locname]:
                locobj = self.locations[locname]
                locobj.add_spy( s )

    def _populate_locations( self, pname:str ):
        """ If a Location object already exists for pname, this does nothing.
        If not, this creates one, setting self.locations[ pname ].

        It's possible that self.locations[ pname ] will end up getting set to 
        None, if it doesn't have any training buildings with slots ready to go, 
        so test that before using it.
        """
        if pname in self.locations:
            return

        bldgs_to_check = []
        if self.args.skill == 'all':
            bldgs_to_check = self.skills
        else:
            bldgs_to_check = [ self.args.skill ]

        bldgs = {}
        self.client.cache_on( 'train_spies', 3600 )
        for s in bldgs_to_check:
            bname = s + 'training'
            self.client.user_logger.info( "Looking for {} building on {}...".format(bname, self.planet.name) )
            try:
                obj = self.planet.get_buildings_bytype( bname, 1, 1, 100 )[0]
                self.client.user_logger.info( "...Got it!".format(bname, self.planet) )
                view = obj.view()
                if view.in_training >= self.args.num:
                    self.client.user_logger.info( "But it's already training its max number of spies." )
                    continue
                bldgs[ s ] = {
                    'obj': obj,
                    'num': view.in_training
                }
            except err.NoSuchBuildingError as e:
                self.client.user_logger.info( "...Nope." )
                continue

        self.client.cache_off()
        if bldgs:
            self.locations[pname] = Location( bldgs )
        else:
            self.locations[pname] = None

    def set_planet( self, pname:str ):
        """ Sets the current working planet by name.

        Arguments:
            - pname -- String name of the planet to set.
        """
        self.client.cache_on( 'my_colonies', 3600 )
        self.planet = self.client.get_body_byname( pname )
        self.client.cache_off()
        self.locations = {}     # clear this for each new planet

    def set_intmin( self ):
        """ Finds the Intelligence Ministry on the current planet.  Must be 
        called after set_planet().  Also organizes spies by location.

        Raises :class:`lacuna.exceptions.NoSuchBuildingError` if the planet 
        being set does not have a working Intelligence Ministry.
        """
        self.intmin = self.planet.get_buildings_bytype( 'intelligence', 1, 1, 100 )[0]
        self._locate_spies()

    def train_spies_at( self, pname:str, loc:Location ):
        skills = []
        if self.args.skill == 'all':
            skills = self.skills
        else:
            skills = [ self.args.skill ]

        for s in skills:
            if not loc.can_train(s):
                continue
            if loc.num_training(s) > self.args.num:
                continue
            num = self._train_spies_in( s, loc )
            self.client.user_logger.info( "Set {} spies on {} to train in {}."
                .format(num, pname, s) )

    def _train_spies_in( self, skill:str, loc:Location ):
        trained = 0
        spies = []
        if self.args.lvl == 'good':
            spies = loc.coll.get_highest(skill)
        else:
            spies = loc.coll.get_lowest(skill)

        self.client.user_logger.info( "Training spies in {}.".format(skill) )
        for s in spies:
            if getattr(s, skill) >= 2600:
                self.client.user_logger.debug( "{} already has a {} score of 2600.  Skipping."
                    .format(s.name, skill)
                )
                continue
            self.client.user_logger.debug( "Training {} in {}.".format(s.name, skill) )
            ### skill is eg 'intel'.  To assign, we need "Intel Training".
            training_name = (skill + " training").title()
            self.intmin.assign_spy( s.id, training_name )
            trained += 1
            loc.coll.delete( s )                    # remove this spy from the pool of TrainableSpies
            loc.add_train(skill)                    # increment this building's "currently training" number
            if loc.num_training(skill) >= self.args.num:
                break

        if trained > 0:
            ### The data we cached earlier is no longer valid; clear it.
            self.client.cache_clear('train_spies')
        return trained

