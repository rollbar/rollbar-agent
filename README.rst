rollbar-agent
=============
A daemon to monitor log files and push messages to Rollbar_.


Requirements
------------
rollbar-agent requires:

- A unix-like system (tested on Fedora Linux and Mac OS X)
- Python 2.6+
- requests 0.13.1+
- a Rollbar_ account


Installation
------------
Install with pip::

    pip install rollbar-agent

This will install the rollbar-agent files in the root directory of your virtualenv. Or if you'd prefer, clone this git repo:

    git clone https://github.com/rollbar/rollbar-agent.git

See Configuration for configuration options and setup.

rollbar-agent comes with an example init.d script, chkconfig compatible and tested on Fedora Linux. To install it, symlink ``rollbar-agent-init.sh`` to ``/etc/init.d/rollbar-agent`` and add to chkconfig::

    ln -s /path/to/rollbar-agent/rollbar-agent-init.sh /etc/init.d/rollbar-agent
    chkconfig --add rollbar-agent
    chkconfig on rollbar-agent
    service rollbar-agent start

Configuration
-------------
Configuration options for rollbar-agent itself are in `rollbar-agent.conf`. If you're using the init script, it has a few of its own configuration variables inside which control how it runs.

**rollbar-agent.conf**
At the bare minimum, you will want to change the following variables:

- ``params.access_token`` -- your Rollbar access token
- ``targets`` -- white-space-separated list of files or directories (non-recursive) to process.

Setting the following variables will improve github integration:

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
If you have any questions, feedback, etc., drop me a line at brian@rollbar.com


.. _Rollbar: http://rollbar.io/
.. _`download the zip`: https://github.com/rollbar/pyrollbar/zipball/master
.. _rollbar-agent: http://github.com/rollbar/rollbar-agent
