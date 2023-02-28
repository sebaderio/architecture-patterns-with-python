from typing import cast

from injector import inject
from sqlalchemy.orm import Session, scoped_session

from base.event_bus import EventBus
from trading_assets.ports import uow


@inject
class PostgresTradingAssetsUnitOfWork(uow.TradingAssetsUnitOfWork):
    def __init__(
        self, session: Session, context: uow.TradingAssetsContext, event_bus: EventBus
    ) -> None:
        self._session = cast(scoped_session, session)
        self._context = context
        self._event_bus = event_bus
        self._context.events = []
        self._transaction = None

    def __enter__(self) -> uow.TradingAssetsContext:
        if self._transaction:
            raise Exception("Transaction already exists")
        self._transaction = self._session()
        return self._context

    def _commit(self) -> None:
        self._transaction.commit()
        self._transaction = None
        # Events should be handled only after commit.
        self._handle_events()

    def _rollback(self) -> None:
        self._transaction.rollback()
        self._transaction = None
        self._drop_events()

    def _handle_events(self) -> None:
        # Current implementation assumes that listeners do not need the session / uow.
        while len(self._context.events):
            event = self._context.events.pop(0)
            self._event_bus.handle(event)

    def _drop_events(self) -> None:
        self._context.events = []
