'''
Copyright (c) 2022 Cisco and/or its affiliates.
This software is licensed to you under the terms of the Cisco Sample
Code License, Version 1.1 (the "License"). You may obtain a copy of the
License at
               https://developer.cisco.com/docs/licenses
All use of the material herein must be in accordance with the terms of
the License. All rights not expressly granted by the License are
reserved. Unless required by applicable law or agreed to separately in
writing, software distributed under the License is distributed on an "AS
IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express
or implied.
'''
from crayons import red,green,cyan,yellow
from netmiko import ConnectHandler
import sys
import yaml
import os


def select_device():
    # Just For rapid testing if you don't want to use yaml device list set correct values here under
    #device=[]    
    device = {
        'device_type': 'cisco_asa',
        'ip': '192.168.1.10',
        'username': 'patrick',
        'password': 'for_testing'
    }                 
    return(device)
    
def yaml_load(filename):
    '''
    load device information for connection from a yaml file
    '''
    fh = open(filename, "r")
    yamlrawtext = fh.read()
    yamldata = yaml.load(yamlrawtext, Loader=yaml.FullLoader)    
    return yamldata
    
def read_cli_commands(file):
    file0 = os.getcwd()+file
    command_list=[]
    with open(file0) as file1:
        content=file1.read()
    command_list=content.split('\n')
    return(command_list)

def send_cli_to_asa(*args):
    cli_file='/'+args[0]["config"]
    commands=read_cli_commands(cli_file)
    print("Update the following device")
    device = {
        'device_type': args[0]["type"],
        'ip': args[0]["ipaddr"],
        'username': args[0]["username"],
        'password': args[0]["password"]
    }  
    print(device)
    print("with the following configuration")
    for item in commands:
        print(yellow(item))      
    try:
        net_connect = ConnectHandler(**device)
        net_connect.find_prompt()    
        output = net_connect.send_config_set(commands)
        print (green(output,bold=True) )
        return 1
    except:
        return 0

def go_asa():
    print(green('Start ASAs Updates',bold=True))
    print()    
    device_list = {}
    file = os.getcwd()+"/asa_devices_list.yml"
    device_list = yaml_load(file)   
    arguments=[]
    for device in device_list["devices"]:
        print("Device {}".format(device["hostname"]))
        print("    Type {}".format(device["type"]))
        print("    Admin IP Address {}".format(device["ipaddr"]))
        #do something here
        #print('==> Update this DEVICE')
        arguments.append(device)
        if send_cli_to_asa(*arguments):
            print(green(f'Success : this device {device["ipaddr"]} had been updated'))
        else:
            print(red(f'Error : this device {device["ipaddr"]} couldn\'t be updated'))
    return 1    
    
if __name__ == "__main__":
	print()
	go_asa()   