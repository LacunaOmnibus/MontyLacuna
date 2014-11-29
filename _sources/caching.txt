
.. _caching:

Caching
=======

Overview
--------
Almost every MontyLacuna method call represents a communication with the TLE 
server.  This communication takes time, and an additional second is used by 
MontyLacuna, per call, to make sure that we don't swamp the server with too 
many requests, which would result in a mandatory one minute lockout.

Often, your code will need to re-access the same information more than once, 
or even access information that you've recently accessed in an entirely 
different script.  In these cases, you can make use of the client.Member 
class's built-in caching facility.

Synopsis
--------
::

    import lacuna

    my_client = lacuna.clients.Member( connection args )

    ### Caching is not turned on by default.

    my_planet_one = my_client.get_body_byname("Earth")    # takes 1-3 seconds
    my_planet_one = my_client.get_body_byname("Earth")    # takes 1-3 seconds

    my_client.cache_on( 'my_planets', 3600 )              # Turn caching on

    my_planet_one = my_client.get_body_byname("Earth")    # takes 1-3 seconds, but result was cached
    my_planet_one = my_client.get_body_byname("Earth")    # takes 4 or 5 milliseconds

    my_planet_one = my_client.get_body_byname("Mars")     # takes 1-3 seconds, but result was cached
    my_planet_one = my_client.get_body_byname("Mars")     # takes 4 or 5 milliseconds

    my_client.cache_on( 'my_buildings', 3600 )            # Switch to a different cache namespace
    sps = planet.get_buildings_bytype( 'spaceport' )      # Get all spaceports on the planet
    ...time passes...
    sps = planet.get_buildings_bytype( 'spaceport' )      # Get spaceports again, much faster

    my_client.cache_on( 'my_planets', 3600 )              # Switch back to the my_planets namespace
    my_client.cache_clear( 'my_planets' )                 # clear this cache, but don't turn it off

    my_planet_one = my_client.get_body_byname("Earth")    # takes 1-3 seconds, but result was cached
    my_planet_one = my_client.get_body_byname("Earth")    # takes 4 or 5 milliseconds

    my_client.cache_off()                                 # Turn caching off, but don't clear entries

    my_planet_one = my_client.get_body_byname("Earth")    # takes 1-3 seconds
    my_planet_one = my_client.get_body_byname("Earth")    # takes 1-3 seconds

    my_client.cache_on( 'my_planets', 3600 )              # Turn caching back on

    my_planet_one = my_client.get_body_byname("Earth")    # takes 4 or 5 milliseconds

Description
-----------
When you turn caching on, you pass in a name and an expiration time.  While 
caching is on, every request to the server will be curried, so when two 
identical requests are made, the second returns the same data that was returned 
by the first, without having to re-query the server.  You can have multiple 
caches, switching between them by simply calling cache_on() with the name of the 
cache you want to use.

It's important to understand that the name you're passing to ``cache_on()`` is a 
namespace name, not a specific cache key.  Individual cache keys will be 
generated for you, and are invisible to you.  So a single cache name can safely 
contain multiple different types of data.  The cache keys are determined by both 
the server method you're calling and the parameters you're passing to that 
method.

Certain actions you take will invalidate your cached data.  In this scenario:
    * Turn caching on
    * Get list of buildings on the surface of a planet
    * Build a new building on that planet
    * Get list of buildings on the surface of that same planet

      * GONNNGG!  Since caching is turned on, we'll get the same list we had
        before, which does not include our new building.

In that case, you'd want to clear out the cache after constructing your new 
building; this would cause the next "get list of buildings" to actually hit the 
server again, and the retrieved list would now contain your new building.

You're encouraged to use multiple named caches in your code.  This way, you can 
clear out any cache namespace that becomes invalid because of some other action, 
while maintaining the cached data in your other namespaces.

Cached data is saved to local files, so accessing the same named cache between 
different runs of a script, or even between two entirely different scripts, will 
make use of your caches.

.. module:: lacuna.clients
.. automethod:: Member.cache_on
   :noindex:
.. automethod:: Member.cache_off
   :noindex:
.. automethod:: Member.cache_clear
   :noindex:

