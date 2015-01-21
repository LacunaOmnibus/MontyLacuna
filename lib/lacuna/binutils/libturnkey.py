
### Search on CHECK

import lacuna, lacuna.binutils.libbin, lacuna.types
import lacuna.exceptions as err
import argparse, operator, os, sys

class Turnkey(lacuna.binutils.libbin.Script):
    """ CHECK Assigns spies to a task, in bulk.
    """

    def __init__(self):
        self.version = '0.1'

        parser = argparse.ArgumentParser(
            description = 'CHECK.',
            epilog      = "CHECK Full docs can be found at http://tmtowtdi.github.io/MontyLacuna/scripts/assign_spies.html",
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
            help        = "CHECK"
        )
        super().__init__(parser)

        self.body   = ''      # Either a colony or a space station.
        self.prison = ''      # Either a Sec Min or a Police Station.

        if self.args.fresh:
            self.client.cache_clear( 'my_colonies' )
            self.client.cache_clear( 'prisoners' )

        self._set_body( self.args.name )
        self._set_prison()

    def _set_body( self, pname:str ):
        """ Sets the current working planet by name.

        Arguments:
            - pname -- String name of the planet to set.
        """
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

        ### No need for a try block.  If the user hasn't got a bldg building, 
        ### this will blow up properly.
        self.client.cache_on( 'my_colonies', 3600 )
        self.prison = self.body.get_buildings_bytype( bldg, 1, 1, 100 )[0]
        self.client.cache_off

    def perform_chosen_task( self ):
        ### CHECK this is dumb - make a dispatch table.
        if self.args.task == 'view_prisoners':
            self.view_prisoners()
        elif self.args.task == 'view_spies':
            self.view_foreign_spies()
        elif self.args.task == 'execute':
            self.execute_prisoners()
        elif self.args.task == 'release':
            self.release_prisoners()
        else:
            raise KeyError( "What are you doing, Dave?" )

    def execute_prisoners( self ):
        if self.args.page == 0:
            ### CHECK sigh pagination.
            pass
        else:
            self.execute_prisoners_page( self.args.page )

    def execute_prisoners_page( self, page ):
        self.client.cache_on('prisoners')
        pris = self.prison.view_prisoners( page )
        for p in pris:
            ### CHECK this is untested
            #self.prison.execute_prisoner( p.id )
            print( "This is where I would execute prisoner ID {}".format(p.id) )

    def release_prisoners( self ):
        if self.args.page == 0:
            ### CHECK sigh pagination.
            pass
        else:
            self.release_prisoners_page( self.args.page )

    def release_prisoners_page( self, page ):
        self.client.cache_on('prisoners')
        pris = self.prison.view_prisoners( page )
        for p in pris:
            ### CHECK this is untested
            #self.prison.release_prisoner( p.id )
            print( "This is where I would release prisoner ID {}".format(p.id) )

    def view_foreign_spies( self ):
        if self.args.page == 0:
            cnt = 0
            while(True):
                cnt += 1
                num = self.view_foreign_spies_page( cnt )
                if num < 25:
                    break
        else:
            self.view_foreign_spies_page( self.args.page )

    def view_foreign_spies_page( self, page ):
        self.client.cache_on('prisoners')   # don't change this
        pris = self.prison.view_foreign_spies( page )
        tmpl = "{:<20}    {:0>2}    {:<10}    {}"
        print( "Displaying foreign spies page {}.".format(page) )
        print( tmpl.format('Name', 'Level', 'Task', 'Next Mission') )
        for p in pris:
            task = self.summarize( p.task, 10 )
            name = self.summarize( p.name, 20 )
            print( tmpl.format(name, p.level, task, p.next_mission))
        print( '' )
        return len(pris)

    def view_prisoners( self ):
        if self.args.page == 0:
            cnt = 0
            while(True):
                cnt += 1
                num = self.view_prisoners_page( cnt )
                if num < 25:
                    break
        else:
            self.view_prisoners_page( self.args.page )

    def view_prisoners_page( self, page ):
        self.client.cache_on('prisoners')
        pris = self.prison.view_prisoners( page )
        tmpl = "{:<20}    {:0>2}    {:<10}    {}"
        print( "Displaying prisoners page {}.".format(page) )
        print( tmpl.format('Name', 'Level', 'Task', 'Sentence Expires') )
        for p in pris:
            task = self.summarize( p.task, 10 )
            name = self.summarize( p.name, 20 )
            print( tmpl.format(name, p.level, task, p.sentence_expires))
        print( '' )
        return len(pris)




