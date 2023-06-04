#!/usr/bin/env python3
import os
import sys
import time
import daemon
import yaml
from pathlib import Path
from apperone.apperone import Apperone

apperone = None


def run_daemon():
    # Your daemon code goes here
    while True:
        start_time = time.time()

        apperone.check()

        elapsed_time = time.time() - start_time

        sleep_time = max(60 - elapsed_time, 0)
        time.sleep(sleep_time)


if __name__ == '__main__':
    # Change directory to the desired working directory
    os.chdir('/')

    configfile = Path("~/.apperone/config.yml").expanduser()

    # config = {
    #     "database": "~/.apperone/timedata.db",
    #     "apps": {
    #         "minecraft": {
    #             "groups": ["games"],
    #             "name": "java",
    #             "cmdline": r".*minecraft.*",
    #             "username": "voit",
    #             "time": 4200,
    #         }
    #     }
    # }
    #
    # with open(configfile, 'w') as file:
    #     yaml.dump(config, file)

    with open(configfile, 'r') as file:
        config = yaml.load(file, Loader=yaml.FullLoader)

    apperone = Apperone(config)

    # # Create a context for the daemon
    with daemon.DaemonContext():
        run_daemon()
