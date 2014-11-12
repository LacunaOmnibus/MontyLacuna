
import calendar, os, sys
bindir = os.path.abspath(os.path.dirname(__file__))
libdir = bindir + "/../../lib"
sys.path.append(libdir)

import lacuna as lac

glc = lac.clients.Member(
    config_file = bindir + "/../../etc/lacuna.cfg",
    config_section = 'play_test',
)
my_planet   = glc.get_body_byname( 'bmots rof 1.1' )
mercs       = my_planet.get_building_coords( -2, -2 )


### See what's available for sale from other empires
###
#trades, num, page = mercs.view_market()
#print( "There are currently", num, "total trades available.")
#print( "We're viewing trade page number {}.".format(page) )
#for i in trades[0:3]:
#    print( "'{}' (trade id {}) was offered by {} on {} for {} E."
#        .format(i.offer_summary, i.id, i.origin.empire_name, i.date_offered, i.ask)
#    )


### Find the cheapest available merc and buy him
### 
### buys the cheapest merc trade on page 1.  "cheapest merc trade" may well be 
### more than you're willing to spend on a test, so be sure to check that 
### first (or be sure you're running this on PT.)
###
#trades, num, page = mercs.view_market()
#min_cost = 9999
#buy_this = {}
#for i in trades:
#    if float(i.ask) < min_cost:
#        buy_this = i
#        min_cost = float(i.ask)
#if not buy_this:
#    raise KeyError("Unable to find the lowest cost trade.")
#print( "The ID of the trade you're about to accept is {}.".format(buy_this.id) )
#mercs.accept_from_market( buy_this.id )
#print( "For {} E paid to {}, we just bought {}\n".
#    format( buy_this.ask, buy_this.origin.empire_name, buy_this.offer )
#)


### Find which of my spies are available for adding as trades
###
#spies = mercs.get_spies()
#print( "Spies take up 350 units of cargo each.  Some spies I have available for trade:" )
#for s in spies[0:10]:
#    print( "\t", s.name )


### Find out what trade ships you have available
### "trade ships" here means "spy pods" - nothing else will work.
###
### This can be done either with an unknown target.  However, if the target is 
### not known, then we won't get back any estimated_travel_time info:
###     ships = mercs.get_trade_ships()
###
### But with a known target, we do get estimated_travel_time, so we'll test 
### with that instead:
#target_planet = glc.get_body_byname( 'bmots rof 2.1' )
#ships = mercs.get_trade_ships( target_planet.id )
#for i in ships:
#    time = i.sec2time( i.estimated_travel_time )
#    print( "Ship {} (of type {}) is ready for trade."
#        .format( i.name, i.type )
#    )
#    print( "{} seconds is {} days, {} hours, {} minutes and {} seconds."
#        .format(i.estimated_travel_time, time.days, time.hours, time.minutes, time.seconds)
#    )


### Add one of your spies to the trade market
###
#name_to_sell = '1.1 spy 89'
#asking_price = 99.5
###
### We could skip getting a specific ship, but for this test we'll include it.
#ships = mercs.get_trade_ships()
###
### Find the correctly-named spy, add him as a trade.
#spies = mercs.get_spies()
#spy_to_sell = {}
#for i in spies:
#    if i.name == name_to_sell:
#        spy_to_sell = i
#        break
#if not spy_to_sell:
#    raise KeyError("Could not find the requested spy by name.")
###trade_id = mercs.add_to_market( spy_to_sell.id, asking_price ) # if we weren't specifying the ship
#trade_id = mercs.add_to_market( spy_to_sell.id, asking_price, ships[0].id )
#print( "Trade is up; its ID is", trade_id )


### Check on trades I've offered
###
#trades, count, page = mercs.view_my_market()
#print( "I have {} trades up on page {}".format(count, page) )
#for i in trades:
#    print( "'{}' was offered {} E.".format(i.offer, i.date_offered, i.ask) )
#    d = i.tle2time( i.date_offered )
#    print( "That was offered on {} {}, {} at {}:{}:{}."
#        .format(calendar.month_name[d.month], d.day, d.year, d.hour, d.minute, d.second)
#    )


### Withdraw the first trade I have listed
###
#trades, count, page = mercs.view_my_market()
#trade_id = trades[0].id
#mercs.withdraw_from_market( trade_id )
#print("Trade ID {} has been withdrawn from the market.".format(trade_id) )


### Report a trade as abusive
###
#trades, count, page = mercs.view_my_market()
#trade_id = trades['trades'][0].id
#mercs.report_abuse( trade_id )
#print( "Reported trade {} for abuse.".format(trade_id) )


### Logout at the end of each test run so you can see where the captcha prompt 
### happens.  Comment this out if you don't care about seeing more than one 
### captcha.
glc.logout()

