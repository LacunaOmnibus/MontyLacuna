
import lacuna.bc
from lacuna.building import MyBuilding

class entertainment(lacuna.building.MyBuilding):
    path = 'entertainment'

    def __init__( self, client, body_id:int = 0, building_id:int = 0 ):
        super().__init__( client, body_id, building_id )

    @lacuna.building.MyBuilding.call_returning_meth
    def get_lottery_voting_options( self, *args, **kwargs ):
        """ Returns a list of external sites that the user can visit.  Each
        visit affords the user a single lottery ticket.

        Requires a captcha.  If you have not solved one yet with the current 
        session_id, one will be displayed for you.

        Returns a dict including key ``options``, which is a list of dicts, each 
        dict containing:
            - name -- "Some Site",
            - url -- "http://www.somesite.com/vote?id=44",
        """
        mylist = []
        for i in kwargs['rslt']['options']:
            mylist.append( LotteryOptions(self.client, i) )
        return mylist

    @lacuna.building.MyBuilding.call_building_meth
    def duck_quack( self, **kwargs ):
        """ Quacks the duck.
        The reasons for wanting to do this are shrouded in the mysteries of 
        the ages.  But it's kind of fun.
        """
        pass

class LotteryOptions(lacuna.bc.SubClass):
    """
    Attributes::

        name    Name of the gaming/voting website
        url     URL to vote on TLE at the website
    """

