import os
from configparser import ConfigParser
from typing import NewType

Settings = NewType("Settings", ConfigParser)


def read_config(config_path: str) -> ConfigParser:
    assert os.path.isfile(config_path)
    config = ConfigParser()
    config.read(config_path)
    return config
