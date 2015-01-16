
import lacuna, lacuna.binutils.libbin
import lacuna.exceptions as err
import argparse, operator, os, sys

class AssignSpies(lacuna.binutils.libbin.Script):
    """ Assigns spies to a task, in bulk.

    Shares cache data with libspies_report.py, as that will often be run just 
    before this.
    """

    def __init__(self):
        self.version = '0.1'

        ### The planet that the spies need to be on to perform the requested 
        ### task.  This will usually be the same as self.args.on, or 
        ### self.args.name (if the --on argument was not sent).
        ### However, if the user passed 'all' as the planet name in --on, we 
        ### need to translate that into an actual planet name.
        ### So self.args.on is not guaranteed to be a planet name, but self.on 
        ### is.
        self.on = ''

        ### The maximum number of spies from any given planet to assign to the 
        ### task.  If --topoff is not sent, this stays at 90 (the max).
        self.max = 90

        self.tasks = {
            ### 'lower case or abbreviation': 'Full taskname, properly cased'
            ###
            ### Training tasks omitted -- training should be its own script.
            'idle': 'Idle',
            'bugout': 'Bugout',
            'counter espionage': 'Counter Espionage',
            'counter': 'Counter Espionage',
            'security sweep': 'Security Sweep',
            'political propaganda': 'Political Propaganda',
            'pp': 'Political Propaganda',
            'prop': 'Political Propaganda',
            'gather resource intelligence': 'Gather Resource Intelligence',
            'gather resint': 'Gather Resource Intelligence',
            'get resint': 'Gather Resource Intelligence',
            'gather empire intelligence': 'Gather Empire Intelligence',
            'gather empint': 'Gather Empire Intelligence',
            'get empint': 'Gather Empire Intelligence',
            'gather operative intelligence': 'Gather Operative Intelligence',
            'gather opint': 'Gather Operative Intelligence',
            'get opint': 'Gather Operative Intelligence',
            'hack network 19': 'Hack Network 19',
            'hack': 'Hack Network 19',
            'hack net19': 'Hack Network 19',
            'sabotage probes': 'Sabotage Probes',
            'sab probes': 'Sabotage Probes',
            'rescue comrades': 'Rescue Comrades',
            'rescue': 'Rescue Comrades',
            'sabotage resources': 'Sabotage Resources',
            'sabotage res': 'Sabotage Resources',
            'sab res': 'Sabotage Resources',
            'appropriate resources': 'Appropriate Resources',
            'appropriate res': 'Appropriate Resources',
            'app res': 'Appropriate Resources',
            'assassinate operatives': 'Assassinate Operatives',
            'ass op': 'Assassinate Operatives',
            'kill': 'Assassinate Operatives',
            'sabotage infrastructure': 'Sabotage Infrastructure',
            'sab infra': 'Sabotage Infrastructure',
            'sabotage defenses': 'Sabotage Defenses',
            'sab def': 'Sabotage Defenses',
            'sabotage bhg': 'Sabotage BHG',
            'sab bhg': 'Sabotage BHG',
            'incite mutiny': 'Incite Mutiny',
            'mutiny': 'Incite Mutiny',
            'abduct operatives': 'Abduct Operatives',
            'abduct op': 'Abduct Operatives',
            'kidnap': 'Abduct Operatives',
            'appropriate technology': 'Appropriate Technology',
            'app tech': 'Appropriate Technology',
            'incite rebellion': 'Incite Rebellion',
            'rebellion': 'Incite Rebellion',
            'rebel': 'Incite Rebellion',
            'incite insurrection': 'Incite Insurrection',
            'insurrection': 'Incite Insurrection',
            'insurrect': 'Incite Insurrection',
            'insurect': 'Incite Insurrection',
        }

        parser = argparse.ArgumentParser(
            description = 'Assigns spies to a new task, in bulk.',
            epilog      = "Full docs can be found at http://tmtowtdi.github.io/MontyLacuna/scripts/assign_spies.html",
        )
        parser.add_argument( 'name', 
            metavar     = '<planet>',
            action      = 'store',
            help        = 'Assign tasks to spies from this planet.  The script will raise an exception if the requested planet does not have a working Intelligence Ministry.'
        )
        parser.add_argument( 'task', 
            metavar     = '<task>',
            action      = 'store',
            choices     = self.tasks.keys(),
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
            help        = "Only assigns spies who are currently doing this task.  Usually only Idle spies can be assigned, but if you're wanting to eg set your Counter Espionage spies to Idle, pass 'Counter Espionage' here.  Defaults to 'Idle'."
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
            help        = "Only assigns spies who are located on this planet.  Defaults to the spies' home planet, so you'll definitely need to change this for offensive tasks."
        )
        parser.add_argument( '--top', 
            metavar     = '<attribute>',
            action      = 'store',
            type        = str,
            default     = 'level',
            choices     = [ 'level', 'politics', 'mayhem', 'theft',
                            'intel', 'offense_rating', 'defense_rating', ],
            help        = "If you have more spies available than you're assigning, this determines which spies get assigned.  Sending a --top of 'intel' will available spies with the highest intel score to the requested task.  Defaults to 'level'."
        )
        super().__init__(parser)
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
            self.on = self.args.on
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
            if spy.assignment == self.get_task( self.args.task ) and spy.assigned_to.name == self.on:
                currently_on_requested_task += 1
        self.max = self.args.num - currently_on_requested_task
        if self.max <= 0:
            raise err.TopoffError(currently_on_requested_task, "Over topoff limit.")

    def get_task( self, task_cand:str ):
        """ Gets the full TLE name of a task, correcting for abbreviations and 
        incorrect casing.

        Arguments:
            - task_cand -- String taskname as provided by the user.  May be an 
              abbreviation and casing does not matter.

        Returns a string -- the properly cased and spelled TLE Spy task name.
        """
        if task_cand.lower() in self.tasks:
            return self.tasks[ task_cand.lower() ]
        raise Exception("'{}' is not a valid task or abbreviation.".format(task_cand))

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
                if self.get_task( self.args.task ) == a.task:
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
            if self.get_task( self.args.doing ) == s.assignment:
                valid.append( s )
        if not valid:
            raise err.NoUsableSpiesError("You have no usable spies currently performing the {} task.".format(self.args.doing))
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
                self.intmin.assign_spy( s.id, self.get_task(self.args.task) )
                self.client.user_logger.debug( "Assigning spy on {} to {}.".format(self.on, self.args.task) )
                cnt += 1
            except err.ServerError as e:
                self.client.user_logger.info( "Spy {} could not be assigned to {} because {}.".format(s.name, self.args.task, e.text) )
                continue
        if cnt > 0:
            self.client.cache_clear( 'spies' )
        return cnt

