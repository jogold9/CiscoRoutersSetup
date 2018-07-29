#Script to loop through a array of Cisco router IP addresses, telnet into those routers, and do some initial config
#Josh Gold

import getpass
import telnetlib

HOSTS = ['10.1.1.2', '10.2.1.2', '10.3.0.2', '10.5.0.5']
AAA_SERVER = "IP address of RADIUS or TACACS+ server goes here"
user = input("Username: ")
password = getpass.getpass()
enable_password = getpass.getpass()

def setup_router():
    telnet = telnetlib.Telnet(HOSTS)
    telnet.read_until(b"Username: ")
    telnet.write(user.encode('ascii') + b"\n")
    if password:
       telnet.read_until(b"Password: ")
       telnet.write(password.encode('ascii') + b"\n")

    telnet.write(b"enable\n")
    telnet.write(enable_password.encode('ascii') + b"\n")

    #Enter global configuration mode
    telnet.write(b"configure terminal\n")

    #Prevent long delay if you mistype a command and IOS thinks you want a domain lookup
    telnet.write(b"no ip domain-lookup\n")

    #Prevent console output from interrupting your typing
    telnet.write(b"logging synchronous\n")

    #Prevent console timeout
    telnet.write(b"no exec-timeout\n")

    #Set a banner message
    telnet.write(b"banner motd & ***Warning***  Authorized persons only &\n")

    #Set up TACACs+ or RADIUS server for authentication
    telnet.write(b"aaa new-model\n")
    telnet.write(b"radius-server host AAA_SERVER\n")
    #telnet.write(b"tacacs-server host AAA_SERVER\n")

    #Get out of global configuration mode
    telnet.write(b"end\n")

    #Save running configuration
    telnet.write(b"copy running-config startup-config\n")
    #Enter to confirm saving
    telnet.write(b"\n")

    telnet.write(b"exit\n")

    print(telnet.read_all().decode('ascii'))

#**********************

for item in HOSTS:
    setup_router()

print ("Script completed")
