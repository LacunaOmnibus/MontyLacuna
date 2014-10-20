
import os, sys
bindir = os.path.abspath(os.path.dirname(__file__))
libdir = bindir + "/../lib"
sys.path.append(libdir)
import lacuna as lac

filepath = 'etc/lacuna.cfg'
if os.path.isfile(filepath):
    print("")
    print("A file already exists at {} - I'm not going to overwrite it.".format(filepath) )
    print("If you're sure you want to re-run this, delete that file yourself first.")
    print("")
    quit()

guest = lac.clients.Guest()
guest.write_default_config_file(filepath)
print("")
print("Done - default config file lives in", filepath)
print("It's still not quite ready - you need to add at least one section containing your")
print("empire name and password.  For help, see the wiki:")
print("    https://github.com/tmtowtdi/MontyLacuna/wiki/Config-File")
print("")

