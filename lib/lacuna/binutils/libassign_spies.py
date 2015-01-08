
### search on CHECK

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
        self.tasks = {
            ### 'lower case': 'proper casing'
            ###
            ### Asking people to spell and case these things correctly is 
            ### likely to cause all kinds of issues.  Provide aliases using 
            ### likely misspellings and abbreviations.
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
            epilog      = "EXAMPLE python bin/assign_spies.py Earth counter",
        )
        parser.add_argument( 'name', 
            metavar     = '<planet>',
            action      = 'store',
            help        = 'Assign tasks to spies from this planet.  The script will raise an exception if the requested planet does not have a working Intelligence Ministry.'
        )
        parser.add_argument( 'task', 
            metavar     = '<task>',
            action      = 'store',
            choices     = self.tasks.values(),
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
            choices     = [
                            'level',
                            'politics',
                            'mayhem',
                            'theft',
                            'intel',
                            'offense_rating',
                            'defense_rating',
                          ],
            help        = "If you have more spies available than you're assigning, this determines which spies get assigned.  Sending a --top of 'intel' will available spies with the highest intel score to the requested task.  Defaults to 'level'."
        )
        super().__init__(parser)

        ### If the user didn't specify where the spies should be located, he 
        ### means the spies at home.
        if not self.args.on:
            self.args.on = self.args.name

        if self.args.name == 'all' and self.get_task() == 'Counter Espionage':
            ### CHECK
            ### This might not be exactly the right way to do this, and the 
            ### method below doesn't exist yet, but it's the general idea of 
            ### what I want to add.
            self.assign_all_idle_to_counter()
            quit()

        self._set_planet( self.args.name )
        self._set_intmin( )
        self._gather_spy_data( )

    def get_task( self ):
        if self.args.task.lower() in self.tasks:
            return self.tasks[ self.args.task.lower() ]
        raise Exception("'{}' is not a valid task or abbreviation.".format(self.args.task))

    def _set_planet( self, pname:str ):
        self.planet = self.client.get_body_byname( pname )

    def _set_intmin( self ):
        """ Finds the Intelligence Ministry on the current planet.  Must be 
        called after set_planet()

        Raises :class:`lacuna.exceptions.NoSuchBuildingError` if the planet 
        being set does not have a working Intelligence Ministry.
        """
        self.intmin = self.planet.get_buildings_bytype( 'intelligence', 1, 1, 100 )[0]

    def _gather_spy_data( self ):
        """ Get data on all of the spies at our planet.  Must be called after 
        :meth:`lacuna.binutils.libspies_report.SpiesReport.set_planet`.
        """
        self.client.cache_on( 'spies', 3600 )
        self.all_spies  = self.intmin.view_all_spies()  # remains constant
        self.spies      = self.all_spies                # changes based on filters
        self.client.cache_off()

    def set_spies_on_target( self ):
        """ Set spies located on the target specified by the ``--on`` option, 
        or the current planet if no ``--on`` option was passed.
        """
        valid = []
        for s in self.spies:
            if s.assigned_to.name.lower() == self.args.on.lower():
                valid.append( s )
        if not valid:
            raise Exception("You have no usable spies on {}.".format(self.args.on))
        self.spies = valid

    def set_able_spies( self ):
        """ Set spies able to perform the specified by the ``task`` argument.
        """
        valid = []
        for s in self.spies:
            for a in s.possible_assignments:
                if self.get_task() == a.task.lower():
                    valid.append( s )
        if not valid:
            raise Exception("You have no usable spies able to perform the {} task.".format(self.args.task))
        self.spies = valid

    def set_spies_doing_correct_task( self ):
        """ Set spies currently performing the task specified by the ``--doing`` 
        option, or "Idle" if no ``--doing`` option was passed.
        """
        valid = []
        for s in self.spies:
            if s.assignment.lower() == self.self.get_task():
                valid.append( s )
        if not valid:
            raise Exception("You have no usable spies currently performing the {} task.".format(self.args.doing))
        self.spies = valid

    def set_best_spies( self ):
        """ If we've got more spies available than requested, set only the 
        ``--top`` ``--num`` spies.
        """
        if len(self.spies) > self.args.num:
            end = self.args.num if self.args.num else None
            self.spies = sorted( self.spies, key=operator.attrgetter(self.args.top) )[0:end]

    def assign_spies( self ):
        """ Assigns our spies to the requested task.  Assumes all desired 
        filters have already been processed.
        """
        if not self.spies:
            ### "shouldn't" ever happen.  But then, lots of things that 
            ### "shouldn't" have ever happened, happened.
            raise Exception("You have no spies able to be assigned.")
        cnt = 0
        for s in self.spies:
            try:
                self.intmin.assign_spy( s.id, self.get_task() )
                cnt += 1
            except err.ServerError as e:
                self.client.user_logger.info( "Spy {} could not be assigned to {} because {}.".format(s.name, self.args.task, e.text) )
                continue
        if cnt > 0:
            self.client.cache_clear( 'spies' )
        return cnt

