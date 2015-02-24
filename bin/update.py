#!/usr/bin/python3

import os, sys, zipfile
libdir  = os.path.abspath(os.path.dirname(sys.argv[0])) + "/../lib"
sys.path.append(libdir)

import lacuna.binutils.libupdate as lib
up = lib.Update()

print( "Downloading the most recent MontyLacuna..." )
up.download_and_extract_zipfile()

print( "Updating your MontyLacuna..." )
cnt = 0
for tmp_path, dirs, files in os.walk( os.path.join(up.tmpdir, "MontyLacuna-master") ):
    for name in files:
        up.copy_mismatched_file( tmp_path, name )
#up.consuela()

print( "Done." )

