import os
import getpass
import logging
import platform
import subprocess
from typing import Iterable


class Env:
    def __init__(self, prefix_env: str, credentials_keys: Iterable):
        self.prefix_env = prefix_env
        self.credentials_keys = credentials_keys
        self.credentials = dict.fromkeys(
            credentials_keys
        )
        self._load_credentials()

    def _load_credentials(self):
        self.credentials = {
            key: os.getenv(f"{self.prefix_env}_{key}")
            for key in self.credentials
        }
        if params := [key for key in self.credentials
                      if not self.credentials[key]]:
            self.ask_credentials_cli(params)

    def ask_credentials_cli(self, list_params: list) -> None:
        for param in list_params:
            if param.lower() in ("senha", "password"):
                value = getpass.getpass(
                    f"Informe a Senha para" f" ({self.prefix_env}): "
                )
            else:
                value = input(f"Informe o(a) {param} "
                              f"para ({self.prefix_env}): ")
            self.set_persistent_env_var(
                f"{self.prefix_env}_{param}".upper(),
                value
            )
            self.credentials[param] = value

    def set_persistent_env_var(self, var_name: str, var_value: str) -> None:
        system = platform.system()

        if system == "Windows":
            subprocess.run(["setx", var_name, var_value], check=True)
        elif system == "Linux":
            home = os.path.expanduser("~")
            bashrc_path = os.path.abspath(os.path.join(home, ".bashrc"))
            with open(bashrc_path, "a") as bashrc:
                bashrc.write(f'\nexport {var_name}="{var_value}"\n')
            logging.info(
                f"Variable added to {bashrc_path}. "
                "Please re-login or source the file."
            )
        else:
            raise NotImplementedError(
                f"Setting environment variables persistently"
                f" is not implemented for {system}"
            )