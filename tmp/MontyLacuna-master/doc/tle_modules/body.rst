
Body
=================

In TLE, a ``body`` is any thingy that orbits a star.  Habitable planets, gas 
giants, space stations, and asteroids are all bodies.

Most of the time, the bodies you'll be dealing with will by 
:class:`lacuna.body.MyBody` objects.  *This includes Space Stations*.

There is a :class:`lacuna.body.SpaceStation` class down below, but don't be 
confused by that.  That class *only* ever gets returned rarely, and does not 
contain much actual information (it gets returned as a list in a 
:class:`lacuna.alliance.MyAlliance` or :class:`lacuna.alliance.Profile` 
object).

So if you're iterating through your space stations (with 
``self.empire.station_names`` or similar), you'll be dealing with 
:class:`lacuna.body.MyBody` objects.

.. automodule:: lacuna.body
   :members:
   :show-inheritance:

