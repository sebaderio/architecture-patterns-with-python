import json
import os

from injector import Injector
from redis import Redis

from base.module import BaseModule


def bootstrap(config_path: str) -> Injector:
    return Injector(
        modules=[
            BaseModule(config_path),
        ]
    )


def run_consumer(container: Injector, handler: callable = lambda event: print(event)):
    channel_name = os.environ["CHANNEL_NAME"]

    redis = container.get(Redis)
    consumer = redis.pubsub(ignore_subscribe_messages=True)
    consumer.subscribe(channel_name)

    for event in consumer.listen():
        event_dict = json.loads(event["data"].decode("utf-8"))
        handler(event_dict)


if __name__ == "__main__":
    config_path = os.environ["CONFIG_PATH"]
    container = bootstrap(config_path)
    run_consumer(container)
