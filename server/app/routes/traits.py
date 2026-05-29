from fastapi import APIRouter, Path, Query

from app.schemas import ErrorResponse, TraitDetailResponse, TraitListResponse
from app.services.traits import get_trait_detail, query_trait_items

router = APIRouter(prefix="/api/traits", tags=["羁绊数据"])


@router.get(
    "",
    summary="查询羁绊效果列表",
    description=(
        "查询金铲铲之战羁绊效果列表。每条记录代表某个羁绊在一个等级档位下的效果，"
        "可按关键字、羁绊名称、羁绊组 ID 或羁绊类型筛选。"
    ),
    response_description="羁绊效果列表查询结果",
    response_model=TraitListResponse,
    responses={
        502: {
            "model": ErrorResponse,
            "description": "羁绊数据源不可用且本地没有可用缓存",
        },
    },
)
async def query_traits(
    keyword: str | None = Query(
        default=None,
        description="搜索关键字。支持按羁绊效果 ID、羁绊组 ID、名称和效果描述模糊匹配。",
        examples=["木灵族"],
    ),
    name: str | None = Query(
        default=None,
        description="羁绊名称筛选，支持模糊匹配。",
        examples=["木灵族"],
    ),
    check_id: str | None = Query(
        default=None,
        alias="checkId",
        description="羁绊组 ID。同一羁绊的不同等级效果通常拥有相同 checkId。",
        examples=["402"],
    ),
    trait_type: int | None = Query(
        default=None,
        alias="type",
        description="羁绊类型筛选。",
        examples=[0],
    ),
) -> TraitListResponse:
    return query_trait_items(
        keyword=keyword,
        name=name,
        check_id=check_id,
        trait_type=trait_type,
    )


@router.get(
    "/{trait_id}",
    summary="查询羁绊效果详情",
    description="根据羁绊效果 ID 查询单条羁绊等级效果。找不到时返回 404。",
    response_description="羁绊效果详情",
    response_model=TraitDetailResponse,
    responses={
        404: {
            "model": ErrorResponse,
            "description": "未找到指定羁绊效果",
            "content": {
                "application/json": {
                    "example": {"detail": "Trait not found"},
                },
            },
        },
        502: {
            "model": ErrorResponse,
            "description": "羁绊数据源不可用且本地没有可用缓存",
        },
    },
)
async def get_trait(
    trait_id: str = Path(description="羁绊效果 ID。示例：83100101。"),
) -> TraitDetailResponse:
    return get_trait_detail(trait_id)

