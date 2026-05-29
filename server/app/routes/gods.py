from fastapi import APIRouter, Path, Query

from app.schemas import ErrorResponse, GodDetailResponse, GodListResponse
from app.services.gods import get_god_detail, query_god_items

router = APIRouter(prefix="/api/gods", tags=["神明数据"])


@router.get(
    "",
    summary="查询神明列表",
    description=(
        "查询金铲铲之战神明列表。响应包含神明基础信息，以及各阶段可选奖励或愿望。"
        "可按关键字、神明名称、奖励名称或阶段筛选。"
    ),
    response_description="神明列表查询结果",
    response_model=GodListResponse,
    responses={
        502: {
            "model": ErrorResponse,
            "description": "神明数据源不可用且本地没有可用缓存",
        },
    },
)
async def query_gods(
    keyword: str | None = Query(
        default=None,
        description="搜索关键字。支持按神明 ID、神明名称、神明提示、奖励 ID、奖励名称和奖励描述模糊匹配。",
        examples=["奥瑞利安"],
    ),
    god_name: str | None = Query(
        default=None,
        alias="godName",
        description="神明名称筛选，支持模糊匹配。",
        examples=["奥瑞利安"],
    ),
    wish_name: str | None = Query(
        default=None,
        alias="wishName",
        description="奖励或愿望名称筛选，支持模糊匹配。",
        examples=["财富探险"],
    ),
    stage: int | None = Query(
        default=None,
        description="阶段编号筛选，例如 2、3、4。",
        examples=[2],
    ),
) -> GodListResponse:
    return query_god_items(
        keyword=keyword,
        god_name=god_name,
        wish_name=wish_name,
        stage=stage,
    )


@router.get(
    "/{god_id}",
    summary="查询神明详情",
    description="根据神明 ID 查询单个神明资料。找不到时返回 404。",
    response_description="神明详情",
    response_model=GodDetailResponse,
    responses={
        404: {
            "model": ErrorResponse,
            "description": "未找到指定神明",
            "content": {
                "application/json": {
                    "example": {"detail": "God not found"},
                },
            },
        },
        502: {
            "model": ErrorResponse,
            "description": "神明数据源不可用且本地没有可用缓存",
        },
    },
)
async def get_god(
    god_id: str = Path(description="神明 ID。示例：2。"),
) -> GodDetailResponse:
    return get_god_detail(god_id)

