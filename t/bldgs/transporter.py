
import os, re, sys
bindir = os.path.abspath(os.path.dirname(sys.argv[0]))
libdir = bindir + "/../../lib"
sys.path.append(libdir)

import lacuna as lac

glc = lac.clients.Member(
    config_file = bindir + "/../../etc/lacuna.cfg",
    config_section = 'my_sitter',
    #config_section = 'play_test',
)
my_planet   = glc.get_body_byname( 'bmots rof 1.1' )
trade       = my_planet.get_building_coords( 5, -4 )


### View sst
###
#trade_max = trade.view()
#print( "This SST can trade a max of", trade_max, "units per trade." )


### View prisoners available for trading
###
#pris, space_used = trade.get_prisoners()
#for i in pris[0:3]:
#   print(i.name)


### Add a trade
###
#tradeable_ships, space_each = trade.get_ships()
#offer = [
#    {
#        'type': 'bean',
#        'quantity': 1
#    },
#    {   'type':         'glyph',
#        'name':         'bauxite',
#        'quantity':     1   },
#    {   'type':                 'plan',
#        'plan_type':            'Permanent_AlgaePond',
#        'level':                1,
#        'extra_build_level':    0,
#        'quantity':             1   },
#    {   'type':     'ship',
#        'ship_id':  tradeable_ships[0].id   },
#]
#ask = 100
#id = trade.add_to_market( offer, ask )
#print("I just added SST trade ID", id)


### View plans available for trading
###
#plans, space_used = trade.get_plan_summary()
#for i in plans[0:3]:
#    print("plan:", i.name)


### View glyphs available for trading
###
#glyphs, space_used = trade.get_glyph_summary()
#for i in glyphs[0:3]:
#    print("glyph", i.type)


### View my trades
###
#print( trade.body_id )
#print( my_planet.id )
#trades, count, page = trade.view_my_market()
#for i in trades[0:3]:
#    print( "I'm asking ",i.ask, "E for:" )
#    glc.pp.pprint( i.offer )
#    print("--------")
#print( "I have {} trades up; the above is from page {}".format(count, page) )


### Add a trade
###
if False:
    offer = [
        {
            'type': 'bean',
            'quantity': 1
        },
        {   'type':         'glyph',
            'name':         'bauxite',
            'quantity':     1   },
    ]
    ask = 100
    trade_id = trade.add_to_market( offer, ask )
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
#for t in trades:
#    if float(t.ask) < 1:
#        print(t.ask, "- -", t.offer)
#        trade.accept_from_market( t.id )
#        break


### See resources available for trade onsite
###
#res = trade.get_stored_resources()
#glc.pp.pprint( res['resources'] )


### Push items to another of your colonies
###
if False:
    target_planet = glc.get_body_byname( 'bmots rof 1.3' )
    items = [
        {
            'type': 'bean',
            'quantity': 1
        },
        {   'type':         'glyph',
            'name':         'bauxite',
            'quantity':     1   },
    ]
    trade.push_items( target_planet.id, items )
    print( "I just pushed items to {}.".format(target_planet.name) )













### Do this for each run so you can see the captchas pop up where required.
glc.logout();

