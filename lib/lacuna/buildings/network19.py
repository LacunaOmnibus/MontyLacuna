
from lacuna.bc import LacunaObject
from lacuna.building import MyBuilding

"""
    The view() retval includes 'restrict_coverage'.  This is a boolean 
    indicating whether or not coverage is currently restricted.
        '0' == coverage is flowing freely
        '1' == coverage is restricted
"""

class network19(MyBuilding):
    path = 'network19'

    def __init__( self, client, body_id:int = 0, building_id:int = 0 ):
        super().__init__( client, body_id, building_id )


    @LacunaObject.set_empire_status
    @MyBuilding.call_building_meth
    def restrict_coverage( self, toggle:int, *args, **kwargs ):
        """ Toggles news coverage restriction on and off.

        Requires 'toggle', an int set to 0 to allow news to flow, or 1 to restrict 
        coverage.

        NOTE that the value for 'toggle' is an int, not a boolean.  This will 
        blow up:
            net19.restrict_coverage( True )
        """
        pass

    @LacunaObject.set_empire_status
    @MyBuilding.call_building_meth
    def view_news( self, *args, **kwargs ):
        """ Shows the news stories and feeds available.

        Retval includes:
            news:   List of news story dicts:
                 {      'date': '27 10 2014 14:03:19 +0000',
                        'headline': 'Chapel demolished, wedding postponed.'     },
            feeds:  Dict, keyed off the zones whose feeds your Net19 can see:
                    {   '-1|-1': 'URL to feed for zone -1|-1',
                        '-1|0': 'URL to feed for zone -1|0',
                        ...         }

        The actual meanings of the news headlines are somewhat obscure, and may 
        require some study by the user.
        """
        pass



