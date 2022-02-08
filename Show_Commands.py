# With this script you will launch the commands inside the file called 'Commands.txt' to all the devices inside the file called 'IPAddressList.txt


import paramiko
import netmiko
from netmiko import ConnectHandler
from contextlib import redirect_stdout
import credentials
import type
import socket
from pathlib import Path
import shutil


total_ips = open("IPAddressList.txt")
ips = total_ips.readlines()
total_commands = open("Commands.txt")
commands = total_commands.readlines()
print("With this script you will launch the commands inside the file called 'Commands.txt' to all the devices inside the file called 'IPAddressList.txt")
for ip in ips:
    SSH = ConnectHandler (ip, device_type = type.type_ios, username = credentials.username, password = credentials.password)
    dev_name = SSH.send_command("show run | in hostname")
    dev_name = dev_name.split(" ")
    hostname = dev_name[1]
    print ("I'm processing the device called ", hostname, "with the following IP Address:", ip)
    SSH_Check_Connection = SSH.is_alive()
    print("The connection to the device is:" + str(SSH_Check_Connection))
    with open(hostname + ".txt", "w") as txt_file:
        print("I created I file called: ", hostname,". You will find here all the outputs")
        with redirect_stdout(txt_file):
            for command in commands:
                print("***", command, "***")
                output = (SSH.send_command(command))
                print (output, "\n\n")         
    SSH.disconnect()
    SSH_Check_Connection = SSH.is_alive()
    print("The connection to the device is:" + str(SSH_Check_Connection))
    print("\n\n\n")
