from setuptools import setup, find_packages
from setuptools.command.install import install
from setuptools.command.develop import develop

setup(
    name='potyspoty',
    version='0.1',
    license='GNU GPLv3 or posterior',
    description='',
    url='https://github.com/BielStela/DaSouza_spoty',
    download_url='https://github.com/BielStela/DaSouza_spoty.git',
    author='Biel Stela',
    author_email='',
    packages=find_packages(),
    # If any package contains *.txt or *.rst files, include them:
    # package_data={'': ['*.yaml', '*.yml']},
    install_requires=['pandas', 'numpy', 'spotipy']
)
