
from lacuna.bc import LacunaObject
from lacuna.building import MyBuilding
import lacuna.glyph
import lacuna.ship

import warnings

"""
    The archaeology building will contain an attribute 'work' if and only if it 
    is currently searching for an ore.  That attribute is a dict containing:
            "searching":            "anthracite",
            "start":                '31 10 2014 18:45:34 +0000',
            "end":                  '01 11 2014 00:45:34 +0000',
            "seconds_remaining":    21574,

    ...But that 'work' attribute will not exist at all if the arch min is not 
    searching right now, so you'll have to do a hasattr() check to see:
            if hasattr( arch, 'work' ):
                # searching now
            else:
                # NOT searching now
"""

class archaeology(MyBuilding):
    path = 'archaeology'

    def __init__( self, client, body_id:int = 0, building_id:int = 0 ):
        super().__init__( client, body_id, building_id )


    @LacunaObject.set_empire_status
    @MyBuilding.call_building_meth
    def get_glyphs( self, **kwargs ):
        """get_glyphs() is deprecated.  Prefer get_glyph_summary() instead."""
        warnings.warn("get_glyphs() is deprecated - please use get_glyph_summary instead.")

    @MyBuilding.call_returning_meth
    def get_glyph_summary( self, **kwargs ):
        """ Returns summary of glyphs that may be assembled in this arch min.

        Returns a list of OwnedGlyph objects.
        """
        mylist = []
        for i in kwargs['rslt']['glyphs']:
            mylist.append( lacuna.glyph.OwnedGlyph(self.client, i) )
        return mylist

    @LacunaObject.set_empire_status
    @MyBuilding.call_building_meth
    def assemble_glyphs( self, glyphs:list, quantity:int = 1, **kwargs ):
        """ Attempts to assemble the listed glyphs into something useful.  
        Quantity defaults to 1.

        On success, retval includes the keys 'item_name' and 'quantity'.
        'item_name' is the name of the artifact created.
        'quantity' is the integer number created.

        Raises ServerError 1002 if the listed glyphs do not form a valid 
        artifact recipe.
        """
        pass

    @LacunaObject.set_empire_status
    @MyBuilding.call_building_meth
    def get_ores_available_for_processing( self, **kwargs ):
        """ Returns list of all ores that are of sufficient quantity onsite to 
        perform glyph searches on.

        Retval contains key 'ore', a dict keyed off ore names, with the ore 
        quantities as values:
            'ore': {   'anthracite': 99294156,
                        'bauxite': 210171773,
                        ...
            }
        """
        pass

    @MyBuilding.call_returning_meth
    def view_excavators( self, **kwargs ):
        """ Gets info on working excavators.

        Returns a tuple:
            excavators      List of Excavator objects
            max             Integer max excavators this arch min can support
            travelling      Integer number of excavators currently in the air 
                            on the way to a body to begin work.
        """
        mylist = []
        for i in kwargs['rslt']['excavators']:
            mylist.append( lacuna.ship.Excavator(self.client, i) )
        return(
            mylist,
            kwargs['rslt']['max_excavators'],
            kwargs['rslt']['travelling'],
        )

    @LacunaObject.set_empire_status
    @MyBuilding.call_building_meth
    def abandon_excavator( self, site_id:int, **kwargs ):
        """ Abandons the excavator located at site_id.
        Be sure you understand the difference between an excavator site ID and 
        a body ID, documented in view_excavators(), before using this.
        """
        pass

