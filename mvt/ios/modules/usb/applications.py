# Mobile Verification Toolkit (MVT)
# Copyright (c) 2021-2022 Claudio Guarnieri.
# Use of this software is governed by the MVT License 1.1 that can be found at
#   https://license.mvt.re/1.1/

import logging

from pymobiledevice3.services.installation_proxy import \
    InstallationProxyService

from .base import IOSUSBExtraction


class Applications(IOSUSBExtraction):
    """This class extracts all applications installed on the phone"""
    def __init__(self, file_path: str = None, target_path: str = None,
                 results_path: str = None, fast_mode: bool = False,
                 log: logging.Logger = None, results: list = []) -> None:
        super().__init__(file_path=file_path, target_path=target_path,
                         results_path=results_path, fast_mode=fast_mode,
                         log=log, results=results)

    def check_indicators(self) -> None:
        if not self.indicators:
            return

        for result in self.results:
            ioc = self.indicators.check_app_id(result["CFBundleIdentifier"])
            if ioc:
                result["matched_indicator"] = ioc
                self.detected.append(result)

    def run(self) -> None:
        user_apps = InstallationProxyService(lockdown=self.lockdown).get_apps("User")
        for u in user_apps:
            u["type"] = "user"

        system_apps = InstallationProxyService(lockdown=self.lockdown).get_apps("System")
        for s in system_apps:
            s["type"] = "system"

        self.results = user_apps + system_apps

        self.log.info("{} applications identified on the phone".format(len(self.results)))