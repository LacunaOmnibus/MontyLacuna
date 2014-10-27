
import lacuna
from lacuna.bc import LacunaObject
from lacuna.building import Building

class oracleofanid(Building):
    path = 'oracleofanid'

    def __init__( self, client, body_id:int = 0, building_id:int = 0 ):
        super().__init__( client, body_id, building_id )

    @Building.call_named_returning_meth
    def get_probed_stars( self, named_args:dict = {'page_number': 1}, *args, **kwargs ):
        """ Returns a list of stars viewable by the Oracle.

        Accepts a single optional dict:
            { 'page_number': 3 }
        If that dict is omitted, the returned page defaults to 1.

        Retval is just a list of lacuna.map.Star objects.
        """
        star_list = []
        for s in kwargs['rslt']['stars']:
            star_list.append( lacuna.map.Star(self.client, s) )
        return star_list

    @Building.call_returning_meth
    def get_star( self, star_id:int, *args, **kwargs ):
        """
        """
        star = lacuna.map.Star( self.client, kwargs['rslt']['star'] )
        return star
