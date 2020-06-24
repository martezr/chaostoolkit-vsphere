 # Chaos Toolkit Extension for VMware vSphere

[![Python versions](https://img.shields.io/pypi/pyversions/chaostoolkit-vsphere.svg)](https://www.python.org/)


This project is a collection of [actions][] and [probes][], gathered as an
extension to the [Chaos Toolkit][chaostoolkit].

[actions]: http://chaostoolkit.org/reference/api/experiment/#action
[probes]: http://chaostoolkit.org/reference/api/experiment/#probe
[chaostoolkit]: http://chaostoolkit.org

## Install

This package requires Python 3.5+

To be used from your experiment, this package must be installed in the Python
environment where [chaostoolkit][] already lives.

```
$ pip install -U chaostoolkit-vsphere
```

## Usage

To use the probes and actions from this package, add the following to your
experiment file:

```json
{
    "type": "action",
    "name": "stop-virtual-machine",
    "provider": {
        "type": "python",
        "module": "chaosvsphere.vm.actions",
        "func": "stop_vm",
        "arguments": {
            "vm_name": "VM01"
        }
    }
},
{
    "type": "probe",
    "name": "fetch-vm-state",
    "provider": {
        "type": "python",
        "module": "chaosvsphere.vm.probes",
        "func": "vm_state",
        "arguments": {
          "state": "poweredOn",
          "vm_name": "VM01"
        }
     }
}
```

That's it!

Please explore the code to see existing probes and actions.

## Configuration

### Setting the vCenter server and SSL verification

The VMware vSphere server and port must be configured to authenticate to the instance.

```json
{
    "configuration": {
        "vsphere_server": "vsphere.lab.local",
        "vsphere_verify_ssl": false 
    }
}
```

### Credentials

This extension uses the [pyvmomi][] library under the hood. This library expects
that you have properly [configured][creds] your environment to connect and
authenticate with the vCenter server.

#### Pass credentials explicitely

You can pass the credentials as a secret to the experiment definition as
follows:

```json
{
    "secrets": {
        "vsphere": {
            "vsphere_username": "your username",
            "vsphere_password": "your password"
        }
    }
}
```

Then, use it as follows:


```json
{
    "type": "action",
    "name": "stop-virtual-machine",
    "provider": {
       "type": "python",
       "secrets": ["vsphere"]  
       "module": "chaosvsphere.vm.actions",
        "func": "stop_vm",
        "arguments": {
            "vm_name": "VM01"
        }
    }
}
```

## Contribute

If you wish to contribute more functions to this package, you are more than
welcome to do so. Please, fork this project, make your changes following the
usual [PEP 8][pep8] code style, sprinkling with tests and submit a PR for
review.

[pep8]: https://pycodestyle.readthedocs.io/en/latest/

The Chaos Toolkit projects require all contributors must sign a
[Developer Certificate of Origin][dco] on each commit they would like to merge
into the master branch of the repository. Please, make sure you can abide by
the rules of the DCO before submitting a PR.

[dco]: https://github.com/probot/dco#how-it-works

### Develop

If you wish to develop on this project, make sure to install the development
dependencies. But first, [create a virtual environment][venv] and then install
those dependencies.

[venv]: http://chaostoolkit.org/reference/usage/install/#create-a-virtual-environment

```console
$ pip install -r requirements-dev.txt -r requirements.txt
```

Then, point your environment to this directory:

```console
$ python setup.py develop
```

Now, you can edit the files and they will be automatically be seen by your
environment, even when running from the `chaos` command locally.

### Test

To run the tests for the project execute the following:

```
$ pytest setup.py test
```
