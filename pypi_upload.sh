python3 setup.py sdist bdist_wheel
pip3 setup.py install --user 
# twine upload --repository-url https://test.pypi.org/legacy/ dist/*