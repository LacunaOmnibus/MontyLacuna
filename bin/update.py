#!/usr/bin/python3

import os, sys, zipfile
libdir  = os.path.abspath(os.path.dirname(sys.argv[0])) + "/../lib"
sys.path.append(libdir)

import lacuna.binutils.libupdate as lib
up = lib.Update()
l  = up.client.user_logger

l.info(  "Downloading the most recent MontyLacuna." )
l.info( "This will take a few seconds, depending on your internet connection." )
up.download_and_extract_zipfile()

l.info( "Updating your MontyLacuna..." )
cnt = 0
for tmp_path, dirs, files in os.walk( os.path.join(up.tmpdir, "MontyLacuna-master") ):
    for name in files:
        cnt += up.copy_mismatched_file( tmp_path, name )
up.consuela()

pl = "file was" if cnt == 1 else "files were"
l.info( "{} {} updated.".format(cnt, pl) )

