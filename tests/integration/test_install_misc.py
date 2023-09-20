import os

import pytest

from pipenv.utils.shell import temp_environ
from .conftest import DEFAULT_PRIVATE_PYPI_SERVER, pipenv_instance_private_pypi


@pytest.mark.urls
@pytest.mark.extras
@pytest.mark.install
def test_install_uri_with_extras(pipenv_instance_pypi):
    server = DEFAULT_PRIVATE_PYPI_SERVER.replace("/simple", "")
    file_uri = f"{server}/packages/plette/plette-0.2.2-py2.py3-none-any.whl"
    with pipenv_instance_pypi() as p:
        with open(p.pipfile_path, 'w') as f:
            contents = f"""
[[source]]
url = "{p.index_url}"
verify_ssl = false
name = "testindex"

[packages]
plette = {{file = "{file_uri}", extras = ["validation"]}}
"""
            f.write(contents)
        c = p.pipenv("install")
        assert c.returncode == 0
        assert "plette" in p.lockfile["default"]
        assert "cerberus" in p.lockfile["default"]


@pytest.mark.ssl
@pytest.mark.needs_mitmproxy
@pytest.mark.extras
@pytest.mark.install
def test_install_verify_custom_ssl_verify(pipenv_instance_private_pypi_secure, cert_path):
    """Ensure environment variables are not expanded in lock file.
        """
    with temp_environ(), pipenv_instance_private_pypi_secure() as p:
        os.environ["REQUESTS_CA_BUNDLE"] = cert_path

        with open(p.pipfile_path, "w") as f:
            f.write(
                f"""
[[source]]
url = "{p.index_url}"
verify_ssl = true
name = 'mockpi'

[packages]
six = {{}}
"""
            )

        c = p.pipenv("install -v")
        assert c.returncode == 0
        assert "six" in p.lockfile["default"]


@pytest.mark.ssl
@pytest.mark.needs_mitmproxy
@pytest.mark.extras
@pytest.mark.install
def test_install_verify_custom_ssl_no_verify(pipenv_instance_private_pypi_secure, cert_path):
    """Ensure environment variables are not expanded in lock file.
        """
    with pipenv_instance_private_pypi_secure() as p:
        with open(p.pipfile_path, "w") as f:
            f.write(
                f"""
[[source]]
url = "{p.index_url}"
verify_ssl = false
name = 'mockpi'

[packages]
six = {{}}
"""
            )

        c = p.pipenv("install -v")
        assert c.returncode == 0
        assert "six" in p.lockfile["default"]


@pytest.mark.ssl
@pytest.mark.needs_mitmproxy
@pytest.mark.extras
@pytest.mark.install
def test_install_verify_custom_ssl_verify_fail(pipenv_instance_private_pypi_secure, cert_path):
    """Ensure environment variables are not expanded in lock file.
        """
    with pipenv_instance_private_pypi_secure() as p:
        with open(p.pipfile_path, "w") as f:
            f.write(
                f"""
[[source]]
url = "{p.index_url}"
verify_ssl = true
name = 'mockpi'

[packages]
six = {{}}
"""
            )

        c = p.pipenv("install -v")
        assert c.returncode == 1
