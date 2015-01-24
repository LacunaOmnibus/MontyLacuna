#!/usr/bin/python3

import configparser, os, re, sys
bindir = os.path.abspath(os.path.dirname(sys.argv[0]))
libdir = bindir + "/../lib"
sys.path.append(libdir)

import lacuna

os.system('cls' if os.name == 'nt' else 'clear')
filepath = 'etc/lacuna.cfg'
if os.path.isfile(filepath):
    print("")
    print("A file already exists at ", filepath )
    print("IF YOU CONTINUE, THAT FILE WILL BE OVERWRITTEN!" )
    print("")
    yn = input("Do you want to continue?  [y/N]: ")
    if not re.match('^y', yn):
        print("If you're sure you want to re-run this, delete that file yourself first.")
        print("")
        quit()
os.system('cls' if os.name == 'nt' else 'clear')


emp_name    = input("What is your empire's name? ")
real_pw     = input("What is your real password? ")
sitter_pw   = input("What is your sitter password? (leave blank if you don't have one) ")

if not sitter_pw:
    sitter_pw = "YOU'LL NEED TO MAKE A SITTER AND ENTER IT HERE BEFORE YOU CAN USE THIS SECTION."

cp = configparser.ConfigParser()
cp['DEFAULT'] = {
    'host': 'us1.lacunaexpanse.com',
    'proto': 'http',
    'api_key': 'anonymous',
    'sleep_on_call': 1,
    'sleep_after_error': 1,
    'warn_on_sleep': 1,
    'show_captcha': 1,
    'logfile': 'us1.log',
}
cp['real'] = {
    'username': emp_name,
    'password': real_pw,
}
cp['sitter'] = {
    'username': emp_name,
    'password': sitter_pw,
}
cp['play_test'] = {
    'host': 'pt.lacunaexpanse.com',
    'username': emp_name,
    'password': sitter_pw,
    'logfile': 'pt.log',
}
with open(filepath, 'w') as handle:
    cp.write(handle)


print("")
print("Done - the new config file lives in", filepath)
print("")
print("You can manually update that file to change empire name, passwords, or even add")
print("new sections.  For help, see the wiki:")
print("    http://tmtowtdi.github.io/MontyLacuna/html_docs/config_file.html")
print("")


