# -*- coding: utf-8 -*-
from pyVim.connect import SmartConnect, Disconnect
from pyVmomi import vim, vmodl
import ssl
import os
from typing import List
from chaoslib.discovery.discover import (discover_actions, discover_probes,
                                         initialize_discovery_result)
from chaoslib.types import (Discovery, DiscoveredActivities,
                            DiscoveredSystemInfo, Configuration, Secrets)
from chaoslib.exceptions import FailedActivity
from logzero import logger


__all__ = ["__version__", "vsphere_client"]

__version__ = '0.1.0'


def vsphere_client(configuration: Configuration = None,
                   secrets: Secrets = None):
    """
    Private function that authorizes against the vSphere API.
    """
    # now setup your connection properties
    host = configuration.get("vsphere_server")
    port = configuration.get("vsphere_port", 443)
    verify_ssl = configuration.get("vsphere_verify_ssl", True)

    if secrets:
        username = secrets.get("vsphere_username")
        password = secrets.get("vsphere_password")
    else:
        username = os.getenv("VSPHERE_USERNAME")
        password = os.getenv("VSPHERE_PASSWORD")

    # now connect to your vCenter/vSphere
    context = None
    if hasattr(ssl, '_create_unverified_context'):
        context = ssl._create_unverified_context()
    connection = SmartConnect(host=host,
                              user=username,
                              pwd=password,
                              port=port,
                              sslContext=context)
    if not connection:
        print("Could not connect to the specified host using specified "
              "username and password")
    return connection


def discover(discover_system: bool = True) -> Discovery:
    """
    Discover vSphere capabilities from this extension as well, if a vsphere
    configuration is available, some information about the vSphere environment.
    """
    logger.info("Discovering capabilities from chaostoolkit-vsphere")

    discovery = initialize_discovery_result(
        "chaostoolkit-vsphere", __version__, "vsphere")
    discovery["activities"].extend(load_exported_activities())

    return discovery


###############################################################################
# Private functions
###############################################################################
def load_exported_activities() -> List[DiscoveredActivities]:
    """
    Extract metadata from actions and probes exposed by this extension.
    """
    activities = []
    activities.extend(discover_actions("chaosvsphere.vm.actions"))
    activities.extend(discover_probes("chaosvsphere.vm.probes"))

    return activities
