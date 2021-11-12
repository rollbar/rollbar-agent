# Upgrading from ratchet-agent

Clone the rollbar-agent repo:

    $ git clone https://github.com/rollbar/rollbar-agent.git

Copy over the rollbar-agent files into your existing ratchet-agent directory.

Uninstall the ratchet-agent init.d service if installed:

    service ratchet-agent stop
    chkconfig --del ratchet-agent
    rm /etc/init.d/ratchet-agent

Backup `rollbar-agent.conf` and rename your existing `ratchet-agent.conf` to be `rollbar-agent.conf`. **Note that Rollbar libraries now write to `.rollbar` files rather than `.ratchet` files**, so make sure you modify `ext_safelist` to include rollbar files and `targets` to point to the right files.

Install the new init.d script if desired:

    ln -s /path/to/rollbar-agent/rollbar-agent-init.sh /etc/init.d/rollbar-agent
    chkconfig --add rollbar-agent
    chkconfig on rollbar-agent
    service rollbar-agent start
    
If installing the init.d script, copy your environment specific configuration from your existing `ratchet-agent-init.sh` into `rollbar-agent-init.sh`.
