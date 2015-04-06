
from setuptools import setup

requires = ['boto']

setup_options = dict(
    name='canary',
    version='0.1',
    description='Canary in the Cloud Coal Mine',
    author='Nate McCourtney',
    author_email='nathan@luminal.io',
    scripts=['bin/canary', 'bin/setup-and-run.sh', 'bin/setup.sh'],
    py_modules=['canary'],
    package_dir={'': 'lib'},
    install_requires=requires,
    )

setup(**setup_options)