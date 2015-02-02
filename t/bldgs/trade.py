
import os, re, sys
bindir = os.path.abspath(os.path.dirname(sys.argv[0]))
libdir = bindir + "/../../lib"
sys.path.append(libdir)

import lacuna as lac

glc = lac.clients.Member(
    config_file = bindir + "/../../etc/lacuna.cfg",
    config_section = 'sitter',
)
my_planet   = glc.get_body_byname( 'some_planet' )
trade       = my_planet.get_buildings_bytype( 'trade', 0, 1 )[0]


### View ships available to be traded
###
#ships, space_used = trade.get_ships()
#print( "Each ship will take up {:,} units of cargo hold space.".format(space_used) )
#for i in ships[0:3]:
#    print(i.name)


### View prisoners available to be traded
###
#pris, space_used = trade.get_prisoners()
#for i in pris[0:3]:
#   print(i.name)


### View plans available to be traded
###
#plans, space_used = trade.get_plan_summary()
#for i in plans[0:3]:
#    print(i.name)


### View glyphs available to be traded
###
#glyphs, space_used = trade.get_glyph_summary()
#for i in glyphs[0:3]:
#    print(i.type)


### View my trades
###
#trades, count, page = trade.view_my_market()
#for i in trades[0:3]:
#    print( "I'm asking ",i.ask, "E for:" )
#    glc.pp.pprint( i.offer )
#    print("--------")
#print( "I have {} trades up; the above is from page {}".format(count, page) )


### Add a trade
###
if False:
    tradeable_ships, space_each = trade.get_ships()
    offer = [
        {
            'type': 'bean',
            'quantity': 1
        },
        {   'type':         'glyph',
            'name':         'bauxite',
            'quantity':     1   },
        {   'type':                 'plan',
            'plan_type':            'Permanent_AlgaePond',
            'level':                1,
            'extra_build_level':    0,
            'quantity':             1   },
        {   'type':     'ship',
            'ship_id':  tradeable_ships[0].id   },
    ]
    ask = 99.4
    options = { 'ship_id': trade.get_trade_ships()[0].id }
    trade_id = trade.add_to_market( offer, ask, options )
    print("I just added trade ID", trade_id)


### Withdraw one of your trades
###
#trades, count, page = trade.view_my_market()
#trade.withdraw_from_market( trades[0].id )
#print( "I just withdrew trade", trades[0].id, "from the market." )


### View trades offered by others
###
#trades, count, page = trade.view_market( filter = 'plan' )
#for i in trades[0:3]:
#    print( "{} is asking {} E.  It'll take {} seconds to get here.".format(i.empire['name'], i.ask, i.delivery['duration']) )
#    glc.pp.pprint( i.offer )
#    print("--------")


### Buy a trade
###
#trades, count, page = trade.view_market( filter = 'plan' )
#trade.accept_from_market( trades[0].id )


### View ships available for using as merch carriers.
###
#ships = trade.get_trade_ships()
#for i in ships[0:3]:
#    print( i.name )


### View ships on or available for waste duty
###
#ships = trade.get_waste_ships()
#for i in ships[0:10]:
#    print( i.name, "- -", i.task )


### View ships on or available for waste duty
###
#ships = trade.get_supply_ships()
#for i in ships[0:10]:
#    print( i.name, "- -", i.task )


### View active supply chains
###
#chain, max = trade.view_supply_chains()
#print( "This trademin can support", max, "supply chains." )
#for i in chain:
#    print( "Chain ID {} is going to {} and carrying {} {} per hour at {} efficiency. "
#        .format(i.id, i.body['name'], i.resource_hour, i.resource_type, i.percent_transferred)
#    )


### View active waste chains
###
#chain = trade.view_waste_chains()
#for i in chain:
#    print( "Chain ID {} is going to {} and carrying {} waste per hour at {} efficiency. "
#        .format(i.id, i.star['name'], i.waste_hour, i.percent_transferred)
#    )


### See resources available for trade onsite
###
#res = trade.get_stored_resources()
#print( "I have {:,} water, {:,} waste, and {:,} bauxite ready for trade."
#    .format(res.water, res.waste, res.bauxite)
#)


### Push items to another of your colonies
###
if False:
    tradeable_ships, space_each = trade.get_ships()
    target_planet = glc.get_body_byname( 'bmots rof 1.2' )
    items = [
        {
            'type': 'bean',
            'quantity': 1
        },
        {   'type':         'glyph',
            'name':         'bauxite',
            'quantity':     1   },
    ]
    options = { 'ship_id': trade.get_trade_ships()[0].id }
    ship = trade.push_items( target_planet.id, items, options )
    print( "I just pushed items to {} on {}".format(target_planet.name, ship.name) )



### Do this for each run so you can see the captchas pop up where required.
#glc.logout();




