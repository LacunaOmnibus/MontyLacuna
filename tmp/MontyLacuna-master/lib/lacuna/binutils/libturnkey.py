
import lacuna, lacuna.binutils.libbin, lacuna.types
import lacuna.exceptions as err
import argparse, operator, os, sys

class Turnkey(lacuna.binutils.libbin.Script):
    """ Manages prisoners in either a Security Ministry or Police Station jail.
    """

    def __init__(self):
        self.version = '0.1'

        parser = argparse.ArgumentParser(
            description = 'Manages prisoners in either a Security Ministry or Police Station jail.',
            epilog      = "Full docs can be found at http://tmtowtdi.github.io/MontyLacuna/scripts/turnkey.html",
        )
        parser.add_argument( 'name', 
            metavar     = '<planet>',
            action      = 'store',
            help        = 'Assign tasks to spies from this planet.  The script will raise an exception if the requested planet does not have a working Intelligence Ministry.'
        )
        parser.add_argument( 'task', 
            metavar     = '<task>',
            action      = 'store',
            choices     = [
                            "execute",
                            "release",
                            "view_prisoners",
                            "view_spies",
                          ],
            help        = "Task to perform.  One of 'execute', 'release', 'view_prisoners', or 'view_spies'."
        )
        parser.add_argument( '--page', 
            metavar     = '<number>',
            action      = 'store',
            type        = int,
            default     = 1,
            help        = "25 spies are listed per page.  This determines which page of spies will be displayed/executed/released.  0 means 'show all pages'.  Defaults to 1."
        )
        parser.add_argument( '--num', 
            metavar     = '<number>',
            action      = 'store',
            type        = int,
            default     = 0,
            help        = "Number of spies to execute or release.  Ignored for the 'view' tasks.  0 means 'perform this task for all prisoners'.  Defaults to 0."
        )
        parser.add_argument( '--fresh', 
            action      = 'store_true',
            help        = "If passed, clears the cache before doing anything else to ensure fresh data."
        )
        super().__init__(parser)

        self.body           = ''    # Either a colony or a space station.
        self.prison         = ''    # Either a Sec Min or a Police Station.
        self.task_dispatch  = {}    # Dispatch table to determine which task method to run

        if self.args.fresh:
            self.client.cache_clear( 'my_colonies' )
            self.client.cache_clear( 'prisoners' )

        self._set_body( self.args.name )
        self._set_prison()
        self._set_dispatch()



    def _set_body( self, pname:str ):
        """ Sets the current working planet by name.

        Arguments:
            - pname -- String name of the planet to set.
        """
        self.client.user_logger.info( "Setting working planet to {}.".format(pname) )
        self.client.cache_on( 'my_colonies', 3600 )
        self.body = self.client.get_body_byname( pname )
        self.client.cache_off()

    def _set_prison( self ):
        """ Finds either the Security Ministry or Police Station on the current 
        body, depending on whether that's a colony or a station.
        
        Must be called after _set_body().

        Raises :class:`lacuna.exceptions.NoSuchBuildingError` if the planet 
        being set does not have a working building of the appropriate type.
        """
        bldg = ''
        if self.body.type == 'space station':
            bldg = 'policestation'
        else:
            bldg = 'security'
        self.client.user_logger.debug( "Prison on this body will be a {}.  Grabbing it if it exists...".format(bldg) )

        self.client.cache_on( 'my_colonies', 3600 )
        self.prison = self.body.get_buildings_bytype( bldg, 1, 1, 100 )[0]
        self.client.cache_off
        self.client.user_logger.info( "Got the {}.".format(bldg) )

    def _set_dispatch( self ):
        self.client.user_logger.debug( "Initializing dispatch table." )
        self.task_dispatch = {
            'view_prisoners': self.view_prisoners,
            'view_spies': self.view_foreign_spies,
            'execute': self.execute_prisoners,
            'release': self.release_prisoners,
        }

    def perform_chosen_task( self ):
        """ Call the method indicated by the 'task' option.  If '--page' is 0, 
        calls that method once for each page of results.
        """
        self.client.user_logger.info( "Running the requested task." )
        if self.args.task in self.task_dispatch:
            self.task_dispatch[ self.args.task ]()
        else:
            raise KeyError("Invalid 'task' argument.")

    def _paginate( self, callback, shifter:bool = False ):
        """ A 'shifter' is execute or release of prisoners.  After dealing 
        with the guys on page 1, the view shifts such that the guys who had 
        been on page 2 become the new page 1.  In this case, we don't want to 
        move forward through the pages, or we'll skip every other page.  Just 
        stay with page 1 till it's empty.
        """
        if self.args.page == 0:
            self.client.user_logger.debug( "Displaying all results, paginated." )
            page = 0
            while(True):
                if shifter:
                    page = 1
                else:
                    page += 1
                num = callback( page )
                if num < 25:
                    break
        else:
            self.client.user_logger.debug( "Displaying page {} of results.".format(self.args.page) )
            callback( self.args.page )

    def execute_prisoners( self ):
        """ Execute the prisoners on the selected page.
        """
        self._paginate( self._execute_prisoners_page, True )

    def release_prisoners( self ):
        """ Release the prisoners on the selected page.
        """
        self._paginate( self._release_prisoners_page, True )

    def view_foreign_spies( self ):
        """ View un-captured foreign spies on the selected page.
        """
        self._paginate( self._view_foreign_spies_page )

    def view_prisoners( self ):
        """ View the prisoners on the selected page.
        """
        self._paginate( self._view_prisoners_page )

    def _execute_prisoners_page( self, page ):
        self.client.user_logger.info( "Executing prisoners.".format(self.args.page) )
        ### Make sure the cache is off.  The user might start a multi-page 
        ### run, interrupt it, then come back here.  In which case he'll end 
        ### up trying to execute already-dead prisoners on the >1st run.
        self.client.cache_off();
        pris = self.prison.view_prisoners( page )
        for p in pris:
            self.client.user_logger.debug( "Executing prisoner {} (ID {}).".format(p.name, p.id) )
            self.prison.execute_prisoner( p.id )
        return len(pris)

    def _release_prisoners_page( self, page ):
        self.client.user_logger.info( "Releasing prisoners.".format(self.args.page) )
        self.client.cache_off();    # see comment in _execute_prisoners_page()
        pris = self.prison.view_prisoners( page )
        for p in pris:
            ### I've never actually run this, but since it's essentially 
            ### identical to _execute_prisoners_page(), which I have run, I'm 
            ### going to assume it works.
            self.client.user_logger.debug( "Releasing prisoner {} (ID {}).".format(p.name, p.id) )
            self.prison.release_prisoner( p.id )
        return len(pris)

    def _view_foreign_spies_page( self, page ):
        self.client.user_logger.info( "Viewing foreign spies.".format(self.args.page) )
        self.client.cache_on('prisoners')   # don't change this
        pris = self.prison.view_foreign_spies( page )
        self.client.cache_off();
        tmpl = "{:<20}    {:0>2}    {:<10}    {}"
        print( "Displaying foreign spies page {}.".format(page) )
        print( tmpl.format('Name', 'Level', 'Task', 'Next Mission') )
        for p in pris:
            task = self.summarize( p.task, 10 )
            name = self.summarize( p.name, 20 )
            print( tmpl.format(name, p.level, task, p.next_mission))
        print( '' )
        return len(pris)

    def _view_prisoners_page( self, page ):
        self.client.user_logger.info( "Viewing prisoners.".format(self.args.page) )
        self.client.cache_on('prisoners')
        pris = self.prison.view_prisoners( page )
        self.client.cache_off();
        tmpl = "{:<20}    {:0>2}    {:<10}    {}"
        print( "Displaying prisoners page {}.".format(page) )
        print( tmpl.format('Name', 'Level', 'Task', 'Sentence Expires') )
        for p in pris:
            task = self.summarize( p.task, 10 )
            name = self.summarize( p.name, 20 )
            print( tmpl.format(name, p.level, task, p.sentence_expires))
        print( '' )
        return len(pris)

