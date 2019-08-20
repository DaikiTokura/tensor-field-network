from setuptools import find_packages, setup

from tfn import __author__, __description__, __email__, __version__

setup(
    name='tfn-layers',
    author=__author__,
    author_email=__email__,
    version=__version__,
    description=__description__,
    packages=find_packages(),
    install_requires=[
        'tensorflow-gpu==2.0.0b1',
        'numpy'
    ],
    extras_require={
        'tests': ['pytest'],
        'tensorflow': ['tensorflow==2.0.0b1'],
        'h5py': ['h5py']
    }
)
