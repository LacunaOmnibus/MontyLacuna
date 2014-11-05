
import os, sys

bindir = os.path.abspath(os.path.dirname(__file__))
libdir = bindir + "/../lib"
sys.path.append(libdir)
import lacuna as lac

guest = lac.clients.Guest()

tmt = lac.clients.Member(
    config_file = bindir + "/../etc/lacuna.cfg",
    config_section = 'my_sitter',
)
io = lac.clients.Member(
    config_file = bindir + "/../etc/lacuna.cfg",
    config_section = 'io',
)
sil = lac.clients.Member(
    config_file = bindir + "/../etc/lacuna.cfg",
    config_section = 'sil',
)

### Example of connecting with a non-logged-in guest account
for n in ['tmtowtdi', 'fake_name']:
    if guest.is_name_available(n):
        print(n, "is available for use.")
    else:
        print(n, "is taken, and is not available for use.")


### Almost everything else requires a logged-in account.
print( "Number of RPCs used today by {} is {}". format(tmt.empire.name, tmt.empire.rpc_count) )
print( "Number of RPCs used today by {} is {}". format(sil.empire.name, sil.empire.rpc_count) )
print( "Number of RPCs used today by {} is {}". format(io.empire.name, io.empire.rpc_count) )


### 
### From a logged-in client, you have access to most other objects via get_*() methods:
### 
# alliance = tmt.get_alliance();                  # Generic Alliance object, NOT set to any specific alliance.
# my_alliance = tmt.get_my_alliance();            # This one is set to my empire's alliance.
# body1 = tmt.get_body( integer body ID );        # Gotta go dig up the planet's ID.  Ugh.
# body2 = tmt.get_body_byname( Name of a body );  # Yay, I already know my planet's name.
# inbox = tmt.get_inbox();                        # My empire's mail inbox
# mymap = tmt.get_map();                          # Starmap
# mystats = tmt.get_stats();                      # Stats

