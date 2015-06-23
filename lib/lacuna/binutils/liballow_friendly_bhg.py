
import lacuna, lacuna.binutils.libbin
import lacuna.exceptions as err
import argparse, csv, operator, os, sys


class AllowFriendlyBHG(lacuna.binutils.libbin.Script):
    """ Gather and report on stations.
    """

    def __init__(self):
        self.version = '0.1'
        parser = argparse.ArgumentParser(
            description = 'Allow a friendly alliance to use their BHGs in the jurisdiction of one of your stations.',
            epilog      = "REMEMBER TO USE YOUR FULL, NOT SITTER, PASSWORD!  Full docs can be found at http://tmtowtdi.github.io/MontyLacuna/scripts/allow_friendly_bhg.html",
        )
        parser.add_argument( 'station', 
            metavar     = '<station name>',
            action      = 'store',
            help        = "The station that wants to grant passage."
        )
        parser.add_argument( 'ally', 
            metavar     = '<ally name>',
            help        = "Members of the alliance to be granted passage."
        )
        parser.add_argument( '--fresh', 
            action      = 'store_true',
            help        = "Clears the cache to ensure fresh data."
        )
        super().__init__(parser)
        self.alliance       = ''
        self.parliament     = ''
        self.station        = ''
        if self.args.fresh:
            self.client.cache_clear( 'my_stations' )
            self.client.cache_clear( 'alliances' )


    def allow_bhg_usage( self, ally_id:int ):
        """ Allows the requested alliance to use their BHG.

        Arguments:
            ally_id (int): The ID of the friendly alliance.
        """
        self.parliament.allow_bhg_by_alliance( ally_id )

    def get_ally_id( self ):
        """ Returns the alliance ID for the alliance specified at the command line.

        Returns:
            id (int): The ID of the alliance requested if it could be found.  If we find either zero or more than one alliances matching the requested name, returns None.

        """
        generic_ally    = self.client.get_alliance()            # generic alliance object
        found_allies    = generic_ally.find( self.args.ally )   # list of FoundAlliance objects

        if len(found_allies) == 0:
            self.client.user_logger.debug( "Found no alliances matching {}.".format(self.args.ally) )
            return None
        elif len(found_allies) > 1:
            return self.choose_ally_from_list( found_allies )
        else:
            return found_allies[0].id;

    def choose_ally_from_list( self, ally_list:list ):
        print( "Multiple alliances were found that match '{}':".format(self.args.ally) )
        for i in range( 0, len(ally_list) ):
            num = i + 1
            print( "\t{:02d}: {}".format(num, ally_list[i].name) )
        print( '' )
        choice = int( input('Which one did you mean? ') )
        if choice > len(ally_list):
            print( "{} is not one of the listed choices, bonehead.".format(choice) )
            quit()
        print( "You chose '{}'." .format(ally_list[ choice - 1 ].name) );
        return ally_list[ choice - 1 ].id;

    def set_station( self ):
        """ Sets the active station object based on the station name argument passed
        by the user.

        Also sets the active Parliament object, provided the Parl on the requested station
        is level 28 or higher and undamage.

        Raises:
            (lacuna.exceptions.NoSuchBuildingError) if the Parl building is damaged or 
            under level 28.
        """
        sname = self.abbrv.get_name(self.args.station)
        self.client.user_logger.debug( "Checking station {}.".format(sname) )
        self.client.cache_on( 'my_stations', 3600 )
        self.station    = self.client.get_body_byname( sname )
        self.parliament = self.station.get_buildings_bytype( 'parliament', 28, 1, 100 )[0];
        self.client.cache_off()

