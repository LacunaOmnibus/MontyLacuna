
import lacuna.bc
import lacuna.building

class Spy(lacuna.bc.SubClass):
    """
    Attributes::

        id                     "id-goes-here",
        name                   "Jason Bourne",
        assignment             "Idle",
        possible_assignments   List of lacuna.spy.Assignment objects
        level                  9,
        politics               0,
        mayhem                 20,
        theft                  40,
        intel                  33,
        offense_rating         570,
        defense_rating         150,
        is_available           1,
        available_on           "01 31 2010 13:09:05 +0600", # if can't be reassigned, this 
                                                            # is when will be available
        started_assignment     "01 31 2010 13:09:05 +0600",
        seconds_remaining      45,
        assigned_to            SpyBody object
        based_from             SpyBody object

    - :class:`lacuna.spy.Assignment`
    - :class:`lacuna.spy.SpyBody`
    """

    def __init__( self, client, mydict:dict, *args, **kwargs ):
        if 'possible_assignments' in mydict:
            assignment_list = []
            for i in mydict['possible_assignments']:
                assignment_list.append( Assignment(client, i) )
            mydict['possible_assignments'] = assignment_list

        if 'assigned_to' in mydict:
            mydict['assigned_to'] = SpyBody(client, mydict['assigned_to'])

        if 'based_from' in mydict:
            mydict['based_from'] = SpyBody(client, mydict['based_from'])

        if 'mission_count' in mydict:
            mydict['mission_count'] = MissionCount(client, mydict['mission_count'])

        super().__init__(client, mydict)

class Assignment(lacuna.bc.SubClass):
    """ A task that a spy can be assigned to.

    Attributes::

            task        "Idle",
            recovery    0,          # in seconds
            skill       "none"

    ==============================  ===========================================
    Tasks
    ---------------------------------------------------------------------------
    Name                            Description
    ==============================  ===========================================
    Abduct Operatives               Kidnap a spy and bring him back home.
    Assassinate Operatives          Kill spies.
    Appropriate Resources           Steal empty ships, ships full of resources, ships full of trade goods, etc.
    Appropriate Technology          Steal plans for buildings that this empire has built, or has in inventory.
    Counter Espionage               Passively defend against all attackers.
    Gather Resource Intelligence    Find out what's up for trade, what ships are available, what ships are being built, where ships are travelling to, etc.
    Gather Empire Intelligence      Find out what is built on this planet, the resources of the planet, what other colonies this Empire has, etc.
    Gather Operative Intelligence   Find out what spies are on this planet, where they are from, what they are doing, etc.
    Hack Network 19                 Attempts to besmirch the good name of the empire controlling this planet, and deprive them of a small amount of happiness.
    Idle                            Don't do anything.
    Incite Insurrection             Steal a planet.
    Incite Mutiny                   Turn spies. If successful they come work for you.
    Incite Rebellion                Obliterate the happiness of a planet. If done long enough, it can shut down a planet.
    Intel Training                  Train in Intelligence skill
    Mayhem Training                 Train in Mayhem skill
    Political Propaganda            Give happiness generation a boost.  Especially effective on unhappy colonies, but hastens an agent toward retirement.
    Politics Training               Train in Politics skill
    Rescue Comrades                 Break spies out of prison.
    Sabotage BHG                    Prevent enemy planet from using Black Hole Generator.
    Sabotage Infrastructure         Destroy buildings.
    Sabotage Probes                 Destroy probes controlled by this empire.
    Sabotage Resources              Destroy ships being built, docked, en route to mining platforms, etc.
    Security Sweep                  Round up attackers.
    Theft Training                  Train in Theft skill
    ==============================  ===========================================

    Recovery:
        The spy is currently recovering from running his previous task.  This 
        is the time remaining, in seconds, of that recovery period.  After 
        that time expires, the spy will be available for another task.

    Skill:
        Which of the spy's skills will be used to calculate success.
    """


class ForeignAgent(Spy):
    """
    Attributes::

        name                "James Bond",
        level               "20",
        task                "Appropriate Technology"
        next_mission        "01 31 2010 13:09:05 +0600"   

    You have to capture a ForeignSpy to turn him into a Prisoner to be able to 
    see his ID.
    """


class Merc(Spy):
    """ A spy who's ready to be added as a trade on the Merc's Guild.

    Attributes::

        id      12345
        name    "James Bond",
        level   "20",
    """


class IntelView(lacuna.bc.SubClass):
    """
    Attributes::

        maximum             5,
        current             1,
        in_training         1,
        training_costs      lacuna.spy.TrainingCosts object

    - :class:`lacuna.spy.TrainingCosts`
    """
    def __init__(self, client, mydict:dict):
        if ['training_costs'] in mydict:
            mydict['training_costs'] = TrainingCosts(client, mydict['training_costs'])
        super().__init__(client, mydict)

class TrainingCosts(lacuna.bc.SubClass):
    """
    Attributes::

        food    100,
        water   120,
        energy  20,
        ore     5,
        waste   10,
        time    60,
    """

class MissionCount(lacuna.bc.SubClass):
    """ The count of missions performed by the spy.

    A spy is forcefully retired after performing 150 of either type of mission 
    (offensive or defensive).  So to get the most life out of a spy, once he 
    gets to 149 of one type of mission, you should only use him for the other 
    type from then on.

    Attributes::

        offensive   149
        defensive   149
    """


class MissionResult(lacuna.bc.SubClass):
    """
    Attributes::

        result          "Failure",
        message_id      "id-goes-here",
        reason          "I'm under heavy fire over here!"

    Possible values for 'result' are::

        Accepted    Nothing happened as a result of the assignment, as to 
                    Counter Espionage or Idle.
        Success     The mission succeeded and your spy won.
        Bounce      The mission began, but was foiled.  Essentially a draw.  
        Failure     The mission failed miserably.  Your spy is probably 
                    knocked out, in jail, or dead.

    The message_id listed is the ID of a message in your inbox 
    containing details of the result of the mission.  Not all 
    missions will include a message_id (eg 'Idle').
    """


class Prisoner(Spy):
    """
    Attributes::

        id                  "id-goes-here",
        name                "James Bond",
        level               "20",
        task                "Captured" or "Prisoner Transport",
        sentence_expires    "01 31 2010 13:09:05 +0600"   
    """


class SpyBody(lacuna.bc.SubClass):
    """ A body (planet, space station, etc).  This can be where the spy is 
    currently located or his home base (from which he is controlled).

    Attributes::

        id          id-goes-here",
        body_id     id-goes-here",
        name        Earth",
        x           40,
        y           -71

    ``id`` and ``body_id`` both contain the same value.
    """
    def __init__( self, client, mydict:dict, *args, **kwargs ):
        if 'body_id' in mydict:
            mydict['id'] = mydict['body_id']
        super().__init__(client, mydict)

class Training(lacuna.building.MyBuilding):
    @lacuna.building.MyBuilding.call_returning_meth
    def view( self, *args, **kwargs ):
        """ Returns info on how many points this training building can confer, 
        and how many spies are currently training.

        Returns a single :class:`lacuna.spy.TrainingView` object.
        """
        lacuna.building.MyBuilding._write_building_status( self, kwargs['rslt'] )
        view = TrainingView( self.client, kwargs['rslt']['spies'] )
        return view

class TrainingView(lacuna.bc.SubClass):
    """
    Attributes::

        max_points      2600
        points_per      45
        in_training     4
    """

