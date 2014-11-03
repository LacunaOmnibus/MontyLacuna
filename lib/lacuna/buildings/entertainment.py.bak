
from lacuna.bc import LacunaObject
from lacuna.building import Building

class entertainment(Building):
    path = 'entertainment'

    def __init__( self, client, body_id:int = 0, building_id:int = 0 ):
        super().__init__( client, body_id, building_id )

    @LacunaObject.set_empire_status
    @Building.call_building_meth
    def get_lottery_voting_options( self, *args, **kwargs ):
        """ Returns a list of external sites that the user can visit.  Each
        visit affords the user a single lottery ticket.

        Requires a captcha.  If you have not solved one yet with the current 
        session_id, one will be displayed for you.

        Retval includes 'options', a list of dicts:
                    [
                        { "name" : "Some Site",
                          "url" : "http://www.somesite.com/vote?id=44"   },
                        ...
                    ],
        """
        pass

    @Building.call_building_meth
    def duck_quack( self, **kwargs ):
        """ Quacks the duck.
        The reasons for wanting to do this are shrouded in the mysteries of 
        the ages.  But it's kind of fun.
        """
        pass
