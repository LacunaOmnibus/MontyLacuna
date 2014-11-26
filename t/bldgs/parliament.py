
import os, re, sys
bindir = os.path.abspath(os.path.dirname(sys.argv[0]))
libdir = bindir + "/../../lib"
sys.path.append(libdir)

import lacuna as lac

glc = lac.clients.Member(
    config_file = bindir + "/../../etc/lacuna.cfg",
    config_section = 'my_real',
)

my_station = glc.get_body_byname( 'Some Station' )
parl = my_station.get_buildings_bytype( 'parliament' )[0]



### View laws
### 
#laws = parl.view_laws( my_station.id )
#for i in laws:
#    if re.match("^Seize", i.name):
#        ### Don't list all the seizure laws.
#        continue
#    print( "{} is described as {}, and was enacted on {}."
#        .format(i.name, i.description, i.date_enacted)
#    )


### View propositions
### 
#props = parl.view_propositions()
#for i in props:
#    print( "{} needs {} votes to pass, and has {} yes and {} no votes.  It was proposed by {}."
#        .format(i.name, i.votes_needed, i.votes_yes, i.votes_no, i.proposed_by.name)
#    )


### Propose a writ
### 
#prop = parl.propose_writ('nopush 3', 'a description')
#print( "I just proposed the writ {}.".format(prop.name) )


### Cast your vote on a proposition
###
#props = parl.view_propositions()
#for i in props:
#    if hasattr(i, 'my_vote'):
#        bule = 'yes' if i.my_vote else 'no'
#        print( "I already voted {} on the '{}' prop.".format(bule, i.name) )
#    else:
#        ### Pick one.
#        #prop = parl.cast_vote( i.id, 1 )   # yes
#        prop = parl.cast_vote( i.id, 0 )   # no
#        ### 
#        bule = 'yes' if prop.my_vote else 'no'
#        print( "I just now voted {} on the '{}' prop.".format(bule, prop.name) )


### Propose repealing an existing law
### 
#laws = parl.view_laws( my_station.id )
#for i in laws:
#    if i.name == 'nopush 2':       # The name of a law to propose repealing
#        prop = parl.propose_repeal_law( i.id )
#        print( "I just proposed to repeal the law {}.".format(prop.name) )


### View taxes
### 
#taxes = parl.view_taxes_collected()
#for i in taxes:
#    print( "{} paid {} today, and {} yesterday.  Total payments this week were {}."
#        .format(i.name, i.paid[0], i.paid[1], i.total)
#    )


### Get stars within the jurisdiction of this station
### 
#stars = parl.get_stars_in_jurisdiction()
#for i in stars:
#    print( "{} ({}, {}), in zone {}, is {}."
#        .format(i.name, i.x, i.y, i.zone, i.color)
#    )
#print( "-------------------------------" )


### Get the bodies orbiting one of the planets in our jurisdiction
### 
#stars = parl.get_stars_in_jurisdiction()
#star = stars[0]
#planets = parl.get_bodies_for_star_in_jurisdiction( star.id )
#for i in planets:
#    print( "{} is at ({}, {}).  It has {} anthracite.".format(i.name, i.x, i.y, i.ore.anthracite) )
#    if hasattr(i, 'station'):
#        print( "\tIts star, {}, has been seized by the station {}.".format(i.star_name, i.station.name) )


### Get mining platforms at a roid orbiting one of the stars in our 
### jurisdiction.
### 
#stars = parl.get_stars_in_jurisdiction()
#star = ''
#for s in stars:
#    if s.name == 'Fow Aendeahl Jo': # use a star that you know has roids with plats on it to test.
#        star = s
#        break
#if not star:
#    print( "I couldn't find the star you were looking for." )
#    quit()
#
#bodies = parl.get_bodies_for_star_in_jurisdiction( star.id )
#for i in bodies:
#    if i.type == 'asteroid':
#        print( "{} is an asteroid.  Checking for platforms...".format(i.name) )
#        plats = parl.get_mining_platforms_for_asteroid_in_jurisdiction( i.id )
#        for j in plats:
#            print( "The empire '{}' has platform ID {} on {}."
#                .format(j.empire.name, j.id, i.name)
#            )



###
### All of the proposal methods work more-or-less the same way.  They do take 
### different arguments; sometimes you need to send along a planet ID or a 
### string message or whatever.  But they're all essentially the same code, so 
### they're not all being tested here.
###
### They _should_ all work, but if you're planning on using one in earnest, 
### give it a test run first.
###


### Propose transferring station ownership
### 
#my_ally = glc.get_my_alliance()
#new_owner = ''
#for i in my_ally.members:
#    if i.name == 'The Name of the Empire to Take Over Control':
#        new_owner = i
#        break
#prop = parl.propose_transfer_station_ownership( i.id )
#print( "I just proposed {}.".format(prop.description) )




