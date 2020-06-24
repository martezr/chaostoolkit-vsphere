# -*- coding: utf-8 -*-
from copy import deepcopy
from unittest.mock import MagicMock, patch

import pytest

from chaosvsphere.vm.actions import (
    start_vm, stop_vm)

from chaoslib.exceptions import FailedActivity


@patch('chaosvsphere.vm.actions.vsphere_client', autospec=True)
def test_stop_vm(vsphere_client):
    client = MagicMock()
    vsphere_client.return_value = client
    name = "i-1234567890abcdef0"
    stop_vm(name)
    client.stop_instances.assert_called_with(
        InstanceIds=[inst_id], Force=False)
