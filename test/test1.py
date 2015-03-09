
import loglib, time

f       = 'out.log'
mystr   = 'a'*10

l = loglib.make_logger(f)
l.info( mystr )
time.sleep(5)
l.info( mystr )
