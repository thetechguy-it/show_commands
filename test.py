from netmiko import ConnectHandler
import os_vendor
import os
from datetime import date, datetime
from ping3 import ping
import getpass

file_ip = open("IPAddressList.txt", "r")
total_ips = file_ip.read()
ip_list = total_ips.splitlines()

file_commands = open("Commands.txt", "r")
total_commands = file_commands.read()
commands_list = total_commands.splitlines()

def create_folder(folder):
    if not os.path.exists(folder):
        os.mkdir(folder)
    os.chdir(folder)

username = input('Enter your username: ')
password = getpass.getpass('Enter your password: ')
    
backup_folder = "CFG_Backup"
create_folder(backup_folder)

now = datetime.now()
dt_string = now.strftime("%m-%d-%Y")
dt_string_full = now.strftime("%m-%d-%Y_%H-%M-%S")

create_folder(dt_string)

print("I'm going to test the ICMP reachability for all the IP Addresses\n\n")

for ip in ip_list:
    print("Testing: " + ip)
    ip_reach = ping(ip)
    print(ip_reach)
    if ip_reach == None:
        print("The device with the IP Address: " + ip + " is not reachable. Please verify its status and connectivity\n\n\n")
        with open(ip + "_" + dt_string_full + ".txt", "w") as downdevice:
            downdevice.write("This device is not reachable. Please verify its status and connectivity")
    else:
        SSH = ConnectHandler (ip, device_type = os_vendor.type_ios, username = username, password = password, fast_cli = False)
        dev_name = SSH.send_command("show run | in hostname")
        dev_name = dev_name.split(" ")
        hostname = dev_name[1]
        print ("It's reachable! I'm processing the device called", hostname, "with the following IP Address:", ip)
        SSH_Check_Connection = SSH.is_alive()
        with open(hostname + "_" + dt_string_full + ".txt", "w") as txt_file:
            print("The file called: " + hostname + ".txt has been created into the " + backup_folder + "/" + dt_string + " folder. You will find here all the outputs. I'm going to close the SSH session")
            for command in commands_list:
                txt_file.write("######## " + command + " ######## \n\n")
                output = (SSH.send_command(command))
                txt_file.write(output + "\n\n\n\n")         
        SSH.disconnect()
        SSH_Check_Connection = SSH.is_alive()
        print("\n\n\n")