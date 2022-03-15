# TOR IP Blocking List to ASA network object to block

The goal of these 2 scripts is to provide with a proof of concept of a ASA firewall update automation from the TOR entry/exit IP addresses list.

2 scripts will run independently

- 1-get_tor_ip_list.py 
- 2-asa_send_cli.py

The **1-get_tor_ip_list.py** script is a loop that runs infinitely and which download every hours the TOR IP entry/exit IP addresses list and generates a text files named **asa_cli.txt** that is a list of ASA CLI commands to be sent to a Cisco ASA.

The generated ASA CLI command file contains cli commands that update a network object-group with new IP addresses to add and IP addresses to remove. At every list update this script keeps in the text file named **current_firewall_blocking_list.py** the last TOR IP List.

This script generates as well a log file **.log.txt** that keeps an history of executed operations.

The second script **2-asa_send_cli.py** runs separatly and can be run at anytime. It is logical to run it just after the first one.

This script reads first the file named **asa_devices_list.yml** which contains a list of ASA devices to update.

For every ASA device in the list we have the ASA administration IP address, username and password and the name of the cli command file that contains the list of commands to be sent to the ASA.

usernames and password are in clear text in this example. THIS IS GOOD FOR TESTING BUT CHANGE THIS OF COURSE FOR PRODUCTION!!. Have a look to **vault** for protecting credentials.

the **asa_cli.txt** file must contain every cli commands to send to the ASA exactly as you would send them with a Putty terminal. And this file will be created for you by the first script.

This second script uses **netmiko** to SSH to ASAs.

There is another way to send cli commands to an ASA : ASA HTTPS APIs.  Have a look to : https://github.com/pcardotatgit/ASA_HTTPS_API_Example 


## Installation

- Create a working directory, into your python machine that will host the scripts
- Open a console window and change directory to your working directory

Windows example 

	md test
	cd test

NEXT : create a python virtual environment and activate it.


### STEP 1 Install a Python virtual environment

For Linux/Mac 

	python3 -m venv venv
	
	source venv/bin/activate

For Windows 
	
We assume that you already have installed git-bash.  If so open a git-bash console and :

	python -m venv venv 
	
	venv\Scripts\activate

### STEP 2 Clone the scripts

	git clone https://github.com/pcardotatgit/tor_ip_list_to_asa.git
	cd  tor_ip_list_to_asa
	
### STEP 3 Install needed python modules

We need the **requests**, **crayons**, **pyyaml**,**netmiko** python modules

install it with the following console command :

	pip install requests
	pip install crayons
	pip install pyyaml
	pip install netmiko
	
Or you can install them with the following  :
	
	pip install -r requirements.txt

# Run the application

For running the application you must first run the **1-get_tor_ip_list.py** script.

Open a console terminal and go to the folder where are located the scripts. Then run the script

	python 1-get_tor_ip_list.py 

You can let it run.

You can Have a look to this script at the top and you can change some parameters :

```python
	frequency=3600 # frequency in seconds
	group_name='TOR_NET_GROUP' # ASA network group name
	cli_file='asa_cli.txt'# name of the resulting asa cli command file
```

Then run the second script 

	python 2-asa_send_cli.py.py

BUT FIRST  you must edit the **asa_devices_list** and set the device variables

