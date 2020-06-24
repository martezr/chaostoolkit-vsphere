# -*- coding: utf-8 -*-
from chaoslib.types import Configuration, Secrets
from chaosvsphere import vsphere_client
from pyVmomi import vim

__all__ = ["vm_state"]


def vm_state(state: str,
             vm_name: str,
             configuration: Configuration = None,
             secrets: Secrets = None) -> bool:
    """
    Determines if EC2 instances match desired state
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
            if vm.runtime.powerState != state:
                return False
    return True
