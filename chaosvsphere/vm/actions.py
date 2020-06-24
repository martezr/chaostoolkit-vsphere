# -*- coding: utf-8 -*-
from random import choice
from typing import Any, Dict, List

from chaoslib.exceptions import ActivityFailed
from chaoslib.types import Configuration, Secrets

from chaosvsphere import vsphere_client
from chaosvsphere.utils import WaitForTasks

from logzero import logger
from pyVmomi import vim, vmodl

__all__ = ["start_vm", "stop_vm"]


def start_vm(vm_name: str, configuration: Configuration = None,
             secrets: Secrets = None):
    client = vsphere_client(configuration, secrets)
    content = client.content
    objView = content.viewManager.CreateContainerView(content.rootFolder,
                                                      [vim.VirtualMachine],
                                                      True)
    vmList = objView.view
    objView.Destroy()

    # Find the vm and power it on
    tasks = [vm.PowerOn() for vm in vmList if vm.name == vm_name]
    WaitForTasks(tasks, client)
    return '{"status":"Powering on VM"}'


def stop_vm(vm_name: str, configuration: Configuration = None,
            secrets: Secrets = None):
    client = vsphere_client(configuration, secrets)
    content = client.content
    objView = content.viewManager.CreateContainerView(content.rootFolder,
                                                      [vim.VirtualMachine],
                                                      True)
    vmList = objView.view
    objView.Destroy()

    # Find the vm and power it on
    tasks = [vm.PowerOffVM_Task() for vm in vmList if vm.name == vm_name]
    WaitForTasks(tasks, client)
    return '{"status":"VM powered off"}'


def disconnect_nic(vm_name: str, nic_id: int,
                   configuration: Configuration = None,
                   secrets: Secrets = None):
    """
    """
    client = vsphere_client(configuration, secrets)
    content = client.content
    objView = content.viewManager.CreateContainerView(content.rootFolder,
                                                      [vim.VirtualMachine],
                                                      True)
    vmList = objView.view
    objView.Destroy()

    # Find the vm and power it on
    tasks = [vm.PowerOffVM_Task() for vm in vmList if vm.name == vm_name]
    WaitForTasks(tasks, client)
    return '{"status":"VM powered off"}'


def destroy_vm(vm_name: str, configuration: Configuration = None,
               secrets: Secrets = None):
    client = vsphere_client(configuration, secrets)
    content = client.content
    objView = content.viewManager.CreateContainerView(content.rootFolder,
                                                      [vim.VirtualMachine],
                                                      True)
    vmList = objView.view
    objView.Destroy()

    # Find the vm and power it on
    tasks = [vm.PowerOffVM_Task() for vm in vmList if vm.name == vm_name]
    WaitForTasks(tasks, client)
    return '{"status":"VM powered off"}'
