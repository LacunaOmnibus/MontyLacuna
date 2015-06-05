#!/usr/bin/python3

import logging, os, sys
bindir = os.path.abspath(os.path.dirname(sys.argv[0]))
libdir = bindir + "/../lib"
sys.path.append(libdir)

import lacuna
import lacuna.binutils.libglyph_repair as lib

### Get library class instance
repair = lib.GlyphRepair()

### get logger
l = repair.client.user_logger

### If there's damage to any glyph buildings, repair it.
for pname in repair.planets:
    repair.set_current_planet(pname)
    if repair.find_damage():
        l.info("I found glyph building damage on {}.  Repairing it.".format(pname))
        repair.do_repairs()
    else:
        l.info("No glyph buildings on {} are damaged.".format(pname))

