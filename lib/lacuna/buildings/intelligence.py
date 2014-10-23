
from lacuna.bc import LacunaObject
from lacuna.building import Building

"""

    The retval from view() contains the key 'spies' pointing to a dict:
            {
                "maximum" : 5,
                "current" : 1,
                "in_training" : 1,
                "training_costs" : {
                    "food" : 100,
                    "water" : 120,
                    "energy" : 20,
                    "ore" : 5,
                    "waste" : 10,
                    "time" : 60,
                }
            }


"""

class intelligence(Building):
    path = 'intelligence'

    def __init__( self, client, body_id:int = 0, building_id:int = 0 ):
        super().__init__( client, body_id, building_id )

    @LacunaObject.set_empire_status
    @Building.call_building_meth
    def train_spy( self, *args, quantity:int = 1, **kwargs ):
        """ Trains one or more spies.  "Train", in this case, means "create".
        The "quantity" argument defaults to 1.

        Retval includes:
            "trained" - Integer number added to the training queue.  Always 
            included in retval, but may be set to 0.

            "not_trained" - Integer number not added to the training queue.  
            Only appears in retval if its value is non-zero.

            "reason_not_trained" - Dict containing the reason that 
            "not_trained" is set.  Only appears in retval if "not_trained" 
            appears.
                        {   "code" : 1011,
                            "message" : "Not enough food to train a spy.",  },
        """
        pass

    @LacunaObject.set_empire_status
    @Building.call_building_meth
    def view_spies( self, page_number:int = 1, *args, **kwargs ):
        """ Returns info on one page (up to 30) spies.  There are a maximum of 
        three pages of spy data.  
        
        To get info on all of your spies at once, see also view_all_spies().

        Retval includes keys "spy_count" (integer number of spies controlled by 
        this int min) and "spies" (list of spy dicts).  

        Spy dicts are formatted as:
                {
                    "id" : "id-goes-here",
                    "name" : "Jason Bourne",
                    "assignment" : "Idle",
                    "possible_assignments" : [
                        {
                            "task" : "Idle",
                            "recovery" : 0,
                            "skill" : "none"
                        },
                        { another possible assignment },
                        ...
                    ],
                    "level" : 9,
                    "politics" : 0,                         # experience in handling happiness
                    "mayhem" : 20,                          # experience in handling missions involving murder and destruction
                    "theft" : 40,                           # experience in handling missions involving stealing items
                    "intel" : 33,                           # experience in handling missions involving information and spies
                    "offense_rating" : 570,
                    "defense_rating" : 150,
                    "assigned_to" : {                       # Where the spy is located right now
                        "body_id" : "id-goes-here",
                        "name" : "Earth",
                        "x" : 40,
                        "y" : -71
                    },
                    "based_from" : {                        # The spy's "home" - from whence he is controlled.
                        "body_id" : "id-goes-here",
                        "name" : "Earth",
                        "x" : 40,
                        "y" : -71
                    },
                    "is_available" : 1, # can be reassigned
                    "available_on" : "01 31 2010 13:09:05 +0600", # if can't be reassigned, this is when will be available
                    "started_assignment" : "01 31 2010 13:09:05 +0600",
                    "seconds_remaining" : 45,
                                "mission_count" : {
                                        "offensive" : 149,
                                        "defensive" : 149
                                }
                },
        """
        pass

    @LacunaObject.set_empire_status
    @Building.call_building_meth
    def view_all_spies( self, *args, **kwargs ):
        """ Returns information on all of the spies controlled from this 
        planet.

        Retval is identical to view_spies(), except that the list can hold up 
        to 90, instead of only 30, entries.
        """
        pass

    @LacunaObject.set_empire_status
    @Building.call_building_meth
    def burn_spy( self, spy_id:int, *args, **kwargs ):
        """ Burns (deletes) an existing spy. """
        pass

    @LacunaObject.set_empire_status
    @Building.call_building_meth
    def name_spy( self, spy_id:int, name:str, *args, **kwargs ):
        """ Renames an existing spy."""
        pass

    @LacunaObject.set_empire_status
    @Building.call_building_meth
    def assign_spy( self, spy_id:int, assignment:str, *args, **kwargs ):
        """ Assigns a spy to a task.
        
        Possible assignments for each spy can be found by calling view_spies() 
        or view_all_spies().  A full list of all possible assignments can be 
        found at:
            https://us1.lacunaexpanse.com/api/Intelligence.html#assignment

        Requires captcha.

        Retval includes:
            "mission" - dict; result of running the mission (assignment).
                    {   "result" : "Failure",
                        "message_id" : "id-goes-here",
                        "reason" : "I'm under heavy fire over here!"    },
                Possible values for 'result' are:
                    Accepted    - Nothing happened as a result of the 
                                  assignment, as to Counter Espionage or Idle.
                    Success     - The mission succeeded and your spy won.
                    Bounce      - The mission began, but was foiled.  
                                  Essentially a draw.  
                    Failure     - The mission failed miserably.  Your spy is 
                                  probably knocked out, in jail, or dead.
                The message_id listed is the ID of a message in your inbox 
                containing details of the result of the mission.  Not all 
                missions will include a message_id (eg 'Idle').

            "spy" - dict; same as that returned by view_spies()
        """
        pass

    @LacunaObject.set_empire_status
    @Building.call_building_meth
    def subsidize_training( self, *args, **kwargs ):
        """ Subsidizes training of all spies currently in the queue.

        Costs 1 E per spy.
        """
        pass

