#!/usr/bin/python3

import os, imp, sys, zipfile
libdir  = os.path.abspath(os.path.dirname(sys.argv[0])) + "/../lib"
sys.path.append(libdir)

import lacuna
import lacuna.binutils.libupdate as lib
up = lib.Update()
l  = up.client.user_logger

l.info(  "Downloading the most recent MontyLacuna." )
l.info( "This will take a few seconds, depending on your internet connection." )
up.download_and_extract_zipfile()

start_version = lacuna.version
l.info( "Your current MontyLacuna version is {} - checking for updates...".format(start_version) )

cnt = 0
for tmp_path, dirs, files in os.walk( os.path.join(up.tmpdir, "MontyLacuna-master") ):
    for name in files:
        #cnt += up.copy_mismatched_file( tmp_path, name )
        pass
up.consuela()

imp.reload( lacuna )
new_version = lacuna.version

pl = "file was" if cnt == 1 else "files were"
if new_version == start_version:
    if cnt:
        l.info( "Bugfix update; MontyLacuna version is still {}.  {} {} updated."
            .format(new_version, cnt, pl) )
    else:
        l.info( "No updates were found." )
else:
    l.info( "A new MontyLacuna version was found.  You're now using {}.  {} {} updated."
        .format(new_version, cnt, pl) )

