
import os, re, sys
bindir = os.path.abspath(os.path.dirname(__file__))
libdir = bindir + "/../../lib"
sys.path.append(libdir)

import lacuna as lac

glc = lac.clients.Member(
    config_file = bindir + "/../../etc/lacuna.cfg",
    #config_section = 'my_sitter',
    config_section = 'play_test',
)
my_planet   = glc.get_body_byname( 'bmots rof 2.1' )
rec         = my_planet.get_building_coords( 5, -3 )


### View recycling stats
###
#job_stats = rec.view()
#print( "This recycle building will take {} seconds per resource converted, up to a max {} resources."
#    .format(job_stats.seconds_per_resource, job_stats.max_recycle)
#)


### Recycle some waste and subsidize the job
###
#rec.recycle( 24500, 0, 0, 1 )
#print( "Job subsidized and complete" )


### Recycle some waste
###
#rec.recycle( 24500, 0, 0, 0 )
#print( "Recycling ongoing." )


### Subsidize the ongoing job for 2 e
###
#rec.subsidize_recycling()
#print( "Current job has been subsidized." )


