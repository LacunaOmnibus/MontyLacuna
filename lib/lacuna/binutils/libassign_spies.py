
import lacuna, lacuna.binutils.libbin, lacuna.types
import lacuna.exceptions as err
import argparse, operator, os, sys

class AssignSpies(lacuna.binutils.libbin.Script):
    """ Assigns spies to a task, in bulk.

    Shares cache data with libspies_report.py, as that will often be run just 
    before this.
    """

    def __init__( self, testargs:dict = {} ):
        self.version = '0.1'

        ### The planet that the spies need to be on to perform the requested 
        ### task.  This will usually be the same as self.args.on, or 
        ### self.args.name (if the --on argument was not sent).
        ### However, if the user passed 'all' as the planet name in --on, we 
        ### need to translate that into an actual planet name.
        ### So self.args.on is not guaranteed to be a planet name, but self.on 
        ### is.
        self.on = ''

        parser = argparse.ArgumentParser(
            description = 'Assigns spies to a new task, in bulk.',
            epilog      = "Full docs can be found at http://tmtowtdi.github.io/MontyLacuna/scripts/assign_spies.html",
        )
        parser.add_argument( 'name', 
            metavar     = '<planet>',
            action      = 'store',
            help        = "Assign tasks to spies from this planet.  Specify 'all' to operate on all of your planets."
        )
        parser.add_argument( 'task', 
            metavar     = '<task>',
            action      = 'store',
            help        = "Task spies should be assigned to."
        )
        parser.add_argument( '--num', 
            metavar     = '<number>',
            action      = 'store',
            type        = int,
            default     = 0,
            help        = "Number of spies to assign.  Sending '0' means 'assign all spies possible to this task'.  Defaults to 0."
        )
        parser.add_argument( '--doing', 
            metavar     = '<task>',
            action      = 'store',
            type        = str,
            default     = 'Idle',
            help        = "Only assign spies currently doing this task.  Defaults to 'Idle'."
        )
        parser.add_argument( '--topoff', 
            dest        = 'topoff',
            action      = 'store_true',
            help        = "If --topoff is sent, the script will ensure that at least --num spies are performing the requested task."
        )
        parser.add_argument( '--on', 
            metavar     = '<planet_name>',
            action      = 'store',
            type        = str,
            help        = "Only assign spies located on this planet.  Defaults to the spies' home planet."
        )
        parser.add_argument( '--fresh', 
            action      = 'store_true',
            help        = "Clear cache to ensure fresh data."
        )
        parser.add_argument( '--top', 
            metavar     = '<attribute>',
            action      = 'store',
            type        = str,
            default     = 'level',
            choices     = [ 'level', 'politics', 'mayhem', 'theft',
                            'intel', 'offense_rating', 'defense_rating', ],
            help        = "Assign spies with the highest score in this attribute.  Defaults to 'level'."
        )
        super().__init__( parser, testargs = testargs )

        self.max        = 90
        self.planet     = None
        self.intmin     = None
        self.all_spies  = []
        self.spies      = []

        ### self.args.(task|doing) will be the string that the user entered, 
        ### but self.(task|doing) will be the translation of that string.  You 
        ### almost always want to use the translation.
        self.trans  = lacuna.types.Translator()
        self.task   = self.trans.translate_assgtype( self.args.task )
        self.doing  = self.trans.translate_assgtype( self.args.doing )
        self.set_planets()

        if self.args.fresh:
            self.client.cache_clear( 'my_colonies' )
            self.client.cache_clear( 'spies' )

    def _set_intmin( self ):
        """ Finds the Intelligence Ministry on the current planet.  Must be 
        called after set_planet()

        Raises :class:`lacuna.exceptions.NoSuchBuildingError` if the planet 
        being set does not have a working Intelligence Ministry.
        """
        self.intmin = self.planet.get_buildings_bytype( 'intelligence', 1, 1, 100 )[0]

    def _gather_spy_data( self ):
        """ Get data on all of the spies at the planet set by 
        :meth:`lacuna.binutils.libspies_report.SpiesReport.set_planet`.
        """
        self.client.cache_on( 'spies', 3600 )
        self.all_spies  = self.intmin.view_all_spies()  # remains constant
        self.spies      = self.all_spies                # changes based on filters
        self.client.cache_off()

    def set_planet( self, pname:str ):
        """ Sets the current working planet by name.

        Arguments:
            - pname -- String name of the planet to set.
        """
        self.client.cache_on( 'my_colonies', 3600 )
        self.planet = self.client.get_body_byname( pname )
        self.client.cache_off()
        self._set_intmin( )
        self._gather_spy_data( )
        ### If the user didn't specify where the spies should be located, he 
        ### means those located at their home planets.
        if self.args.on:
            self.on = self.abbrv.get_name( self.args.on )
        else:
            self.on = pname
        self.max = 90           # gotta reset in case the last planet mangled this.

    def check_topoff( self ):
        """ If the user just wants to topoff, usually for Counter Espionage, 
        check how many spies are already performing that task and set how many 
        more should be assigned.
        """
        if not self.args.topoff:
            return
        currently_on_requested_task = 0
        for spy in self.all_spies:
            if spy.assignment == self.task and spy.assigned_to.name == self.on:
                currently_on_requested_task += 1
        self.max = self.args.num - currently_on_requested_task
        if self.max <= 0:
            raise err.TopoffError(currently_on_requested_task, "Over topoff limit.")

    def set_spies_on_target( self ):
        """ Set spies located on the target specified by the ``--on`` option, 
        or the current planet if no ``--on`` option was passed.
        """
        valid = []
        for s in self.spies:
            if s.assigned_to.name.lower() == self.on.lower():
                valid.append( s )
        if not valid:
            raise err.NoUsableSpiesError("You have no usable spies on {}.".format(self.on))
        self.spies = valid

    def set_able_spies( self ):
        """ Set spies able to perform the specified by the ``task`` argument.
        """
        valid = []
        for s in self.spies:
            for a in s.possible_assignments:
                if self.task == a.task:
                    valid.append( s )
        if not valid:
            raise err.NoUsableSpiesError("You have no usable spies able to perform the {} task.".format(self.args.task))
        self.spies = valid

    def set_spies_doing_correct_task( self ):
        """ Set spies currently performing the task specified by the ``--doing`` 
        option, or "Idle" if no ``--doing`` option was passed.
        """
        valid = []
        for s in self.spies:
            if self.doing == s.assignment:
                valid.append( s )
        if not valid:
            raise err.NoUsableSpiesError("You have no usable spies currently performing the {} task.".format(self.doing))
        self.spies = valid

    def set_best_spies( self ):
        """ If we've got more spies available than requested, set only the 
        ``--top`` ``--num`` spies.
        """
        if len(self.spies) > self.args.num:
            end = self.args.num if self.args.num else None
            ### Sort in reverse order so the guys with the best --top score 
            ### show first in the list.
            self.spies = sorted( self.spies, key=operator.attrgetter(self.args.top), reverse=True )[0:end]

    def assign_spies( self ):
        """ Assigns our spies to the requested task.  Assumes all desired 
        filters have already been processed.
        """
        if not self.spies:
            ### "shouldn't" ever happen.  But then, lots of things that 
            ### "shouldn't" have ever happened, happened.
            raise Exception("You have no spies able to be assigned.")
        cnt = 0
        spies_to_assign = self.spies[0:self.max]
        for s in spies_to_assign:
            try:
                spy, rslt = self.intmin.assign_spy( s.id, self.task )
                self.client.user_logger.debug( "Assigning spy {} on {} to {} resulted in {}."
                    .format(spy.name, self.on, self.args.task, rslt.result)
                )
                cnt += 1
            except err.ServerError as e:
                self.client.user_logger.info( "Spy {} could not be assigned to {} because {}.".format(s.name, self.args.task, e.text) )
                continue
        if cnt > 0:
            self.client.cache_clear( 'spies' )
        return cnt

