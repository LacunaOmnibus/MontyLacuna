
import lacuna.bc
import lacuna.building

class network19(lacuna.building.MyBuilding):
    path = 'network19'

    def __init__( self, client, body_id:int = 0, building_id:int = 0 ):
        super().__init__( client, body_id, building_id )

    @lacuna.building.MyBuilding.call_returning_meth
    def view( self, *args, **kwargs ):
        """ Indicates whether news coverage is restricted or flowing freely.

        Returns 'restrict_coverage'.  This is a boolean integer indicating 
        whether or not coverage is currently restricted.
            '0' == coverage is flowing freely
            '1' == coverage is restricted
        """
        return kwargs['rslt']['restrict_coverage']

    @lacuna.bc.LacunaObject.set_empire_status
    @lacuna.building.MyBuilding.call_building_meth
    def restrict_coverage( self, toggle:int = 0, *args, **kwargs ):
        """ Toggles news coverage restriction on and off.

        Arguments:
            toggle  Integer 0 or 1.  0 to allow news to flow, or 1 to restrict 
                    coverage.  Defaults to 0.

                    NOTE that value _is_ an int, not a boolean.  This will blow 
                    up:
                        net19.restrict_coverage( True )
        """
        pass


    @lacuna.building.MyBuilding.call_returning_meth
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
        story_list = []
        for i in kwargs['rslt']['news']:
            story_list.append( Story(i) )

        feed_list = []
        for zone, url in kwargs['rslt']['feeds'].items():
            feed_list.append( Feed(zone, url) )

        return (
            story_list,
            feed_list
        )


class NewsItem():
    def __init__(self, mydict):
        for k, v in mydict.items():
            setattr(self, k, v)

class Story(NewsItem):
    """
    Attributes:
        headline    "HCorp founded a new colony on Rigel 4.", 
        date        "01 31 2010 13:09:05 +0600" 
    """

class Feed():
    """
    Attributes:
           zone     0|0
           url      'http://feeds.game.lacunaexpanse.com/78d5e7b2-b8d7-317c-b244-3f774264be57.rss'
    """
    def __init__(self, zone, url):
        self.zone = zone
        self.url = url


