# With this script you will launch the commands inside the file called 'Commands.txt' to all the devices inside the file called 'IPAddressList.txt

from netmiko import ConnectHandler
import credentials
import os_vendor
import os
from datetime import date, datetime

total_ips = open("IPAddressList.txt", "r")
ips = total_ips.readlines()
total_commands = open("Commands.txt", "r")
commands = total_commands.readlines()

print("With this script you will launch the commands inside the file called 'Commands.txt' to all the devices inside the file called 'IPAddressList.txt")

# Checks if the backup folder exists, if not, it creates it.
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

for ip in ips:
    SSH = ConnectHandler (ip, device_type = os_vendor.type_ios, username = credentials.username, password = credentials.password, fast_cli = False)
    dev_name = SSH.send_command("show run | in hostname")
    dev_name = dev_name.split(" ")
    hostname = dev_name[1]
    print ("I'm processing the device called ", hostname, "with the following IP Address:", ip)
    SSH_Check_Connection = SSH.is_alive()
    print("The connection to the device is:" + str(SSH_Check_Connection))
    with open(hostname + "_" + dt_string_full + ".txt", "w") as txt_file:
        print("The file called: " + hostname + ".txt has been created into the " + backup_folder + "folder. You will find here all the outputs")
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