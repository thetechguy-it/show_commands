# With this script you will launch the commands inside the file called 'Commands.txt' to all the devices inside the file called 'IPAddressList.txt

from netmiko import ConnectHandler
from contextlib import redirect_stdout
import credentials
import type
import os

total_ips = open("IPAddressList.txt", "r") # Create a file called "IPAddressList.txt" and put one IP addresses in each line
ips = total_ips.readlines()
total_commands = open("Commands.txt", "r") # Create a file called "Commands.txt" and put one CLI commans in each line
commands = total_commands.readlines()

print("With this script you will launch the commands inside the file called 'Commands.txt' to all the devices inside the file called 'IPAddressList.txt")
os.mkdir("CFG Backup")
# Put your own folder
os.chdir("") 

for ip in ips:
    SSH = ConnectHandler (ip, device_type = type.type_ios, username = credentials.username, password = credentials.password, fast_cli = False)
    dev_name = SSH.send_command("show run | in hostname")
    dev_name = dev_name.split(" ")
    hostname = dev_name[1]
    print ("I'm processing the device called ", hostname, "with the following IP Address:", ip)
    SSH_Check_Connection = SSH.is_alive()
    print("The connection to the device is:" + str(SSH_Check_Connection))
    with open(hostname + ".txt", "w") as txt_file:
        print("The file called: " + hostname +".txt has been created into the 'CFG Backup' folder. You will find here all the outputs")
        for command in commands:
            txt_file.write("This is the output for the following command:" + command)
            output = (SSH.send_command(command))
            txt_file.write(output + "\n\n")         
    SSH.disconnect()
    SSH_Check_Connection = SSH.is_alive()
    print("The connection to the device is:" + str(SSH_Check_Connection))
    print("\n\n\n")
total_ips.close()
total_commands.close()
