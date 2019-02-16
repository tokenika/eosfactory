python3 setup.py sdist bdist_wheel
pip3 install --user ./dist/eosfactory_tokenika*.tar.gz # install locally
# twine upload --repository-url https://test.pypi.org/legacy/ dist/*
