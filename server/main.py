import sys
from pathlib import Path

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

SERVER_DIR = Path(__file__).resolve().parent
if str(SERVER_DIR) not in sys.path:
    sys.path.insert(0, str(SERVER_DIR))

from app.openapi import openapi_tags
from app.routes import api_router

app = FastAPI(
    title="JCC Server",
    summary="金铲铲之战资料服务",
    description=(
        "提供金铲铲之战英雄资料查询接口。英雄数据会从官方静态资源拉取，"
        "并在本地缓存以提升响应速度。"
    ),
    version="0.1.0",
    openapi_tags=openapi_tags,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router)
