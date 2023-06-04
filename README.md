# Apperone
Python software for limiting program time under linux

Must run as a user that can kill processes of users under surveillance, usually root.

## Installation

    pip install psutil python-daemon

## Config
Config in `~/.apperone/config.yaml`. Example:

    apps:
      minecraft:
        cmdline: .*minecraft.*
        groups:
        - games
        name: java
        time: 70
        username: voit
    database: ~/.apperone/timedata.db

`user`, `name` and `cmdline` are re.match'ed against the respective fields of psutil processes.
`groups` is reserved for later use to be able to limit e.g. all games to a certain time.

`time` is the allowed daily time in minutes. TODO: Make this a 7-element list and check depending on DOW.

## Running
Copy `apperone.service` to `/etc/systemd/system/` and, adjust `WorkingDirectory` to repository path and run

    systemctl enable apperone
    systemctl start apperone