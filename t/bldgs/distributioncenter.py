
import os, sys
bindir = os.path.abspath(os.path.dirname(sys.argv[0]))
libdir = bindir + "/../../lib"
sys.path.append(libdir)

import lacuna as lac

glc = lac.clients.Member(
    config_file = bindir + "/../../etc/lacuna.cfg",
    config_section = 'play_test',
)
my_planet = glc.get_body_byname( 'bmots support 02' )
dist = my_planet.get_buildings_bytype( 'distributioncenter', 0, 1 )[0]


### View the dist ctr
###
#view = dist.view( )
#if view.can:
#    print( "I can reserve a max of {:,} resources for {:,} seconds."
#        .format(view.max_reserve_size, view.max_reserve_duration)
#    )
#else:
#    print( "I can't reserve anything right now because there's already stuff being reserved." )
#print( "" )
#for r in view.resources.all_resources:
#    quan = eval("view.resources."+r)
#    print( "I currently have {:,} {} reserved".format(quan, r) )


### List resources onsite to see what can be reserved
###
#res, space = dist.get_stored_resources( )
#print( "Each resource unit takes up {:,} unit of reserve space.".format(space) )
#print( "I have {:,} water stored".format(res.water) )
#print( "I have {:,} anthracite stored".format(res.anthracite) )


### Reserve specific resources
###
res = [
    { 
        'type': 'apple',
        'quantity': 10
    },
    { 
        'type': 'energy',
        'quantity': 11
    },
    { 
        'type': 'cheese',
        'quantity': 12
    },
]
#view = dist.reserve( res )
#for r in view.resources.all_resources:
#    quan = eval("view.resources."+r)
#    if quan:
#        print( "I currently have {:,} {} reserved".format(quan, r) )



### Release all reserved resources
###
#view = dist.release_reserve( )
#if view.can:
#    print( "I can now store more resources because I just released what I'd had in there." )


