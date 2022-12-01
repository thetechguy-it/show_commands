from netmiko import ConnectHandler
import os_vendor
import os
from datetime import date, datetime
from ping3 import ping
import getpass
import networkscan

def create_folder(folder):
    if not os.path.exists(folder):
        os.mkdir(folder)
    os.chdir(folder)

# Login to the devices 
def device_login(host, username, password):
    cisco_ios = {
        'device_type': 'cisco_ios',
        'host': host,
        'username': username,
        'password': password,
    }
    try:
        connection = ConnectHandler(**cisco_ios)
        connection.enable()
        device_hostname(connection) 
    except Exception as err:
        print(f"Oops! {err}\n")

# Retrieve the device Hostname
def device_hostname(SSH):
    output = SSH.send_command("show run")
    dev_name = SSH.send_command("show run | in hostname")
    dev_name = dev_name.split(" ")
    hostname = dev_name[1]
    print("The device name is: ", hostname)
    device_commands(hostname, SSH) 

# Push the commands stored into the "Commands.txt" file and store the output in an unique file called with the actual date
def device_commands(device_name, device_SSH):
    txt_file = open(dt_string_full + ".txt", "a")
    txt_file.write("#####" + device_name + "#####" + device_name + "#####" + device_name + "#####" + device_name + "#####" + device_name + "\n")
    for command in commands_list:
        txt_file.write("######## " + command + " ######## \n\n")
        output = (device_SSH.send_command(command))
        txt_file.write(output + "\n\n")         
    device_SSH.disconnect()
    SSH_Check_Connection = device_SSH.is_alive()
    txt_file.write("\n\n\n\n\n\n\n\n ######################################################################################## \n\n\n\n\n\n\n\n")
    print("\n\n\n")

# Verify if an IP address is reachable.
# If YES: run "device_login" function
# If NO: Create a file called with the IP Address of the device and write inside "This device is not reachable. Please verify its status and connectivity"
def ip_reachability(ip_list):
    for ip in ip_list:
        print("Testing: " + ip)
        ip_reach = ping(ip)
        if ip_reach == None:
            print("The device with the IP Address: " + ip + " is not reachable. Please verify its status and connectivity\n\n\n")
            with open(ip + "_" + dt_string_full + ".txt", "w") as downdevice:
                downdevice.write("This device is not reachable. Please verify its status and connectivity")
        else:
            print ("It's reachable! I'm going to retrieve data from it.")
            device_login(ip, username, password)

def discover_network():
    network_mask = input("Enter the management network (x.x.x.x/y): ")
    my_scan = networkscan.Networkscan(network_mask)
    my_scan.run()
    reachable_ip = []
    print("List of reachable devices:\n" )
    for i in my_scan.list_of_hosts_found:
        print(i)
        reachable_ip.append(i)
    ip_reachability(reachable_ip)

# User enters device credentials 
username = input('Enter your username: ')
password = getpass.getpass('Enter your password: ')

# Code opens the file where commands are stored (1 per line)
file_commands = open("Commands.txt", "r")
total_commands = file_commands.read()
commands_list = total_commands.splitlines()

# Create Backup Folder
backup_folder = "BACKUP"
create_folder(backup_folder)

# Create daily folder inside Backup Folder
now = datetime.now()
dt_string = now.strftime("%m-%d-%Y")
dt_string_full = now.strftime("%m-%d-%Y_%H-%M-%S")
create_folder(dt_string)

# Code
discover_network()