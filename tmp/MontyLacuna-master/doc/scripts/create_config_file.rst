
Create Config File
==================

Creates a fresh new config file in ``ROOT/etc/lacuna.cfg``.  This script 
doesn't require any configuration at all, you can just run it as-is.  It will 
prompt you to answer a few questions, and then create your basic config file.

    >>> python bin/create_config_file.py

If you've already got a config file in the default location, running this will 
notice that and ask if you want to overwrite that file.  If that happens, you 
should answer "no" unless you're really really sure you really want to 
overwrite that file (really).  After answering "no", go back up or rename your 
existing config file, then just come back and run this again.

