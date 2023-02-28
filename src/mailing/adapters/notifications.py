from smtplib import SMTP

from injector import inject

from mailing.ports import notifications


@inject
class SMTPEmailNotification(notifications.EmailNotification):
    def __init__(self, server: SMTP) -> None:
        self._server = server

    def send(self, destination: str, message: str):
        self._server.sendmail(
            from_addr="notify@archipatterns.com",
            to_addrs=[destination],
            msg=message,
        )
