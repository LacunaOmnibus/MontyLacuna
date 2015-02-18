

import datetime, hashlib, ntpath, os, re, requests, shutil, sys, zipfile

class Update():
    """ Updates MontyLacuna from github.
    """

    def __init__( self ):
        self.rootdir    = os.path.abspath(os.path.dirname(sys.argv[0])) + "/.."
        self.vardir     = self.rootdir + "/var"
        self.zip_url    = "https://github.com/tmtowtdi/MontyLacuna/archive/master.zip"
        self.zip_path   = os.path.join( self.vardir, self.get_zipfile_name("monty_") )

        self._set_clean_tmpdir()

    def _set_clean_tmpdir( self ):
        """ Creates a "clean" temporary directory under 'root'.

        Arguments:
            - root -- Directory under which the temp directory should be created.

        Returns the path to the created temporary directory.

        A "clean" temporary directory means that, if the temp directory did not 
        already exist, it will be created, empty.  If it did already exist, it and 
        all of its contents will be removed, and then the temp directory will be 
        re-created empty.
        """
        tmpdir = self.rootdir + "/tmp"
        try:
            os.stat( tmpdir )
            shutil.rmtree( tmpdir )
        except:
            pass
        os.mkdir( tmpdir )
        self.tmpdir = tmpdir

    def get_zipfile_name( self, prefix ):
        """ Given a prefix, returns a dated filename string with a .zip extension.

        Arguments
            - prefix -- String.  Nothing is appended to this, so you probably want 
              to include an underscore or other separator.

        >>> print get_zipfile_name( "foo_" );
        foo_20150218170100.zip
        """
        dt = datetime.datetime.today()
        zipfile_name = prefix + datetime.datetime.now().strftime("%Y%m%d%H%M%S") + ".zip"
        return zipfile_name

    def download_and_extract_zipfile( self ):
        """ Downloads a file from a given URL and writes it to the requested path.

        Arguments:
            - URL -- A FQ URL, assumed to point to a .zip file.
            - output_file -- Full path to where you want the downloaded file 
              written.
        """
        resp = requests.get( self.zip_url, stream=True )
        with open(self.zip_path, "wb") as f:
            f.write( resp.content )
        zf = zipfile.ZipFile( self.zip_path )
        zf.extractall( self.tmpdir )

    def get_live_path( self, path ):
        """ Given a path to a file, which is assumed to be living under a temporary 
        directory named 'tmp', returns the path where the file needs to end up.

        Arguments:
            - path -- the current temporary directory path.

        This is a bit fragile.  You CANNOT go changing the name of your temporary 
        directory and expect this to work.  It must be named 'tmp'.
        """
        pat = re.compile( '/tmp/MontyLacuna-master' )
        return pat.sub( "", path )

    def hash_file( self, filepath ):
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

    def consuela( self ):
        """ Clean up after ourselves.

        Removes both the temporary directory, including its contents, and the 
        downloaded .zip file.

        Needs more lemon pledge.
        """
        shutil.rmtree( self.tmpdir )
        os.remove( self.zip_path )

    def copy_new_file( self, file_path, new_path ):
        """ Copy a file to a new path, maintaining the original filename.

        Arguments
            - file_path -- Full path to the file to copy
            - new_path -- Path into which the file should be copied.  
              MUST NOT END WITH A SLASH.
        """
        filename = ntpath.basename(file_path)
        new_path = os.path.join(new_path, filename)
        shutil.copyfile( file_path, new_path )

    def copy_mismatched_file( self, tmp_path, name ):
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
        live_path   = self.get_live_path( tmp_path )
        tmp_file    = os.path.join( tmp_path, name )
        live_file   = os.path.join( live_path, name )
        if( os.path.isfile(live_file) ):
            tmp_hash    = self.hash_file( tmp_file )
            live_hash   = self.hash_file( live_file )
            if( tmp_hash != live_hash ):
                print( "\t'{}' hashes don't match - copying.".format(name) )
                self.copy_new_file( tmp_file, live_path)
        else:
            print( "\t'{}' is a new file, and does not exist in our current live path.".format(name) )
            self.copy_new_file( tmp_file, live_path)

