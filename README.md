## CODE MISSION
With this code I want to help all the engineers who have to backup configurations, store or retrieve data from multiple devices into a single or multiple devices-named files. Thanks to this code you'll be able to push a defined list of commands to a static or dynamic list of IP addresses.     

There are two versions:    
- **Static**: The code will use the list of the IP Addresses defined inside the file called "IPAddressList.txt". Please put one IP per line.      
- **Dynamic**: The code will ask you which network you want to scan and he creates a list with all the reachable devices (via ICMP) in the provided network.       

Each version has two different ways to store the data:
- **Create**: The code will create one file for each device     
- **Append**: The code will create a single file with all the outputs     

It's up to you!


**Static code list of operations**:
- Open the file called "IPAddressList.txt" and store it in a list
- Open the file called "Commands.txt" and store it in a list
- Verify if the devices in the IPAddressList are reachable via ICMP
- SSH connection to each IP
- Push commands (stored in the Commands list)
- Store outputs in dedicated files (create version) o unique file (append version)

**Dynamic code list of operations**:
- Scan a network provided by the user (via ICMP, it's automatic)
- Store the reachable IP in a list
- SSH connection to each IP. If it's not a Cisco device skip it.
- Push commands (stored in the Commands list)
- Store outputs in dedicated files (create version) o unique file (append version)

## MODULES
Install the following modules:

> pip3 install netmiko       
> pip3 install ping3         
> pip3 install networkscan       

## USERNAME/PASSWORD
The code does not have any pre-defined username/password. When you run the code it will ask you the username and password for the devices.     

## CISCO VERSION
Tested and working with:
- IOS XE
- NX-OS
- IOS

## RUN THE CODE
Create a virtual environment in order to test the code:     

> python3 -m venv TEST        
> source TEST/bin/activate         
> cd TEST/            
> git clone https://github.com/thetechguy-it/show_commands.git         
> cd show_commands/         
> pip3 install netmiko         
> pip3 install ping3        
> pip3 install networkscan          
> sudo python3 < scriptname >.py         

The code will create a folder called "BACKUP" and then another folder with the date. Inside this second folder, you will find all your files.

Example:
![example1](https://github.com/thetechguy-it/show_commands/blob/main/example1.png)