
import os, sys
bindir = os.path.abspath(os.path.dirname(__file__))
libdir = bindir + "/../../lib"
sys.path.append(libdir)

import lacuna as lac
from lacuna.exceptions import CaptchaResponseError

glc = lac.clients.Member(
    config_file = bindir + "/../../etc/lacuna.cfg",
    config_section = 'my_sitter',
)
my_planet   = glc.get_body_byname( 'bmots rof 1.4' )
gen         = my_planet.get_building_coords( 2, -5 )


### Prepare for experimentation
### 
#rva = gen.prepare_experiment()
#del( rva['status'] )
#glc.pp.pprint( rva )

### Rename your species
###     name: Blarg
###     description:  http://tmtowtdi.github.io/LacunaWaX/ Alpha version of 
###     WaX that works on PT - 
###     https://github.com/tmtowtdi/LacunaWaX/releases/tag/untagged-39b9eaa89f81d7fc2f51 
new_species = {
    "name": "Grundle <> foobar",
    "description": "new description"
}
rvb = gen.rename_species( new_species )
glc.pp.pprint( rvb )

