python3 setup.py sdist bdist_wheel

# install locally
pip3 install --user ./dist/amaxfactory_tokenika*.tar.gz

# run Twine to upload all of the archives under dist to the Test PyPi:
#python3 -m twine upload --repository-url https://test.pypi.org/legacy/ dist/*

# run Twine to upload all of the archives under dist to the PyPi:
# python3 -m twine upload dist/*
