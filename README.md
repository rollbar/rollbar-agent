ratchetd
========
A daemon to monitor log files and push messages to [Ratchet.io](http://ratchet.io).


Requirements
------------
ratchetd requires:

- A unix-like system (tested on Fedora Linux and Mac OS X)
- Python 2.6+
- requests 0.13.1+
- a [Ratchet.io](http://ratchet.io) account


Installation
------------
Get the ratchet code by cloning the git repo (or [download the zip](https://github.com/brianr/ratchetd/zipball/master) and unzip it somewhere):

    git clone https://github.com/brianr/ratchetd.git

Once you download it, install the requirements (in a virtualenv, if you wish):

    cd ratchetd
    pip install -r requirements.txt

To make sure it works, start it up:

    cd ratchetd
    ./ratchetd

Press Ctrl-c to exit.

See Configuration for configuration options to make it actually useful.

Ratchetd comes with an example init.d script, chkconfig compatible and tested on Fedora Linux. To install it, symlink `ratchetd-init.sh` to `/etc/init.d/ratchetd` and add to chkconfig:

    ln -s /path/to/ratchetd/ratchetd-init.sh /etc/init.d/ratchetd
    chkconfig --add ratchetd
    chkconfig on ratchetd
    service ratchetd start


Configuration
-------------
Configuration options for ratchetd itself are in `ratchetd.conf`. If you're using the init script, it has a few of its own configuration variables inside which control how it runs.

### `ratchetd.conf`
At the bare minimum, you will want to change the following variables:

- params.access_token -- your Ratchet.io access token
- targets -- white-space-separated list of files or directories (non-recursive) to process.

Setting the following variables will enable github integration:

- params.root -- path to your code root
- params.branch -- the current branch
- params.github.account -- your github account name
- params.github.repo -- your github repo name

Other options are documented in the sample config file.

### ratchetd-init.sh
Configuration variables should be self-explanatory. If you're not using a virtualenv, set `VIRTUALENV=""`.

Additional Help
---------------
If you have any questions, feedback, etc., drop me a line at brian@ratchet.io
