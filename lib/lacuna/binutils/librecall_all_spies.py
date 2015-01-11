
import lacuna, lacuna.binutils.libbin
import argparse, os, sys

class RecallAllSpies(lacuna.binutils.libbin.Script):

    def __init__(self):
        self.version = '0.1'
        parser = argparse.ArgumentParser(
            description = "Fetch home all spies based on a given planet, regardless of where they're currently located.  Spies will be fetched using the fastest ship you have available that can carry occupants.",
            epilog      = "EXAMPLE: python3 bin/recall_all_spies Earth",
        )
        parser.add_argument( 'name', 
            metavar     = '<planet>',
            action      = 'store',
            help        = 'All spies from this planet will be recalled.'
        )
        super().__init__(parser, 'real')

    
    def find_nothome_spies( self, home_id:int, intmin ):
        """ Finds all of the bodies where you've got spies assigned, 
        not including your current planet.

        Arguments:
            - home_id -- Integer ID of the planet to consider 'home'
            - intmin -- ``lacuna.buildings.intelligence.intelligence`` object; 
              the Int Min located on ``home_id``.

        Returns a dict of planets hosting spies whose home is ``home_id``::

            {   planet_id_1: planet_name_1,
                planet_id_2: planet_name_2,
                etc     }
        """
        bodies = {}
        spies = intmin.view_all_spies()
        for s in spies:
            if s.assigned_to.body_id == home_id:
                continue
            else:
                bodies[ s.assigned_to.body_id ] = s.assigned_to.name
        return bodies


