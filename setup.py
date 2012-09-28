import os.path
from setuptools import Command, find_packages, setup

HERE = os.path.abspath(os.path.dirname(__file__))

README_PATH = os.path.join(HERE, 'README.rst')
try:
    README = open(README_PATH).read()
except IOError:
    README = ''

setup(
    name='ratchet-agent',
    data_files=[('', ['ratchet-agent', 'ratchet-agent-init.sh', 'ratchet-agent.conf', 'LICENSE', 'requirements.txt'])],
    version='0.2.1',
    description='Ratchet.io server-side agent',
    long_description=README,
    author='Ratchet, Inc.',
    author_email='support@ratchet.io',
    url='http://github.com/ratchetio/ratchet-agent',
    classifiers=[
        "Programming Language :: Python",
        "License :: OSI Approved :: MIT License",
        "Development Status :: 3 - Alpha",
        "Environment :: Web Environment",
        "Intended Audience :: Developers",
        "Topic :: Internet :: WWW/HTTP",
        "Topic :: Internet :: WWW/HTTP :: WSGI :: Middleware",
        "Topic :: Software Development",
        "Topic :: Software Development :: Bug Tracking",
        "Topic :: Software Development :: Testing",
        "Topic :: Software Development :: Quality Assurance",
        ],
    install_requires=[
        'requests',
        ],
    )







