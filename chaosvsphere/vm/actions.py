# -*- coding: utf-8 -*-
from random import choice
from typing import Any, Dict, List

from chaoslib.exceptions import ActivityFailed
from chaoslib.types import Configuration, Secrets

from chaosvsphere import vsphere_client
from chaosvsphere.utils import WaitForTasks

from logzero import logger
from pyVmomi import vim, vmodl

__all__ = ["start_vm", "stop_vm", "connect_nic", "disconnect_nic"]


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


def connect_nic(vm_name: str, nic_number: int,
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

    for vm in vmList:
        if vm.name == vm_name:
            vm_obj = vm

    nic_prefix_label = 'Network adapter '
    nic_label = nic_prefix_label + str(nic_number)
    virtual_nic_device = None
    for dev in vm_obj.config.hardware.device:
        if isinstance(dev, vim.vm.device.VirtualEthernetCard) \
                and dev.deviceInfo.label == nic_label:
            virtual_nic_device = dev

    virtual_nic_spec = vim.vm.device.VirtualDeviceSpec()
    virtual_nic_spec.operation = vim.vm.device.VirtualDeviceSpec.Operation.edit
    virtual_nic_spec.device = virtual_nic_device

    connectable = vim.vm.device.VirtualDevice.ConnectInfo()
    connectable.connected = True
    virtual_nic_spec.device.connectable = connectable
    dev_changes = []
    dev_changes.append(virtual_nic_spec)
    spec = vim.vm.ConfigSpec()
    spec.deviceChange = dev_changes
    task = vm_obj.ReconfigVM_Task(spec=spec)
    WaitForTasks([task], client)
    return '{"status":"Nic connected"}'


def disconnect_nic(vm_name: str, nic_number: int,
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

    for vm in vmList:
        if vm.name == vm_name:
            vm_obj = vm

    nic_prefix_label = 'Network adapter '
    nic_label = nic_prefix_label + str(nic_number)
    virtual_nic_device = None
    for dev in vm_obj.config.hardware.device:
        if isinstance(dev, vim.vm.device.VirtualEthernetCard) \
                and dev.deviceInfo.label == nic_label:
            virtual_nic_device = dev

    virtual_nic_spec = vim.vm.device.VirtualDeviceSpec()
    virtual_nic_spec.operation = vim.vm.device.VirtualDeviceSpec.Operation.edit
    virtual_nic_spec.device = virtual_nic_device

    connectable = vim.vm.device.VirtualDevice.ConnectInfo()
    connectable.connected = False
    virtual_nic_spec.device.connectable = connectable
    dev_changes = []
    dev_changes.append(virtual_nic_spec)
    spec = vim.vm.ConfigSpec()
    spec.deviceChange = dev_changes
    task = vm_obj.ReconfigVM_Task(spec=spec)
    WaitForTasks([task], client)
    return '{"status":"Nic disconnected"}'


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
