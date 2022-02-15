# With this script you will launch the commands inside the file called 'Commands.txt' to all the devices inside the file called 'IPAddressList.txt

from typing import Type
from netmiko import ConnectHandler
import credentials
import os_vendor
import os
from datetime import date, datetime
from ping3 import ping

total_ips = open("IPAddressList.txt", "r")
ip_list_temp = total_ips.readlines()

# The created list has "\n" in each string. I'll create a new empty list in order to fill it with just the IPs without the "\n"
# ['10.155.233.205\n', '10.155.233.201\n', '10.155.233.202\n', '10.155.233.203\n', '10.155.233.204\n', '10.155.233.206']
ip_list = []
for ips in ip_list_temp:
    temp_list = ips.split("\n")
    ip_list.append(temp_list[0])

#The list called "ip_list" is a list with only the IP addresses
# ['10.155.233.205', '10.155.233.201', '10.155.233.202', '10.155.233.203', '10.155.233.204', '10.155.233.206']

total_commands = open("Commands.txt", "r")
commands = total_commands.readlines()

print("With this script you will launch the commands inside the file called 'Commands.txt' to all the devices inside the file called 'IPAddressList.txt\n\n\n")

# Checks if the backup folder exists, if not, it creates it. Put the name 
backup_folder = "CFG_Backup"
if not os.path.exists(backup_folder):
    os.mkdir(backup_folder)
os.chdir(backup_folder)

# Current time and formats it as: Month, Day, Year, Hour and Minute.
now = datetime.now()
dt_string_full = now.strftime("%m-%d-%Y_%H-%M")
dt_string = now.strftime("%m-%d-%Y")

# Checks if the daily folder exists, if not, it creates it.
if not os.path.exists(dt_string):
    os.mkdir(dt_string)
os.chdir(dt_string)
print("I'm going to test the ICMP reachability for all the IP Addresses\n\n")

for ip in ip_list:
    print("Testing: " + ip)
    ip_reach = ping(ip)
    if ip_reach == None:
        print("The device with the IP Address: " + ip + " is not reachable.\n\n\n")
        with open(ip + "_" + dt_string_full + ".txt", "w") as downdevice:
            downdevice.write("This device is not reachable, please fix the issue")
    else:
        print("The device with the IP Address: " + ip + " is reachable. I'm going to connect via SSH\n")
        SSH = ConnectHandler (ip, device_type = os_vendor.type_ios, username = credentials.username, password = credentials.password, fast_cli = False)
        dev_name = SSH.send_command("show run | in hostname")
        dev_name = dev_name.split(" ")
        hostname = dev_name[1]
        print ("I'm processing the device called ", hostname, "with the following IP Address:", ip)
        SSH_Check_Connection = SSH.is_alive()
        print("The connection to the device is:" + str(SSH_Check_Connection))
        with open(hostname + "_" + dt_string_full + ".txt", "w") as txt_file:
            print("The file called: " + hostname + ".txt has been created into the " + backup_folder + " folder. You will find here all the outputs")
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