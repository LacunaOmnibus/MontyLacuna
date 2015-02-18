#!/usr/bin/python3

import datetime, hashlib, os, re, requests, shutil, sys, zipfile

bindir  = os.path.abspath(os.path.dirname(sys.argv[0]))
rootdir = bindir + "/.."
vardir  = rootdir + "/var"



def get_zipfile_name():
    dt = datetime.datetime.today()
    zipfile_name = "monty_" + str(dt.year) + str(dt.month) + str(dt.day) + str(dt.hour) + str(dt.minute) + str(dt.second) + ".zip"
    return zipfile_name

def download_zipfile( url, output ):
    resp = requests.get( url, stream=True )
    with open(outfile, "wb") as f:
        f.write( resp.content )

def get_clean_tmpdir( root ):
    tmpdir = root + "/tmp"
    try:
        os.stat( tmpdir )
        shutil.rmtree( tmpdir )
    except:
        pass
    os.mkdir( tmpdir )
    return tmpdir

def get_live_path( path ):
    pat = re.compile( '/tmp/MontyLacuna-master' )
    return pat.sub( "", path )

def hash_file( filename ):
    #h = hashlib.sha1()
    h = hashlib.md5()
    with open(filename,'rb') as file:
        chunk = 0
        while chunk != b'':
            chunk = file.read(1024)
            h.update(chunk)
    return h.hexdigest()

def copy_new_file( new_file, live_path ):
    live_path += '/'
    shutil.copyfile( new_file, live_path )

def copy_mismatched_files( tmp_path, name ):
    live_path   = get_live_path( tmp_path )
    tmp_file    = os.path.join( tmp_path, name )
    live_file   = os.path.join( live_path, name )
    if( os.path.isfile(live_file) ):
        tmp_hash    = hash_file( tmp_file )
        live_hash   = hash_file( live_file )
        if( tmp_hash != live_hash ):
            print( "'{}' hashes don't match - copying.".format(name) )
            copy_new_file( tmp_file, live_path)
    else:
        print( "'{}' is a new file, and does not exist in our current live path.".format(name) )
        copy_new_file( tmp_file, live_path)


zip_url     = "https://github.com/tmtowtdi/MontyLacuna/archive/master.zip"
zip_path    = vardir + get_zipfile_name();
download_zipfile( zip_url, zip_path )

member  = "MontyLacuna-master"
zf      = zipfile.ZipFile( zip_path )

tmpdir = get_clean_tmpdir( rootdir )
zf.extractall( tmpdir )

### at this point, we have ROOT/tmp/MontyLacuna-master/

cnt = 0
for tmp_path, dirs, files in os.walk( tmpdir + "/MontyLacuna-master" ):
    cnt += 1
    if cnt > 3:
        exit()
    for name in files:
        copy_mismatched_files( tmp_path, name )

