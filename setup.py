import os
import sys
from pathlib import Path

import tensorflow as tf
from setuptools import (
    find_packages,
    setup,
    Command,
)

# Package meta-data.
NAME = 'trainer'
DESCRIPTION = 'Trainer powered by cloud ml'

REQUIRED = [
    'tensorflow-gpu==1.13.*' if tf.test.is_gpu_available() else 'tensorflow==1.13.*',
    'tensorflow-model-analysis==0.13.*'
]

EXTRAS = dict(
    dev=[
        'pytest==4.2.*',
        'pytest-cov==2.6.*',
        'pytest-mock==1.10.*',
        'pytest-xdist==1.26.*',
        'tox==3.7.*',
    ],
)

# Load the package's __version__.py module as a directory.
about = {}
project_slug = NAME.lower().replace('-', '_').replace(' ', '_')
with open(str(Path('{}/{}'.format(project_slug, '__version__.py')).resolve())) as f:
    exec(f.read(), about)


class ReleaseCommand(Command):
    """ref. https://github.com/kennethreitz/setup.py/blob/master/setup.py"""
    user_options = []

    @staticmethod
    def status(s):
        """Prints things in bold."""
        print('\033[1m{0}\033[0m'.format(s))

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        try:
            self.status('Removing previous builds...')
            Path('dist').rmdir()
        except OSError:
            pass

        self.status('Building Source and Wheel (universal) distribution...')
        os.system('{} setup.py sdist bdist_wheel --universal'.format(sys.executable))

        self.status('Pushing git tags...')
        os.system('git tag v{}'.format(about['__version__']))
        os.system('git push --tags')

        sys.exit()


# Where the magic happens:
setup(
    name=NAME,
    version=about['__version__'],
    description=DESCRIPTION,
    packages=find_packages(exclude=['tests', '*.tests', '*.tests.*', 'tests.*']),
    python_requires='==3.5.*',
    install_requires=REQUIRED,
    extras_require=EXTRAS,
    include_package_data=True,
    license='MIT',
    cmdclass=dict(
        release=ReleaseCommand,
    ),
)
