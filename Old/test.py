from ping3 import ping
from datetime import date, datetime

now = datetime.now()
dt_string_full = now.strftime("%m-%d-%Y_%H-%M")
dt_string = now.strftime("%m-%d-%Y")

ip = "10.155.233.205"
ip_reach = ping(ip)
print(ip_reach)
if ip_reach == None:
        print("The device with the IP Address: " + ip + " is not reachable.")
        with open(ip + "_" + dt_string_full + ".txt", "w") as downdevice:
            downdevice.write("This device is not reachable, please fix the issue")
else:
    print("It is reachable")
    
ip1 = "10.155.233.201"
ip_reach = ping(ip1)
print(ip_reach)
if ip_reach == None:
        print("The device with the IP Address: " + ip1 + " is not reachable.")
        with open(ip1 + "_" + dt_string_full + ".txt", "w") as downdevice:
            downdevice.write("This device is not reachable, please fix the issue")
else:
    print(ip1 + " is reachable")