from fastapi import APIRouter, Path, Query

from app.schemas import ErrorResponse, HeroDetailResponse, HeroListResponse
from app.services.heroes import get_hero_detail, query_hero_items

router = APIRouter(prefix="/api/heroes", tags=["英雄数据"])


@router.get(
    "",
    summary="查询英雄列表",
    description=(
        "按关键字、费用、羁绊和职业筛选英雄列表。默认只返回配置为可展示的英雄。"
        "响应中包含数据源版本信息、缓存信息、命中总数和英雄列表。"
    ),
    response_description="英雄列表查询结果",
    response_model=HeroListResponse,
    responses={
        502: {
            "model": ErrorResponse,
            "description": "英雄数据源不可用且本地没有可用缓存",
        },
    },
)
async def query_heroes(
    keyword: str | None = Query(
        default=None,
        description="搜索关键字。支持按英雄 ID、英雄名称、皮肤标识、技能名称或 TFT 英雄 ID 模糊匹配。",
        examples=["亚索"],
    ),
    price: int | None = Query(
        default=None,
        ge=0,
        description="英雄费用筛选。传入 1、2、3、4、5 等费用值时，只返回对应费用的英雄。",
        examples=[1],
    ),
    species: str | None = Query(
        default=None,
        description="羁绊 ID 筛选。英雄存在多个羁绊时，只要包含该 ID 即会命中。",
        examples=["1"],
    ),
    hero_class: str | None = Query(
        default=None,
        alias="class",
        description="职业 ID 筛选。请求参数名为 class，英雄存在多个职业时，只要包含该 ID 即会命中。",
        examples=["2"],
    ),
    show_only: bool = Query(
        default=True,
        description="是否只返回前端可展示英雄。true 表示仅返回 showHeroTag 为 1 的英雄；false 表示返回全部英雄。",
    ),
) -> HeroListResponse:
    return query_hero_items(
        keyword=keyword,
        price=price,
        species=species,
        hero_class=hero_class,
        show_only=show_only,
    )


@router.get(
    "/{hero_id}",
    summary="查询英雄详情",
    description="根据英雄 ID 查询单个英雄的完整原始资料。找不到英雄时返回 404。",
    response_description="英雄详情",
    response_model=HeroDetailResponse,
    responses={
        404: {
            "model": ErrorResponse,
            "description": "未找到指定英雄",
            "content": {
                "application/json": {
                    "example": {"detail": "Hero not found"},
                },
            },
        },
        502: {
            "model": ErrorResponse,
            "description": "英雄数据源不可用且本地没有可用缓存",
        },
    },
)
async def get_hero(
    hero_id: str = Path(description="英雄 ID。示例：11450。"),
) -> HeroDetailResponse:
    return get_hero_detail(hero_id)

