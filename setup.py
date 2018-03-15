import os.path
from setuptools import Command, find_packages, setup

HERE = os.path.abspath(os.path.dirname(__file__))

README_PATH = os.path.join(HERE, 'README.rst')
try:
    README = open(README_PATH).read()
except IOError:
    README = ''

setup(
    name='rollbar-agent',
    data_files=[('', ['rollbar-agent', 'rollbar-agent-init.sh', 'rollbar-agent.conf', 'LICENSE', 'requirements.txt'])],
    version='0.4.3',
    description='Rollbar server-side agent',
    long_description=README,
    author='Rollbar, Inc.',
    author_email='support@rollbar.com',
    url='http://github.com/rollbar/rollbar-agent',
    classifiers=[
        "Programming Language :: Python",
        "License :: OSI Approved :: MIT License",
        "Development Status :: 4 - Beta",
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







