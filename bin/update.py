#!/usr/bin/python3

import datetime, hashlib, os, re, requests, shutil, sys, zipfile

bindir  = os.path.abspath(os.path.dirname(sys.argv[0]))
rootdir = bindir + "/.."
vardir  = rootdir + "/var"



def get_zipfile_name():
    dt = datetime.datetime.today()
    zipfile_name = "monty_" + str(dt.year) + str(dt.month) + str(dt.day) + str(dt.hour) + str(dt.minute) + str(dt.second) + ".zip"
    return zipfile_name

def download_zipfile( url, output_file ):
    resp = requests.get( url, stream=True )
    with open(output_file, "wb") as f:
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

def hash_file( filepath ):
    """ Returns the hash digest of a file as a string.

    Arguments:
        - filepath -- full path to a file to hash

    SHA1 may or may not be faster/slower than MD5.  Either way, the difference 
    in speed is negligible.
    """
    h = hashlib.sha1()
    with open(filepath,'rb') as file:
        chunk = 0
        while chunk != b'':
            chunk = file.read(1024)
            h.update(chunk)
    return h.hexdigest()

def copy_new_file( file, new_path ):
    """ Copy a file to a new path, maintaining the original filename.

    Arguments
        - file -- Full path to the file to copy
        - new_path -- Path into which the file should be copied.  
          MUST NOT END WITH A SLASH.
    """
    new_path += '/'
    shutil.copyfile( file, new_path )

def copy_mismatched_file( tmp_path, name ):
    """ Copies an existing file to our "live file path" if that file is either 
    completely new (it doesn't already exist in our "live file path"), or if 
    the file in question does not exactly match the file in our "live file 
    path".

    Arguments:
        - tmp_path -- The path where the file in question currently lives.
          MUST NOT END WITH A SLASH.
        - name -- The name of the file in question.

    The "live file path" is determined by get_live_path().
    """
    print( tmp_path )
    exit()
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
zip_path    = os.path.join( vardir, get_zipfile_name() )
download_zipfile( zip_url, zip_path )

member  = "MontyLacuna-master"
zf      = zipfile.ZipFile( zip_path )

tmpdir = get_clean_tmpdir( rootdir )
zf.extractall( tmpdir )

### at this point, we have ROOT/tmp/MontyLacuna-master/

cnt = 0
for tmp_path, dirs, files in os.walk( os.path.join(tmpdir, "MontyLacuna-master") ):
    cnt += 1
    if cnt > 3:
        continue
    for name in files:
        copy_mismatched_file( tmp_path, name )

### Fully remove the tmp directory and the downloaded zip file
shutil.rmtree( tmpdir )
os.remove( zip_path )

