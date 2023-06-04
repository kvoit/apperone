import re
from psutil import Process

from apperone.output import log

class AppConfigs:
    def __init__(self, config):
        self.app_configs = []
        for app in config["apps"]:
            log(f"Adding {app}")
            self.app_configs.append(
                AppConfig(app,
                          groups=config["apps"][app]["groups"],
                          name=config["apps"][app]["name"],
                          cmdline=config["apps"][app]["cmdline"],
                          username=config["apps"][app]["username"],
                          time=config["apps"][app]["time"])
            )
        self.index = 0
        self.config = config

    def __iter__(self):
        return self

    def __next__(self):
        if self.index >= len(self.app_configs):
            self.index = 0
            raise StopIteration
        app_config = self.app_configs[self.index]
        self.index += 1
        return app_config


class AppConfig:
    def __init__(self, app_id, groups=(), name=r".*", cmdline=r".*", username=r".*", time=3600):
        self.app_id = app_id
        self.groups = groups
        self.name = name
        self.cmdline = cmdline
        self.username = username
        self.time = time

    def check_process(self, process: Process):
        if re.match(self.username, process.username()) \
                and re.match(self.name, process.name()) \
                and re.match(self.cmdline, " ".join(process.cmdline())):
            return True
        else:
            return False
