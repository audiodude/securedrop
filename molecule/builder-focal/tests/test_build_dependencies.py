import os

import pytest

SECUREDROP_TARGET_DISTRIBUTION = os.environ.get("SECUREDROP_TARGET_DISTRIBUTION")
SECUREDROP_PYTHON_VERSION = os.environ.get("SECUREDROP_PYTHON_VERSION", "3.8")
DH_VIRTUALENV_VERSION = "1.2.2"

testinfra_hosts = ["docker://{}-sd-app".format(SECUREDROP_TARGET_DISTRIBUTION)]


@pytest.mark.xfail(reason="This check conflicts with the concept of pegging" "dependencies")
def test_build_all_packages_updated(host):
    """
    Ensure a dist-upgrade has already been run, by checking that no
    packages are eligible for upgrade currently. This will ensure that
    all upgrades, security and otherwise, have been applied to the VM
    used to build packages.
    """
    c = host.run("apt-get --simulate -y dist-upgrade")
    assert c.rc == 0
    assert "No packages will be installed, upgraded, or removed." in c.stdout


def test_python_version(host):
    """
    The Python 3 version shouldn't change between LTS releases, but we're
    pulling in some packages from Debian for dh-virtualenv support, so
    we must be careful not to change Python as well.
    """
    c = host.run("python3 --version")
    version_string = "Python {}".format(SECUREDROP_PYTHON_VERSION)
    assert c.stdout.startswith(version_string)


def test_dh_virtualenv(host):
    """
    Confirm the expected version of dh-virtualenv is found.
    """
    expected_version = DH_VIRTUALENV_VERSION
    version_string = "dh_virtualenv {}".format(expected_version)
    c = host.run("dh_virtualenv --version")
    assert c.stdout.startswith(version_string)
