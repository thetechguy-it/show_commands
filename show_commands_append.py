from netmiko import ConnectHandler
import credentials
import os_vendor
import os
from datetime import date, datetime
from ping3 import ping

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
    
backup_folder = "FAN_PSU_Check"
create_folder(backup_folder)

now = datetime.now()
dt_string = now.strftime("%m-%d-%Y") 
dt_string_full = now.strftime("%m-%d-%Y_%H-%M-%S")

print("I'm going to test the ICMP reachability for all the IP Addresses\n\n")
for ip in ip_list:
    print("Testing: " + ip)
    ip_reach = ping(ip)
    if ip_reach == None:
        print("The device with the IP Address: " + ip + " is not reachable. Please verify its status and connectivity\n\n\n")
        with open(ip + "_" + dt_string_full + ".txt", "w") as downdevice:
            downdevice.write("This device is not reachable. Please verify its status and connectivity")
    else:
        SSH = ConnectHandler (ip, device_type = os_vendor.type_ios, username = credentials.username, password = credentials.password, fast_cli = False)
        hostname = SSH.send_command("show switchname")
        print ("It's reachable! I'm processing the device called", hostname, "with the following IP Address:", ip)
        SSH_Check_Connection = SSH.is_alive()
        #print("The SSH connection to the device is:" + str(SSH_Check_Connection)) #Output = True
        txt_file = open(dt_string_full + ".txt", "a")
        txt_file.write("#####" + hostname + "#####" + hostname + "#####" + hostname + "#####" + hostname + "#####" + hostname + "\n")
        for command in commands_list:
            txt_file.write("######## " + command + " ######## \n\n")
            output = (SSH.send_command(command))
            txt_file.write(output + "\n\n")         
        SSH.disconnect()
        SSH_Check_Connection = SSH.is_alive()
        txt_file.write("\n\n\n\n\n\n\n\n ######################################################################################## \n\n\n\n\n\n\n\n")
        #print("The SSH connection to the device is:" + str(SSH_Check_Connection)) #Output = False
        print("\n\n\n")