# setup.py
from setuptools import setup, find_packages
import os

lib_folder = os.path.dirname(os.path.realpath(__file__))
requirement_path = f"{lib_folder}/requirements.txt"
install_requires = []
if os.path.isfile(requirement_path):
    with open(requirement_path) as f:
        install_requires = f.read().splitlines()

setup(
    name='docai-dev',
    version='0.1.0',
    description='DocAI Python module',
    author='Sonu Sudhakaran',
    author_email='sonu.sudhakaran@gmail.com',
    packages=find_packages(),
    install_requires=install_requires,  # List any dependencies here
)
