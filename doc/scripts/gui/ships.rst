
Ship GUI
========

Builds and scuttles ships.

This script is a work in progress.  Ship scuttling works just fine.  Ship 
building works fine if you're not building a lot.

But the ship builder is supposed to be able to keep your build queues full, 
continually building more ships until the total number you requested has been 
built.  This part is still not exactly working correctly.

Since the scuttler works, and is useful, the script has been added to Monty, 
but please keep in mind that the builder isn't quite ready yet.

Building Ships
--------------
The shipbuilder will build as many ships as you want, up to the number of 
docks you have available.

If you tell it to build more ships than you have available shipyard slots, it 
will build what it can and then go to sleep.  It will automatically wake up 
when it's time to do so, and add more ships to the shipyard build queues.

You do have to remember not to close the program; it will only continue to add 
ships to the queues as long as it's actually running.

So if you want it to build 1000 sweepers and 200 snarks, tell it to do so, 
then minimize it and wait.

You can mass build ships on as many of your planets as you like at the same 
time.

Scuttling Ships
---------------
This scuttles ships.  I'm not real sure what else to say about it :)

