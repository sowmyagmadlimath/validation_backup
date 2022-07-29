#!/usr/bin/python3
from http import client
import json
from result_output import ResultOutput
import importlib.util
import sys
from pprint import pprint
import socket
import vagrant
import os
import re
import shutil
import subprocess
import sys
import tempfile
import time
from typing import Generator
from fabric.api import *


class Activity():

    
    def testcase_check_local_status(self,test_object):
        testcase_description="Checking local Virtual Machine status  "
    
        vms_status=['running']
        expected_result="local machine is running"
        actual = ""
        test_object.update_pre_result(testcase_description,expected_result)
        # print("Came back")
        try: 
           
            vm_dir='/home/ubuntu/workspace/pc1-backup-restore-master'
            v = vagrant.Vagrant(vm_dir)
            vm_status_list=[]
            vm_status=v.status(vm_name = "local")
            print(vm_status)


            # if len(vm_status)==3 and run in vms_status:
            #     actual = "VirtualMachine1: "+vm1_name+"VirtualMachine2: "+vm2_name+"VirtualMachine3: "+vm3_name+"VirtualMachinesStatus"+vm_status_list
            #     return test_object.update_result(1,expected_result,actual,testcase_description,"nuvepro.com")
            # actual = "resource not found"
            # return test_object.update_result(0,expected_result,actual,testcase_description,"nuvepro.com")            

        except Exception as e:    
            print(str(e))
            test_object.update_result(-1,expected_result,"Internal Server error","Please check with Admin","")
            test_object.eval_message["testcase_check_Container"]=str(e)
    
    def testcase_check_DNS_virtual_machines(self,test_object):
        testcase_description="Checking DNS virtual machines"
        DNS_VM_1='Dns-srv'
        DNS_VM_2='Dns-client01'
        DNS_VM_3='Dns-client02'
        vms_status=['running']
        expected_result="VirtualMachine1: "+DNS_VM_1+"VirtualMachine2: "+DNS_VM_2+"VirtualMachine3: "+DNS_VM_3+"VirtualMachinesStatus"+vms_status
        actual = ""
        test_object.update_pre_result(testcase_description,expected_result)
        try:
            vm_dir2='/home/ubuntu/pc1-network-services/exercise-2'
            v = vagrant.Vagrant(vm_dir2)
            vm_status_list=[]
            vm_status=v.status()
            vm1_name=v.status()[0][0]
            vm2_name=v.status()[1][0]
            vm3_name=v.status()[2][0]

            vm1_status=v.status()[0][1]
            vm2_status=v.status()[1][1]
            vm3_status=v.status()[2][1]
            vm_status_list.append(vm1_status)
            vm_status_list.append(vm2_status)
            vm_status_list.append(vm3_status)
            vm_stat=''
            for run in vm_status_list: 
                vm_stat=run
            if len(vm_status)==3 and run in vms_status:
                actual = "VirtualMachine1: "+vm1_name+"VirtualMachine2: "+vm2_name+"VirtualMachine3: "+vm3_name+"VirtualMachinesStatus"+vm_status_list
                return test_object.update_result(1,expected_result,actual,testcase_description,"nuvepro.com")
            actual = "resource not found"
            return test_object.update_result(0,expected_result,actual,testcase_description,"nuvepro.com")
        except Exception as e:    
            test_object.update_result(-1,expected_result,"Internal Server error","Please check with Admin","")
            test_object.eval_message["testcase_check_Image"]=str(e)


def start_tests(args):
    # args=sys.argv[1]
    
    
    if "result_output" not in sys.modules:
        importlib.import_module("result_output")
    else:   
        importlib.reload(sys.modules["result_output"])

    
    challenge_test=Activity()
    test_object=ResultOutput(args)
    challenge_test. testcase_check_vm_status(test_object)
    # challenge_test.testcase_check_DNS_virtual_machines(test_object)

    print(json.dumps(test_object.result_final(),indent=4))
    return test_object.result_final()

def main():
    
    args = sys.argv[1]
    start_tests(args)

if __name__== "__main__" :
    main()
