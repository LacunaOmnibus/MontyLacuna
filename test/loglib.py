
import logging, logging.handlers

def make_logger( file ):

    l = logging.getLogger( 'testlog' )
    l.setLevel(logging.DEBUG)

    max_log_size    = 300
    log_format      = '[%(asctime)s] (MODULE) (%(levelname)s) - %(message)s'
    date_format     = '%Y-%m-%d %H:%M:%S'

    sh = logging.StreamHandler()
    sh.setLevel(logging.WARNING)
    sh.setFormatter(logging.Formatter(log_format, date_format))
    l.addHandler(sh)

    lf = logging.handlers.RotatingFileHandler( 
        file, 
        maxBytes = max_log_size, 
        backupCount = 3
    )
    lf.setLevel(logging.DEBUG)
    lf.setFormatter(logging.Formatter(log_format, date_format))
    l.addHandler(lf)
    return l


