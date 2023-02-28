import os

from api.app import create_app
from base import bootstrap


def app_factory():
    config_path = os.environ["CONFIG_PATH"]
    container = bootstrap(config_path)
    return create_app(container)
