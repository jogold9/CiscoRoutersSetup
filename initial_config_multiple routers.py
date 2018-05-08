#Script to loop through a array of Cisco router IP addresses, telnet into those routers, and do some initial config
#Josh Gold

import getpass
import telnetlib

HOSTS = ['1st_router_IP', '2nd_router_IP', '3rd router_IP', '4th_router_IP']
AAA_SERVER = "IP address of RADIUS or TACACS+ server goes here (for usernames and passwords / authentication)"
user = input("Username: ")
password = getpass.getpass()
enable_password = getpass.getpass()

for item in HOSTS:
    setup_router()

print "Script completed"

# End of script

def setup_router():
    tn = telnetlib.Telnet(HOST)

    tn.read_until(b"Username: ")
    tn.write(user.encode('ascii') + b"\n")
    if password:
    tn.read_until(b"Password: ")
    tn.write(password.encode('ascii') + b"\n")

    tn.write(b"enable\n")
    tn.write(enable_password.encode('ascii') + b\n")

    #Enter global configuration mode
    tn.write(b"configure terminal\n")

    #Prevent long delay if you mistype a command and IOS thinks you want a domain lookup
    tn.write(b"no ip domain-lookup\n")

    #Prevent console output from interrupting your typing
    tn.write(b"logging synchronous\n")

    #Prevent console timeout
    tn.write(b"no exec-timeout\n")

    #Set a banner message
    tn.write(b"banner motd & ***Warning***  Authorized persons only &\n")

    #Set up TACACs+ or RADIUS
    tn.write(b"aaa new-model\n")
    tn.write(b"radius-server host AAA_SERVER\n")
    #tn.write(b"tacacs-server host AAA_SERVER\n")

    #Get out of global configuration mode
    tn.write(b"end\n")

    #Save running configuration
    tn.write(b"copy running-config startup-config\n")
    #Enter to confirm saving
    tn.write(b"\n")

    tn.write(b"exit\n")

    print(tn.read_all().decode('ascii')