
import lacuna.bc
import lacuna.building

class network19(lacuna.building.MyBuilding):
    path = 'network19'

    def __init__( self, client, body_id:int = 0, building_id:int = 0 ):
        super().__init__( client, body_id, building_id )

    @lacuna.building.MyBuilding.call_returning_meth
    def view( self, *args, **kwargs ):
        """ Indicates whether news coverage is restricted or flowing freely.

        Returns an integer indicating whether or not coverage is currently 
        restricted:
            - ``0`` -- coverage is flowing freely
            - ``1`` -- coverage is restricted
        """
        ### restrict_coverage() wants '1' or '0'.  For consistency, leave this 
        ### return as-is (meaning, 'also 1 or 0') rather than converting it to 
        ### a boolean.
        return self.get_type(kwargs['rslt']['restrict_coverage'])

    @lacuna.bc.LacunaObject.set_empire_status
    @lacuna.building.MyBuilding.call_building_meth
    def restrict_coverage( self, toggle:int = 0, *args, **kwargs ):
        """ Toggles news coverage restriction on and off.

        Arguments:
            - toggle -- Pseudo-boolean integer.  ``0`` to turn restrictions off
              (allow news to flow normally), ``1`` to turn restrictions on.
        """
        pass


    @lacuna.building.MyBuilding.call_returning_meth
    def view_news( self, *args, **kwargs ):
        """ Shows the news stories and feeds available.

        Returns:
            - news:   List of Story objects
            - feeds:  List of Feed objects

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

class Story(lacuna.bc.SubClass):
    """
    Attributes::

        headline    "HCorp founded a new colony on Rigel 4.", 
        date        "01 31 2010 13:09:05 +0600" 
    """

class Feed( lacuna.bc.SubClass ):
    """
    Attributes::

        zone     0|0
        url      'http://feeds.game.lacunaexpanse.com/78d5e7b2-b8d7-317c-b244-3f774264be57.rss'
    """
    def __init__(self, zone, url):
        self.zone = zone
        self.url = url


