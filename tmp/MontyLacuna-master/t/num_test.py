
import os, sys
bindir = os.path.abspath(os.path.dirname(sys.argv[0]))
libdir = bindir + "/../lib"
sys.path.append(libdir)
import lacuna

client = lacuna.clients.Member(
    config_file = bindir + "/../etc/lacuna.cfg",
    config_section = 'play_test',
)

cand = 1
new = client.get_type( cand )
print( type(new) )              # int

cand = 1.7
new = client.get_type( cand )
print( type(new) )              # float

cand = "one point seven"
new = client.get_type( cand )
print( type(new) )              # str

cand = { 'number': 1.7 }
new = client.get_type( cand )
print( type(new) )              # dict
