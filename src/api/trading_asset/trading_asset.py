from uuid import uuid4

from fastapi import HTTPException, Request
from fastapi.responses import JSONResponse

from api.injector import inject
from api.trading_asset.router import trading_asset_router
from base.command_bus import CommandBus
from cache.ports.repositories import TradingAssetCache
from trading_assets.commands import AddTradingAsset, UpdateTradingAsset
from trading_assets.ports.uow import TradingAssetsUnitOfWork


@trading_asset_router.get("/v1/trading_asset/{id}")
async def get_trading_asset(
    request: Request, cache: TradingAssetCache = inject(TradingAssetCache)
) -> JSONResponse:
    trading_asset_id = int(request.path_params["id"])
    trading_asset = cache.get(trading_asset_id)
    if not trading_asset:
        raise HTTPException(status_code=404)
    return JSONResponse(content=trading_asset.dict())


@trading_asset_router.get("/v1/trading_asset/command/{id}")
async def get_trading_asset_request_info(
    request: Request, uow: TradingAssetsUnitOfWork = inject(TradingAssetsUnitOfWork)
) -> JSONResponse:
    command_id = request.path_params["id"]
    with uow as context:
        command_log = context.command_log.get(command_id)
    return JSONResponse(content=command_log.dict())


@trading_asset_router.post("/v1/trading_asset/")
async def add_trading_asset(
    request: Request, command_bus: CommandBus = inject(CommandBus)
) -> JSONResponse:
    # NOTE `request.json()` does not accept request without body. Empty json is enough.
    payload = await request.json()
    command_id = str(uuid4())
    command = AddTradingAsset(
        id=command_id,
        trading_asset_id=payload["id"],
        full_name=payload["full_name"],
        iso_code=payload["iso_code"],
        tags=list(set(payload["tags"])),
    )

    command_bus.handle(command)

    return JSONResponse(status_code=201, content={"command_id": command_id})


@trading_asset_router.put("/v1/trading_asset/")
async def update_trading_asset(
    request: Request, command_bus: CommandBus = inject(CommandBus)
) -> JSONResponse:
    payload = await request.json()
    command_id = str(uuid4())
    command = UpdateTradingAsset(
        id=command_id,
        trading_asset_id=payload["id"],
        full_name=payload["full_name"],
        iso_code=payload["iso_code"],
        tags=list(set(payload["tags"])),
    )

    command_bus.handle(command)

    return JSONResponse(status_code=201, content={"command_id": command_id})
