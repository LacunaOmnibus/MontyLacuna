
from lacuna.bc import LacunaObject
from lacuna.building import Building

import warnings

class archaeology(Building):
    path = 'archaeology'

    def __init__( self, client, body_id:int = 0, building_id:int = 0 ):
        super().__init__( client, body_id, building_id )

    @LacunaObject.set_empire_status
    @Building.call_building_meth
    def get_glyphs( self, **kwargs ):
        """get_glyphs() is deprecated.  Prefer get_glyph_summary() instead."""
        warnings.warn("get_glyphs() is deprecated - please use get_glyph_summary instead.")

    @LacunaObject.set_empire_status
    @Building.call_building_meth
    def get_glyph_summary( self, **kwargs ):
        """ Returns summary of glyphs that may be assembled in this arch min.
        Retval includes key 'glyphs', a list of glyph dicts.
        Format of glyph dicts:
            {   'id': '12219153',
                'name': 'rutile',
                'quantity': '12000',
                'type': 'rutile'},
        """
        pass

    @LacunaObject.set_empire_status
    @Building.call_building_meth
    def assemble_glyphs( self, glyphs:list, quantity:int = 1, **kwargs ):
        """ Attempts to assemble the listed glyphs into something useful.  
        Quantity defaults to 1.

        On success, retval includes the keys 'item_name' and 'quantity'.
        'item_name' is the name of the artifact created.
        'quantity' is the integer number created.

        Raises 1002 if the listed glyphs do not form a valid artifact recipe.
        """
        pass

    @LacunaObject.set_empire_status
    @Building.call_building_meth
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

    @LacunaObject.set_empire_status
    @Building.call_building_meth
    def view_excavators( self, **kwargs ):
        """ Returns status of excavators currently controlled by this archmin.

        Retval contains the keys:
            'id' - Integer ID of the excavator site.  IMPORTANT - this is 
            neither the ID of the body the excavator is on nor the ID of the 
            ship itself.  It is an excavator site ID, and it's what you must 
            pass to abandon_excavator().
            'travelling' - Integer number of excavs currently on their way to 
            a target
            'max_excavators' - Integer max excavators this archmin can control
            'excavators' - List of excavator dicts, each in the form:
                {
                    "id" : "id-goes-here",
                    "body" : {
                        Body dict describing the body this excavator is on.  
                        See body.pm for docs on this.
                        Note that this contains an 'id' key - this is the ID 
                        of the body, NOT the ID of the excavator site.
                    },
                    "artifact" : 5,
                    "glyph" : 30,
                    "plan" : 7,
                    "resource" : 53
                    "date_landed" : Date excav started at location (eg '20 10 2014 13:28:20 +0000')
                },
        """
        pass

    @LacunaObject.set_empire_status
    @Building.call_building_meth
    def abandon_excavator( self, site_id:int, **kwargs ):
        """ Abandons the excavator located at site_id.
        Be sure you understand the difference between an excavator site ID and 
        a body ID, documented in view_excavators(), before using this.
        """
        pass

