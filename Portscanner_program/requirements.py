#!/bin/python3

import importlib

import subprocess

import time

module_to_check=['importlib','subprocess','time','nmap','argparse','re','os','asyncio','concurrent.futures','colorama','Fore','Style']

time.sleep(1)

user_input=input("Do you want to continue the process  to check required modules and install it:(Y/N)")


if(user_input == "y" or user_input=="yes" or user_input=="Y" or user_input=="YES"):

    time.sleep(1)

    print("Process started to check the require modules...")

    time.sleep(1)

    print("process in  loading........")

    time.sleep(1)

    for module_name in module_to_check:
        try:
            importlib.import_module(module_name)
            time.sleep(2)
            print(f"{module_name} is already installed")

        except ImportError:
            try:
                subprocess.run(['pip','install',module_name])
                print(f"{module_name} has been successfully installled")
            except subprocess.CalledProcessError:
                time.sleep(2)
                print(f"{module_name} could not be installed..")
                exit()


elif(user_input == "no" or user_input=="NO" or user_input=="n" or user_input=="N"):
    print(f"Process is cancelled by user and extiting from this process in 3 seconds......")
    time.sleep(3)
    exit()


else:

    print(f"Soemthing went wrong and  exiting from the process in 3 seconds...")
    time.sleep(3)
    exit()
