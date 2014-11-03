
import os, sys
bindir = os.path.abspath(os.path.dirname(__file__))
libdir = bindir + "/../../lib"
sys.path.append(libdir)

import lacuna as lac

glc = lac.clients.Member(
    config_file = bindir + "/../../etc/lacuna.cfg",
    config_section = 'my_sitter',
    #config_section = 'play_test',
)
my_planet   = glc.get_body_byname( 'bmots rof 1.1' )
mercs       = my_planet.get_building_coords( -2, -2 )


### Any of the test blocks in here without CHECK marks _have_ been oopified 
### and tested.


### See what's available for sale from other empires
###
#trades, num, page = mercs.view_market()
#print( "There are currently", num, "total trades available.")
#print( "We're viewing trade page number {}.".format(page) )
#for i in trades[0:3]:
#    print( "'{}' (trade id {} from body id {}) was offered on {} for {} E."
#        .format(i.offer_summary, i.id, i.body_id, i.date_offered, i.ask)
#    )


### Find the cheapest available merc and buy him
### CHECK need PT back to test this.
### 
### buys the cheapest merc trade on page 1.  "cheapest merc trade" may well be 
### more than you're willing to spend on a test.
###
#rvb = mercs.view_market()
#min_cost = 9999
#buy_this = {}
#for i in rvb['trades']:
#    if float(i['ask']) < min_cost:
#        buy_this = i
#        min_cost = float(i['ask'])
#if not 'ask' in buy_this:
#    raise KeyError("Unable to find the lowest cost trade.")
#print( "The ID of the trade you're about to accept is {}.".format(buy_this['id']) )
#rvc = mercs.accept_from_market( buy_this['id'] )
#print( "For {} E paid to {}, we just bought {}\n".format(buy_this['ask'], buy_this['empire']['name'], ''.join(buy_this['offer'])) )


### Find which of my spies are available for adding as trades
###
#spies = mercs.get_spies()
#print( "Spies take up 350 units of cargo each.  These spies are available for trade:" )
#for s in spies:
#    print( "\t", s.name )


### Find out what trade ships you have available
### "trade ships" here means "spy pods" - nothing else will work.
###
# This can be done either with an unknown target...
#ships = mercs.get_trade_ships()

# ...or with a known target...
#target_planet = glc.get_body_byname( 'bmots rof 2.1' )
#ships = mercs.get_trade_ships( target_planet.id )

# ...either way:
#for i in ships:
#    print( "Ship {} (of type {}) is ready for trade.  Travel time is estimated at '{}'.".format(i.name, i.type, i.estimated_travel_time) )


### Add one of your spies to the trade market
### CHECK need PT back up again
###
#name_to_sell = '1.1 spy 90'
#asking_price = 99.5
### Optional - get a ship to send the merc
#ships = mercs.get_trade_ships()
#ship_id = ships[0].id
### Find the correctly-named spy, add him as a trade.
#spies = mercs.get_spies()
#spy_to_sell = {}
#for i in spies:
#    if i.name == name_to_sell:
#        spy_to_sell = i
#        break
#if not spy_to_sell:
#    raise KeyError("Could not find the requested spy by name.")
#trade_id = mercs.add_to_market( spy_to_sell.id, asking_price )
###trade_id = mercs.add_to_market( spy_to_sell.id, asking_price, ship_id )
#print( "Trade is up; its ID is", trade_id )


### Check on trades I've offered
###
#trades, count, page = mercs.view_my_market()
#print( "I have {} trades up on page {}".format(count, page) )
#for i in trades:
#    print( "'{}' was offered at {}.".format(i.offer, i.date_offered) )


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

