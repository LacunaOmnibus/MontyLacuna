
from lacuna.bc import LacunaObject
from lacuna.building import MyBuilding

class thedillonforge(MyBuilding):
    path = 'thedillonforge'

    def __init__( self, client, body_id:int = 0, building_id:int = 0 ):
        super().__init__( client, body_id, building_id )


    def _marshal_view(self, rv):
        """ Multiple methods return the same data. """

        make_plans_list = []
        if 'make_plan' in rv['tasks']:
            for i in rv['tasks']['make_plan']:
                make_plans_list.append( MakePlan(self.client, i) )

        split_plans_list = []
        if 'split_plan' in rv['tasks']:
            for i in rv['tasks']['split_plan']:
                split_plans_list.append( SplitPlan(self.client, i) )

        ct = 'None'
        if 'current_task' in rv['tasks']:
            ct = rv['tasks']['current_task']

        can = 0
        if 'can' in rv['tasks']:
            can = rv['tasks']['can']

        sr = 0
        if 'seconds_remaining' in rv['tasks']:
            sr = rv['tasks']['seconds_remaining']

        wrk = 0
        if 'working' in rv['tasks']:
            wrk = rv['tasks']['working']

        sub = 0
        if 'subsidy_cost' in rv['tasks']:
            sub = rv['tasks']['subsidy_cost']

        return(
            make_plans_list, split_plans_list,
            ct, sr, can, wrk, sub
        )

    @MyBuilding.call_returning_meth
    def view( self, *args, **kwargs ):
        """ View plans that can be built and split.

        Returns:
            - make_list -- List of MakePlan objects
            - split_list -- List of SplitPlan objects
            - current_task -- "make_plan", "split_plan", or "None"
            - seconds_remaining -- How many seconds left on the current task.  0 if the forge isn't doing anything.
            - can -- 1 if the forge is available, 0 if it's working.
            - working -- Human-readable description of the task the forge is working on right now.  "Making Crater 6.0"
            - subsidy_cost -- Always 2, whether the forge is working or not.
        """
        return self._marshal_view( kwargs['rslt'] )

    @MyBuilding.call_returning_meth
    def make_plan( self, perl_class:str, level:int = 1, *args, **kwargs ):
        """ Starts making a plan in the forge.

        Arguments:
            - perl_class -- As displayed in MakeClass.perl_class
            - level -- Optional integer level to build.  Defaults to 1.

        Returns a tuple is the same as for view().  make_list and split_list are 
        included included in the tuple, but they will both be empty lists.
        """
        return self._marshal_view( kwargs['rslt'] )

    @MyBuilding.call_returning_meth
    def split_plan( self, perl_class:str, level:int = 1, extra_build_level:int = 0, quantity:int = 1, *args, **kwargs ):
        """ Starts splitting a plan in the forge.

        Arguments:
            - perl_class -- As displayed in MakeClass.perl_class
            - level -- Optional integer level to build.  Defaults to 1.
            - extra_build_level -- Optional integer additional build level.  Defaults to 0.
            - quantity -- Optional integer number to build.  Defaults to 1.

        Returns a tuple is the same as for view().  make_list and split_list are 
        included included in the tuple, but they will both be empty lists.
        """
        return self._marshal_view( kwargs['rslt'] )

    @LacunaObject.set_empire_status
    @MyBuilding.call_building_meth
    def subsidize( self, *args, **kwargs ):
        """ Spends 2 E to subsidize the current job.
        
        Raises ServerError 1010 if the forge isn't doing anything right now.
        """
        pass



class Plan():
    """ Plan base class """
    def __init__( self, client, mydict:dict, *args, **kwargs ):
        self.client = client

        if 'class' in mydict:
            setattr(self, 'perl_class', mydict['class'])
            del mydict['class']

        for k, v in mydict.items():
            setattr(self, k, v)

class MakePlan(Plan):
    """
    Attributes:
        >>> 
        name                    "Algae",
        max_level               10,
        perl_class              "Food::Algae",
        reset_sec_per_level     5000,

    "perl_class" is named "class" in the return from TLE, but "class" is a 
    reserved word in Python so I can't make an attribute with that name.

    "reset_sec_per_level" is the number of seconds it'll take to build the plan 
        (reset_sec_per_level * (level you're building) == total seconds)
    """

class SplitPlan(Plan):
    """
    Attributes:
        >>> 
        name                "Beach [10]",
        perl_class          "Permanent::Beach10",
        level               1,
        extra_build_level   6,
        fail_chance         50,
        reset_seconds       50400

    "perl_class" is named "class" in the return from TLE, but "class" is a 
    reserved word in Python so I can't make an attribute with that name.
    
    "reset_seconds" is the number of seconds it'll take to split this plan.
    """


