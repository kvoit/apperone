import psutil
from apperone.app_time import AppTime
from apperone.app_config import AppConfigs
from apperone.output import log


class Apperone:
    def __init__(self, config):
        self.app_time = AppTime(config["database"])
        self.app_configs = AppConfigs(config)

    def check(self):
        pids = psutil.pids()

        for pid in pids:
            try:
                process = psutil.Process(pid=pid)
            except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                continue

            for i, app in enumerate(self.app_configs):
                if app.check_process(process):
                    log(f"Checking app {app.app_id} ({i})")
                    if not self.app_time.increase_times(app):
                        process.kill()
