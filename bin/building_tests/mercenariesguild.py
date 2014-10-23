
import os, sys
bindir = os.path.abspath(os.path.dirname(__file__))
libdir = bindir + "/../../lib"
sys.path.append(libdir)

import lacuna as lac

glc = lac.clients.Member(
    config_file = bindir + "/../../etc/lacuna.cfg",
    #config_section = 'my_sitter',
    config_section = 'play_test',
)
my_planet   = glc.get_body_byname( 'bmots rof 1.1' )
mercs       = my_planet.get_building_coords( -2, -2 )


### See what's available for sale from other empires
###
#rva = mercs.view_market()
#print( "There are currently", rva['trade_count'], "total trades available.")
#print( "We're viewing trade page number {}.".format(rva['page_number']) )
#glc.pp.pprint( rva['trades'] )


### Find the cheapest available merc and buy him
### 
### CAREFUL WITH THIS - it will buy the cheapest merc trade on page 1.  
### "cheapest merc trade" may well be more than you're willing to spend on a 
### test.
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
#rvd = mercs.get_spies()
#glc.pp.pprint( rvd['spies'] )


### Find out what trade ships you have available
### "trade ships" here means "spy pods" - nothing else will work.
###
#rve = mercs.get_trade_ships()
#glc.pp.pprint( rve['ships'] )


### Add one of your spies to the trade market
###
#name_to_sell = '1.1 spy 90'
#asking_price = 10.5
### Optional - get a ship to send the merc
#rvf = mercs.get_trade_ships()
#ship_id = rvf['ships'][0]['id']
### Find the correctly-named spy, add him as a trade.
#spies = mercs.get_spies()['spies']
#spy_to_sell = {}
#for i in spies:
#    if i['name'] == name_to_sell:
#        spy_to_sell = i
#        break
#if not 'name' in spy_to_sell:
#    raise KeyError("Could not find the requested spy by name.")
#rvg = mercs.add_to_market( spy_to_sell['id'], asking_price, ship_id )
#print( "Trade is up; its ID is", rvg['trade_id'] )


### Check on trades I've offered
###
#rvh = mercs.view_my_market()
#del( rvh['status'] )
#glc.pp.pprint( rvh )


### Withdraw the first trade I have listed
###
#rvi = mercs.view_my_market()
#trade_id = rvi['trades'][0]['id']
#rvj = mercs.withdraw_from_market( trade_id )
#print("Trade ID {} has been withdrawn from the market.".format(trade_id) )


### Logout at the end of each test run so you can see where the captcha prompt 
### happens.  Comment this out if you don't care about seeing more than one 
### captcha.
glc.logout()

