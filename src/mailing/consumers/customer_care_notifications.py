import os
from dataclasses import dataclass

from base import bootstrap
from base.consumer import run_consumer
from mailing.ports.notifications import EmailNotification


@dataclass
class CustomerCareNotificationsConsumer:
    DESTINATION_EMAIL_ADDRESS = "customer.care.notifications@archipatterns.com"
    _notifications: EmailNotification

    def __call__(self, event: dict):
        event_name = event["name"]
        event_data = event["data"]
        event_data.pop("command_id", None)
        message = f"{event_name} -> {event_data}"
        self._notifications.send(self.DESTINATION_EMAIL_ADDRESS, message)


if __name__ == "__main__":
    config_path = os.environ["CONFIG_PATH"]
    container = bootstrap(config_path)
    notifcations = container.get(EmailNotification)
    run_consumer(container, CustomerCareNotificationsConsumer(notifcations))
