

import lacuna.bc
import lacuna.building
import lacuna.glyph
import lacuna.resource
import lacuna.ship

import warnings

class archaeology(lacuna.building.MyBuilding):
    """ Archaeology Ministry

    The archaeology ministry will contain an attribute 'work' if and only if it 
    is currently searching ore for a glyph.  That attribute is a dict containing::

        - searching -- "anthracite",
        - start -- '31 10 2014 18:45:34 +0000',
        - end -- '01 11 2014 00:45:34 +0000',
        - seconds_remaining -- 21574,

    ...But that 'work' attribute will not exist at all if the arch min is not 
    searching right now, so you'll have to do a hasattr() check to see.
    """

    path = 'archaeology'

    def __init__( self, client, body_id:int = 0, building_id:int = 0 ):
        super().__init__( client, body_id, building_id )


    @lacuna.bc.LacunaObject.set_empire_status
    @lacuna.building.MyBuilding.call_building_meth
    def get_glyphs( self, **kwargs ):
        """get_glyphs() is deprecated.  Prefer get_glyph_summary() instead."""
        warnings.warn("get_glyphs() is deprecated - please use get_glyph_summary instead.")

    @lacuna.building.MyBuilding.call_returning_meth
    def get_glyph_summary( self, **kwargs ):
        """ Returns summary of glyphs that may be assembled in this arch min.

        Returns a list of lacuna.glyph.OwnedGlyph objects.
        """
        mylist = []
        for i in kwargs['rslt']['glyphs']:
            mylist.append( lacuna.glyph.OwnedGlyph(self.client, i) )
        return mylist

    @lacuna.building.MyBuilding.call_returning_meth
    def assemble_glyphs( self, glyphs:list, quantity:int = 1, **kwargs ):
        """ Attempts to assemble the listed glyphs into something useful.  

        Arguments:
            - glyphs -- a list of glyphs to assemble.  Order, spelling, and 
              capitalization matter; "goethite" is valid, "Goethite" is not!
            - quantity -- Integer number of this recipe you want to assemble.

        Returns a glyph.AssembledArtifact object.

        Raises ServerError 1002 if the listed glyphs do not form a valid 
        artifact recipe.
        """
        return lacuna.glyph.AssembledArtifact(self.client, kwargs['rslt']['item_name'], kwargs['rslt']['quantity'] )

    @lacuna.building.MyBuilding.call_returning_meth
    def get_ores_available_for_processing( self, **kwargs ):
        """ Get ores of sufficient quantity to perform glyph searches on.

        Returns a lacuna.resource.AvailableOre object.
        """
        return lacuna.resource.AvailableOre(self.client, kwargs['rslt']['ore'])

    @lacuna.building.MyBuilding.call_returning_meth
    def view_excavators( self, **kwargs ):
        """ Gets info on working excavators.

        Returns a tuple:
            - excavators -- List of lacuna.ship.Excavator objects
            - max -- Integer max excavators this arch min can support
            - travelling -- Integer number of excavators currently in the air on the way to a body to begin work.
        """
        mylist = []
        for i in kwargs['rslt']['excavators']:
            mylist.append( lacuna.ship.Excavator(self.client, i) )
        return(
            mylist,
            self.get_type(kwargs['rslt']['max_excavators']),
            self.get_type(kwargs['rslt']['travelling']),
        )

    @lacuna.bc.LacunaObject.set_empire_status
    @lacuna.building.MyBuilding.call_building_meth
    def abandon_excavator( self, site_id:int, **kwargs ):
        """ Abandons the excavator located at site_id.

        Arguments:
            - site_id -- Integer ID of the excavation site to abandon, taken from an Excavator object returned by view_excavators().
        """
        pass

