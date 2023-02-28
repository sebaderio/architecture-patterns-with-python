from fastapi import FastAPI
from injector import Injector

from api.trading_asset import trading_asset_router


def create_app(container: Injector) -> FastAPI:
    app = FastAPI()
    app.state.injector = container

    app.get("/v1/ping")(lambda: "pong")
    app.include_router(trading_asset_router)

    return app
