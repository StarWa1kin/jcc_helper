from fastapi import APIRouter, Path, Query

from app.schemas import EquipDetailResponse, EquipListResponse, ErrorResponse
from app.services.equips import get_equip_detail, query_equip_items

router = APIRouter(prefix="/api/equips", tags=["装备数据"])


@router.get(
    "",
    summary="查询装备列表",
    description=(
        "查询金铲铲之战装备列表。可按关键字、装备类型、合成材料、关联羁绊、"
        "效果类型或是否可合成筛选。"
    ),
    response_description="装备列表查询结果",
    response_model=EquipListResponse,
    responses={
        502: {
            "model": ErrorResponse,
            "description": "装备数据源不可用且本地没有可用缓存",
        },
    },
)
async def query_equips(
    keyword: str | None = Query(
        default=None,
        description="搜索关键字。支持按装备 ID、名称、类型、属性描述、效果描述、关联羁绊 ID 或 TFT 装备 ID 模糊匹配。",
        examples=["暴风之剑"],
    ),
    equip_type: str | None = Query(
        default=None,
        alias="type",
        description="装备类型筛选，支持模糊匹配，例如基础装备、成装。",
        examples=["基础装备"],
    ),
    material_id: str | None = Query(
        default=None,
        alias="materialId",
        description="合成材料装备 ID 筛选。只要 synthesis1 或 synthesis2 命中即返回。",
        examples=["1001"],
    ),
    fetter_id: str | None = Query(
        default=None,
        alias="fetterId",
        description="关联羁绊 ID 筛选。",
    ),
    effect_type: str | None = Query(
        default=None,
        alias="effectType",
        description="装备效果类型筛选，对应数据源字段 EffectType。",
        examples=["0"],
    ),
    composable: bool | None = Query(
        default=None,
        description="是否只查询可由两个材料合成的装备。true 表示仅可合成装备，false 表示仅不可合成装备。",
    ),
) -> EquipListResponse:
    return query_equip_items(
        keyword=keyword,
        equip_type=equip_type,
        material_id=material_id,
        fetter_id=fetter_id,
        effect_type=effect_type,
        composable=composable,
    )


@router.get(
    "/{equip_id}",
    summary="查询装备详情",
    description="根据装备 ID 查询单个装备资料。找不到时返回 404。",
    response_description="装备详情",
    response_model=EquipDetailResponse,
    responses={
        404: {
            "model": ErrorResponse,
            "description": "未找到指定装备",
            "content": {
                "application/json": {
                    "example": {"detail": "Equip not found"},
                },
            },
        },
        502: {
            "model": ErrorResponse,
            "description": "装备数据源不可用且本地没有可用缓存",
        },
    },
)
async def get_equip(
    equip_id: str = Path(description="装备 ID。示例：1001。"),
) -> EquipDetailResponse:
    return get_equip_detail(equip_id)

