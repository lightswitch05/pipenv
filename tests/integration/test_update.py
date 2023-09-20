import os

import pytest

from pipenv.utils.shell import temp_environ


@pytest.mark.parametrize("cmd_option", ["", "--dev"])
@pytest.mark.basic
@pytest.mark.update
def test_update_outdated_with_outdated_package(pipenv_instance_private_pypi, cmd_option):
    with pipenv_instance_private_pypi() as p:
        package_name = "six"
        p.pipenv(f"install {cmd_option} {package_name}==1.11")
        c = p.pipenv(f"update {package_name} {cmd_option} --outdated")
        assert f"Package '{package_name}' out-of-date:" in c.stdout


@pytest.mark.ssl
@pytest.mark.needs_mitmproxy
@pytest.mark.extras
@pytest.mark.update
def test_update_outdated_with_outdated_package_trusted(pipenv_instance_private_pypi_secure, cert_path):
    with pipenv_instance_private_pypi_secure() as p, temp_environ():
        os.environ["REQUESTS_CA_BUNDLE"] = cert_path
        package_name = "six"
        p.pipenv(f"install {package_name}==1.11")
        c = p.pipenv(f"update {package_name} --outdated")
        assert f"Package '{package_name}' out-of-date:" in c.stdout


@pytest.mark.ssl
@pytest.mark.needs_mitmproxy
@pytest.mark.extras
@pytest.mark.update
def test_update_outdated_with_outdated_package_secure_untrusted(pipenv_instance_private_pypi_secure, cert_path):
    with pipenv_instance_private_pypi_secure() as p, temp_environ():
        package_name = "six"
        os.environ["REQUESTS_CA_BUNDLE"] = cert_path
        p.pipenv(f"install {package_name}==1.11")
        os.environ["REQUESTS_CA_BUNDLE"] = ""
        c = p.pipenv(f"update {package_name} --outdated")
        assert "SSLCertVerificationError" in c.stderr
