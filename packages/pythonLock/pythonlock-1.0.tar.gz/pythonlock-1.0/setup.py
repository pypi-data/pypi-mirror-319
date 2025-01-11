from setuptools import setup, find_packages
import codecs
import os

here = os.path.abspath(os.path.dirname(__file__))

with codecs.open(os.path.join(here, "README.md"), encoding="utf-8") as fh:
    long_description = "\n" + fh.read()

VERSION = '1.0'
DESCRIPTION = 'Package to used for handling lock mechanism when running appplication with multiple replicas'
LONG_DESCRIPTION = 'Package to used for handling lock mechanism when running appplication with multiple replicas. It usage Redis or MYSQL lock as per your input'

# Setting up
setup(
    name="pythonLock",
    version=VERSION,
    author="Tanmay Varade",
    author_email="tanmayvarade235@gmail.com",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=long_description,
    packages=find_packages(),
    install_requires=['APScheduler', 'mysql-connector-python','redis','requests'],
    keywords=['python', 'distributed', 'lock', 'rds', 'sql', 'redis', 'replicas', 'kubernetes'],
)
