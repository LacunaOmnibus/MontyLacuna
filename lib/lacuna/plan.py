
import lacuna.bc

class Plan(lacuna.bc.SubClass):
    """ Plan base class """

class OwnedPlan(Plan):
    """ Returned from viewing plans you currently own, as in your PCC.

    Attributes::

        name                "Volcano"
        plan_type           "Permanent_Volcano"
        level               1
        extra_build_level   5
        quantity            23

    plan_type is what needs to be sent to 
    :meth:`lacuna.buildings.callable.trade.trade.add_to_market` or 
    :meth:`lacuna.buildings.callable.transporter.transporter.add_to_market` to 
    trade the plan.
    """
    def __init__(self, client, mydict, *args, **kwargs):
        if not 'extra_build_level' in mydict:
            mydict['extra_build_level'] = 0
        super().__init__(client, mydict)

class PotentialSSPlan(Plan):
    """ Returned from viewing plans you can build, as in your Space Station Lab
    (A).

    Attributes::

        name                "Interstellar Broadcast System"
        type                "ibs"
        image               "ibs"
        url                 "/ibs"
    """

class LevelCosts(Plan):
    """ Not a plan at all, but the costs associated with creating a plan at your 
    SS Lab.

    Attributes::

        level   1,
        food    10000
        ore     10000
        water   10000
        energy  10000
        waste   2500
        time    1200 (in seconds)
    """
