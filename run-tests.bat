
pip install -e .[test] --upgrade --upgrade-strategy=only-if-needed
pipenv install --dev
git submodule sync && git submodule update --init --recursive
cmd /c start pipenv run pypi-server run -v --host=0.0.0.0 --port=8080 --hash-algo=sha256 --disable-fallback ./tests/pypi/ ./tests/fixtures
cmd /c start pipenv run mitmdump -p 8443 --set confdir=./tests/test_artifacts/certs --mode reverse:http://127.0.0.1:8080
pipenv run pytest -n auto -v tests
