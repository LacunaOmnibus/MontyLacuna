
### CHECK
### Pick back up at propose_seize_star, which has not been started yet  
### (working through the API docs top to bottom).

import lacuna.bc
import lacuna.body
import lacuna.empire

class parliament(lacuna.building.MyBuilding):
    path = 'parliament'

    def __init__( self, client, body_id:int = 0, building_id:int = 0 ):
        super().__init__( client, body_id, building_id )

    @lacuna.bc.LacunaObject.call_returning_body_meth
    def view_laws( self, body_id:int, *args, **kwargs ):
        """ Show laws passed by this parliament building

        Arguments:
            - body_id -- Integer ID of the Space Station (not of the parliament 
              building.)

        This method is really being called against the station itself rather 
        than against the parliament building in particular.

        This means that anybody can call this method on any space station to 
        see what laws have been enacted on that station; these laws are public 
        information.

        Returns a list of lacuna.parliament.Law objects.
        """
        mylist = []
        for i in kwargs['rslt']['laws']:
            mylist.append( Law(self.client, i) )
        return mylist

    @lacuna.building.MyBuilding.call_returning_meth
    def view_propositions( self, *args, **kwargs ):
        """ Show propositions pending approval or rejection by vote.

        Returns a list of lacuna.parliament.Proposition objects.
        """
        mylist = []
        for i in kwargs['rslt']['propositions']:
            mylist.append( Proposition(self.client, i) )
        return mylist

    @lacuna.building.MyBuilding.call_returning_meth
    def view_taxes_collected( self, *args, **kwargs ):
        """ Show taxes collected.

        Taxes haven't really been implemented in the game.
        This is included for API completeness.

        For one station, owned by me, I'm getting back a Tax object that claims 
        that I have paid 0 taxes total.

        For another station, owned by Infinate Ones, I'm getting back no Tax 
        objects at all.

        My guess is that you'll get back a Tax object if the empire you're using 
        to connect actually owns the station you're querying.  But even if you 
        do get a Tax object back, it'll always list 0 in payments, since Taxes 
        are un-implemented.

        Returns a list of lacuna.parliament.Tax objects.
        """
        mylist = []
        for i in kwargs['rslt']['taxes_collected']:
            mylist.append( Tax(self.client, i) )
        return mylist


    @lacuna.building.MyBuilding.call_returning_meth
    def get_stars_in_jurisdiction( self, *args, **kwargs ):
        """ Get all stars in the jurisdiction of this station.

        The TLE API documentation says that seized stars will include a key 
        named 'station', pointing to a dict describing the seizing station.
        That 'station' dict is never included.

        Also, it does not mention the 'zone' key, which is included, and is 
        an attribute of the StationStar objects returned.

        Returns a list of lacuna.map.StationStar objects.
        """
        mylist = []
        for i in kwargs['rslt']['stars']:
            mylist.append( lacuna.map.StationStar(self.client, i) )
        return mylist


    @lacuna.building.MyBuilding.call_returning_meth
    def get_bodies_for_star_in_jurisdiction( self, star_id:int, *args, **kwargs ):
        """ Get the bodies orbiting one of the stars in the station's 
        jurisdiction.

        Arguments:
            - star_id -- Integer ID of the star whose bodies we want listed.

        Returns a list of lacuna.body.JurisdictionPlanet objects.
        """
        mylist = []
        for i in kwargs['rslt']['bodies']:
            mylist.append( lacuna.body.JurisdictionPlanet(self.client, i) )
        return mylist


    @lacuna.building.MyBuilding.call_returning_meth
    def get_mining_platforms_for_asteroid_in_jurisdiction( self, roid_id:int, *args, **kwargs ):
        """ Get the bodies orbiting one of the stars in the station's 
        jurisdiction.

        Arguments:
            - roid_id -- Integer ID of the asteroid we want to check for platforms.

        Returns a list of lacuna.buildings.parliament.MiningPlatform objects.
        """
        mylist = []
        for i in kwargs['rslt']['platforms']:
            mylist.append( MiningPlatform(self.client, i) )
        return mylist

    @lacuna.building.MyBuilding.call_returning_meth
    def cast_vote( self, prop_id:int, vote_id:int = 1, *args, **kwargs ):
        """ Votes on a proposition.

        Arguments:
            - prop_id -- Integer ID of the proposition to vote for.
            - vote -- Optional integer.  1 to vote yes, 0 to vote no.  Defaults 
              to 1 ('yes').

        Returns a single lacuna.buildings.parliament.Proposition object.
        """
        return Proposition(self.client, kwargs['rslt']['proposition'])


    @lacuna.building.MyBuilding.call_returning_meth
    def propose_writ( self, title:str, description:str, *args, **kwargs ):
        """ Create a Writ proposal

        Arguments:
            - title -- String.  The title of the proposition.
            - description -- String.  The description of the proposition.

        Returns a single lacuna.buildings.parliament.Proposition object.
        """
        return Proposition(self.client, kwargs['rslt']['proposition'])


    @lacuna.building.MyBuilding.call_returning_meth
    def propose_repeal_law( self, law_id:int, *args, **kwargs ):
        """ Create a proposal to repeal an existing law

        Arguments:
            - law_id -- Integer ID of the law to repeal.

        Returns a single lacuna.buildings.parliament.Proposition object.
        """ 
        return Proposition(self.client, kwargs['rslt']['proposition'])


    @lacuna.building.MyBuilding.call_returning_meth
    def propose_transfer_station_ownership( self, to_empire_id:int, *args, **kwargs ):
        """ Create a proposal to transfer station ownership to another empire.

        Arguments:
            - to_empire_id -- Integer ID of the empire who should end up owning the station.

        Returns a single lacuna.buildings.parliament.Proposition object.
        """ 
        return Proposition(self.client, kwargs['rslt']['proposition'])


class Law(lacuna.bc.SubClass):
    """
    Attributes::
        
        id              "id-goes-here",
        name            "Censure of Jamie Vrbsky",
        description     "Jamie Vrbsky is bad at playing Lacuna!",
        date_enacted    "01 31 2010 13:09:05 +0600"
    """

class MiningPlatform(lacuna.bc.SubClass):
    """ This appears in this module because it's the only place this format 
    appears.

    Attributes::
        
        id          "id-goes-here",
        empire      lacuna.empire.FoundEmpire object
    """
    def __init__(self, client, mydict:dict):
        mydict['empire'] = lacuna.empire.FoundEmpire(client, mydict['empire'])
        super().__init__(client, mydict)

class Proposition(lacuna.bc.SubClass):
    """
    Attributes::
        
        id              "id-goes-here",
        name            "Rename Station",
        description     "Rename the station from 'Bri Prui 7' to 'Deep Space 1'.",
        votes_needed    7,
        votes_yes       1,
        votes_no        0,
        status          "Pending",
        date_ends       "01 31 2010 13:09:05 +0600",
        proposed_by     lacuna.empire.FoundEmpire object
        ###
        ### Will only be present if the current empire has already voted
        my_vote         0   # 1 for yes, 0 for no.
    """
    def __init__(self, client, mydict:dict):
        mydict['proposed_by'] = lacuna.empire.FoundEmpire( client, mydict['proposed_by'] )
        super().__init__(client, mydict)

class Proposition(lacuna.bc.SubClass):
    """
    Attributes::
        
        id              "id-goes-here",
        name            "Rename Station",
        description     "Rename the station from 'Bri Prui 7' to 'Deep Space 1'.",
        votes_needed    7,
        votes_yes       1,
        votes_no        0,
        status          "Pending",
        date_ends       "01 31 2010 13:09:05 +0600",
        proposed_by     lacuna.empire.FoundEmpire object
        my_vote         0 # not present if they haven't voted
    """
    def __init__(self, client, mydict:dict):
        mydict['proposed_by'] = lacuna.empire.FoundEmpire( client, mydict['proposed_by'] )
        super().__init__(client, mydict)

class Tax(lacuna.bc.SubClass):
    """
    Attributes::
        
        id      "id-goes-here",
        name    "Klingons",
        paid    [ 0, 1000, 0, 0, 1500, 500, 500 ],
        total   3500,

    The ``paid`` attribute is a list of payments over the past seven days, 
    element 0 being "today".
    """


