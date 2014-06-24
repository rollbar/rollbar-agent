rollbar-agent
=============
A daemon to monitor log files and push messages to Rollbar_.


Requirements
------------
rollbar-agent requires:

- A unix-like system (tested on Fedora Linux and Mac OS X)
- Python 2.6+
- requests 0.13.1+ (will be installed by pip or setup.py, below)
- a Rollbar_ account


Installation
------------

**Installing with pip**

If you're familiar with pip, use this option. (If not, see the "Installing from source" method below.)

In a virtualenv, install like so::

    pip install rollbar-agent

This will install the rollbar-agent files in the root directory of your virtualenv. 

**Installing from source**

If you're comfortable with Git::

    git clone https://github.com/rollbar/rollbar-agent.git
    cd rollbar-agent

Or just grab the .tar.gz::

    wget https://github.com/rollbar/rollbar-agent/archive/v0.3.9.tar.gz
    tar -xzf v0.3.9
    cd rollbar-agent-0.3.9

Then install (may require sudo)::

    python setup.py install
    
Symlink the rollbar-agent executable to /usr/local/rollbar-agent::

    ln -s /usr/local/rollbar-agent /path/to/rollbar-agent/rollbar-agent

**init.d script**

rollbar-agent comes with an example init.d script, chkconfig compatible and tested on Fedora Linux, update-rc.d on Ubuntu Linux. To install it, symlink ``rollbar-agent-init.sh`` to ``/etc/init.d/rollbar-agent``::

    chmod +x /path/to/rollbar-agent-init.sh
    ln -s /path/to/rollbar-agent-init.sh /etc/init.d/rollbar-agent

On Ubuntu, you'll need to add to rc.d. Run the following::

    update-rc.d rollbar-agent defaults

On Fedora, add to chkconfig::

    chkconfig --add rollbar-agent
    chkconfig on rollbar-agent
    
On other systems, check your system's documentation for its equivalent of chkconfig.

Now, start the service::

    service rollbar-agent start

To check that it's running, tail its log file::

    tail -f /var/log/rollbar-agent.log

Configuration
-------------
Configuration options for rollbar-agent itself are in `rollbar-agent.conf`. If you're using the init script, it has a few of its own configuration variables inside which control how it runs.

**rollbar-agent.conf**
At the bare minimum, you will want to change the following variables:

- ``params.access_token`` -- your Rollbar access token, specifically an API token that allows "post_server_item"
- ``targets`` -- white-space-separated list of files or directories (non-recursive) to process.
- ``statefile`` -- path to a file where the state will be stored. File does not need to exist, but the directory does. This file should *not* be placed somewhere it is likely to be deleted, as that will trigger all files to be re-processed. ``/tmp`` is not a good location.

There are several parameters about formats, etc.; you do NOT need to do anything with these if you're only using rollbar-agent as a relay in combination with one of our other libraries.

Setting the following variables will improve integration:

- ``params.root`` -- path to your code root
- ``params.branch`` -- the current branch

Other options are documented in the sample config file.

**rollbar-agent-init.sh**
Configuration variables should be self-explanatory. If you're not using a virtualenv, set ``VIRTUALENV=""``.


Contributing
------------

Contributions are welcome. The project is hosted on github at http://github.com/rollbar/rollbar-agent


Additional Help
---------------
If you have any questions, feedback, etc., drop us a line at team@rollbar.com


.. _Rollbar: http://rollbar.com/
.. _`download the zip`: https://github.com/rollbar/pyrollbar/zipball/master
.. _rollbar-agent: http://github.com/rollbar/rollbar-agent
.. _pip: http://www.pip-installer.org/en/latest/installing.html
