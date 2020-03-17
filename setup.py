from setuptools import find_packages, setup

from tfn import __author__, __description__, __email__, __version__

setup(
    name='tensor-field-networks',
    author=__author__,
    author_email=__email__,
    version=__version__,
    description=__description__,
    packages=find_packages(),
    install_requires=[
        'tensorflow-gpu>=2.0',
        'numpy',
        'matplotlib'
    ]
)
