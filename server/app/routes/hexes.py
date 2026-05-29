from fastapi import APIRouter, Path, Query

from app.schemas import ErrorResponse, HexDetailResponse, HexListResponse
from app.services.hexes import get_hex_detail, query_hex_items

router = APIRouter(prefix="/api/hexes", tags=["强化符文数据"])


@router.get(
    "",
    summary="查询强化符文列表",
    description=(
        "查询金铲铲之战强化符文列表。可按关键字、等级、是否传说相关、英雄强化类型、"
        "关联羁绊 ID 或关联羁绊类型筛选。"
    ),
    response_description="强化符文列表查询结果",
    response_model=HexListResponse,
    responses={
        502: {
            "model": ErrorResponse,
            "description": "强化符文数据源不可用且本地没有可用缓存",
        },
    },
)
async def query_hexes(
    keyword: str | None = Query(
        default=None,
        description="搜索关键字。支持按强化符文 ID、名称、效果描述、关联羁绊 ID 或关联羁绊类型模糊匹配。",
        examples=["存心失利"],
    ),
    level: str | None = Query(
        default=None,
        description="强化符文等级或稀有度档位筛选。",
        examples=["2"],
    ),
    is_legend: int | None = Query(
        default=None,
        description="是否为传说相关符文标识筛选。",
        examples=[0],
    ),
    hero_enhancement_type: str | None = Query(
        default=None,
        alias="heroEnhancementType",
        description="英雄强化类型筛选，对应数据源字段 hero_enhancement_type。",
        examples=["0"],
    ),
    fetter_id: str | None = Query(
        default=None,
        alias="fetterId",
        description="关联羁绊 ID 筛选。",
        examples=["402"],
    ),
    fetter_type: str | None = Query(
        default=None,
        alias="fetterType",
        description="关联羁绊类型筛选。",
        examples=["0"],
    ),
) -> HexListResponse:
    return query_hex_items(
        keyword=keyword,
        level=level,
        is_legend=is_legend,
        hero_enhancement_type=hero_enhancement_type,
        fetter_id=fetter_id,
        fetter_type=fetter_type,
    )


@router.get(
    "/{hex_id}",
    summary="查询强化符文详情",
    description="根据强化符文 ID 查询单条强化符文资料。找不到时返回 404。",
    response_description="强化符文详情",
    response_model=HexDetailResponse,
    responses={
        404: {
            "model": ErrorResponse,
            "description": "未找到指定强化符文",
            "content": {
                "application/json": {
                    "example": {"detail": "Hex not found"},
                },
            },
        },
        502: {
            "model": ErrorResponse,
            "description": "强化符文数据源不可用且本地没有可用缓存",
        },
    },
)
async def get_hex(
    hex_id: str = Path(description="强化符文 ID。示例：1002。"),
) -> HexDetailResponse:
    return get_hex_detail(hex_id)

