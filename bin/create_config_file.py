#!/usr/bin/python3

import configparser, getpass, os, re, sys
bindir = os.path.abspath(os.path.dirname(sys.argv[0]))
libdir = bindir + "/../lib"
sys.path.append(libdir)

import lacuna
import lacuna.exceptions as err


def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def check_for_existing_config( file ):
    if os.path.isfile(file):
        print("")
        print("A file already exists at ", file )
        print("IF YOU CONTINUE, THAT FILE WILL BE OVERWRITTEN!" )
        print("")
        yn = input("Do you want to continue?  [y/N]: ")
        if not re.match('^y', yn):
            print("If you're sure you want to re-run this, delete that file yourself first.")
            print("")
            quit()
        clear_screen()

def get_creds( file ):
    emp_name = input("What is your empire's name? ")
    cnt = 0
    print( "" )
    print( "I'm going to ask you to enter your password below.  When you type your ")
    print( "password, it will not be echoed to the screen -- you won't see anything." )
    print( "That's OK, just look at your keyboard and keep typing." )
    print( "" )

    real_pw1    = getpass.getpass("What is your real password? ")
    sitter_pw1  = getpass.getpass("What is your sitter password? ")

    if not real_pw1:
        print( "You must enter a password.  I'm guessing you're not sure what yours is right " )
        print( "now, so I'm going to quit." )
        print( "Go ahead and run this again later after you've found both your real and " )
        print( "sitter passwords." )
        quit()

    if not sitter_pw1:
        sitter_pw1 = "YOU'LL NEED TO MAKE A SITTER AND ENTER IT HERE BEFORE YOU CAN USE THIS SECTION."
        print( '' )
        print( '*****' )
        print( "You did not enter a sitter password, but most MontyLacuna scripts connect using" )
        print( "the sitter by default.  If you don't have a sitter yet, you're strongly encouraged" )
        print( "to create one in-game, and then edit '{}' to add your sitter.".format(file) )
        print( '*****' )
        print( '' )

    return (emp_name, real_pw1, sitter_pw1)

def get_creds_orig( file ):
    ### This version prompts the user to enter each password twice, which is 
    ### tedious and fraught.  Since we're now testing the user-entered 
    ### passwords by logging in with them, we really don't need this anymore.
    emp_name = input("What is your empire's name? ")
    passwords_do_not_match = True
    cnt = 0
    print( "" )
    print( "I'm going to ask you to enter your password below.  When you type your ")
    print( "password, it will not be echoed to the screen -- you won't see anything." )
    print( "That's OK, just look at your keyboard and keep typing." )
    print( "" )
    while passwords_do_not_match:
        if cnt:
            print( "BZZZT!  Passwords do not match.  Try again." )
            print(  )
        real_pw1    = getpass.getpass("What is your real password? ")
        real_pw2    = getpass.getpass("Confirm: ")
        print( "" )
        sitter_pw1  = getpass.getpass("What is your sitter password? (leave blank if you don't have one) ")
        sitter_pw2  = ""
        if sitter_pw1:
            sitter_pw2  = getpass.getpass("Confirm: ")
        if real_pw1 == real_pw2 and sitter_pw1 == sitter_pw2:
            passwords_do_not_match = False
        cnt += 1
    if not sitter_pw1:
        sitter_pw1 = "YOU'LL NEED TO MAKE A SITTER AND ENTER IT HERE BEFORE YOU CAN USE THIS SECTION."
        print( '' )
        print( '*****' )
        print( "You did not enter a sitter password, but most MontyLacuna scripts connect using" )
        print( "the sitter by default.  If you don't have a sitter yet, you're strongly encouraged" )
        print( "to create one in-game, and then edit '{}' to add your sitter.".format(file) )
        print( '*****' )
        print( '' )
    return (emp_name, real_pw1, sitter_pw1)

def write_config( file, emp, realpw, sitterpw ):
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
        'username': emp,
        'password': realpw,
    }
    cp['sitter'] = {
        'username': emp,
        'password': sitterpw,
    }
    cp['play_test'] = {
        'host': 'pt.lacunaexpanse.com',
        'username': emp,
        'password': sitterpw,
        'logfile': 'pt.log',
    }
    with open(file, 'w') as handle:
        cp.write(handle)

def test_section( file, section ):
    try:
        client = lacuna.clients.Member(
            config_file = file,
            config_section = section,
        )
    except (err.ServerError, lacuna.exceptions.BadCredentialsError) as e:
        return False 
    return client




filepath = 'etc/lacuna.cfg'

clear_screen()
check_for_existing_config( filepath )
emp_name, real_pw, sitter_pw = get_creds(filepath)
write_config( filepath, emp_name, real_pw, sitter_pw )

print( "" )
print( "Testing your passwords, please wait a few seconds..." )
emp_id = 0
bad_pw = 0
for section in ('real', 'sitter'):
    client = test_section( filepath, section )
    if client:
        emp_id = client.empire.id
    else:
        bad_pw = 1
        print( "The {} password you entered is INCORRECT!".format(section) )
        print( "You can update that password by editing {}, or by simply running this ".format(filepath) )
        print( "script again and entering the correct password this time." )
if not bad_pw:
    print( "...Yay!  Your passwords check out!" )

print("")
print( '*****' )
print("Done - the new config file lives in", filepath)
print("")
print("You can manually update that file to change empire name, passwords, or even add")
print("new sections.  For help, see the wiki:")
print("    http://tmtowtdi.github.io/MontyLacuna/html_docs/config_file.html")

if emp_id:
    print( "" )
    print( "Your empire ID is {0}.  If you like, you can log in to the game using '#{0}' as your ".format(emp_id) )
    print( "empire name instead of '{}'.  If you ever change your empire name, your ID will stay ".format(emp_name) )
    print( "the same, so logging in with ID rather than empire name might be convenient.  " )
    print( "" )
    print( "If you want to do this, edit the config file ({}) and just change all ".format(filepath) )
    print( "instances of '{}' to '#{}' and you'll be set.".format(emp_name, emp_id) )

print( '*****' )
print("")

