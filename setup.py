from setuptools import setup, find_packages

def readme():
    with open('README.md') as f:
        return f.read()

setup(name='eosfactory',
      version='2.4',
      description='Python-based EOS smart-contract development & testing framework',
      long_description=readme(),
      classifiers=[
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3 :: Only',
        'Topic :: Software Development :: Testing',
      ],
      keywords='EOSIO, smart contract unit testing',
      url='https://github.com/tokenika/eosfactory',
      author='Tokenika',
      author_email='contact@tokenika.io',
      license='MIT',
      packages=find_packages(),
      include_package_data=True,
      install_requires=[
          'termcolor',
      ],
      zip_safe=False)
