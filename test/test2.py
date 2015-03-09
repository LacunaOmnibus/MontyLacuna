
import loglib, time

f       = 'out.log'
mystr   = 'b'*30

l = loglib.make_logger(f)
l.info( mystr )
l.info( mystr )
l.info( mystr )
