#!/usr/bin/python3

import configparser, getpass, os, re, sys
bindir = os.path.abspath(os.path.dirname(sys.argv[0]))
libdir = bindir + "/../lib"
sys.path.append(libdir)

import lacuna

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

clear_screen()
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
clear_screen()

emp_name = input("What is your empire's name? ")
passwords_do_not_match = True
cnt = 0
while passwords_do_not_match:
    if cnt:
        print( "BZZZT!  Passwords do not match.  Try again." )
        print(  )
    real_pw1    = getpass.getpass("What is your real password? ")
    real_pw2    = getpass.getpass("Confirm: ")
    sitter_pw1  = getpass.getpass("What is your sitter password? (leave blank if you don't have one) ")
    sitter_pw2  = ""
    if sitter_pw1:
        sitter_pw2  = getpass.getpass("Confirm: ")
    if real_pw1 == real_pw2 and sitter_pw1 == sitter_pw2:
        passwords_do_not_match = False
    cnt += 1
clear_screen()

if not sitter_pw1:
    sitter_pw1 = "YOU'LL NEED TO MAKE A SITTER AND ENTER IT HERE BEFORE YOU CAN USE THIS SECTION."


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
    'password': real_pw1,
}
cp['sitter'] = {
    'username': emp_name,
    'password': sitter_pw1,
}
cp['play_test'] = {
    'host': 'pt.lacunaexpanse.com',
    'username': emp_name,
    'password': sitter_pw1,
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

