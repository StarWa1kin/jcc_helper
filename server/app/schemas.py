from pydantic import BaseModel, ConfigDict, Field

from app.config import CHESS_SOURCE_URL, EQUIP_SOURCE_URL, GOD_SOURCE_URL, HEX_SOURCE_URL, TRAIT_SOURCE_URL


class ServiceMessageResponse(BaseModel):
    message: str = Field(description="服务运行提示信息", examples=["JCC Server is running"])


class HealthResponse(BaseModel):
    status: str = Field(description="服务健康状态", examples=["ok"])


class ErrorResponse(BaseModel):
    detail: str = Field(description="错误详情", examples=["Hero not found"])


class HeroMetaResponse(BaseModel):
    version: str = Field(description="数据源版本号", examples=["17.17.3"])
    season: str = Field(description="赛季标识", examples=["S18"])
    setId: str = Field(description="玩法或数据集合 ID", examples=["17"])
    time: str = Field(description="数据源更新时间", examples=["2026-05-21 12:00:00"])
    sourceUrl: str = Field(description="英雄数据来源地址", examples=[CHESS_SOURCE_URL])


class HeroCacheResponse(BaseModel):
    ttlSeconds: int = Field(description="缓存有效期，单位为秒", examples=[43200])
    fetchedAt: int = Field(description="本次缓存拉取时间戳，单位为秒", examples=[1779379200])


class HeroPayload(BaseModel):
    model_config = ConfigDict(
        extra="allow",
        populate_by_name=True,
        json_schema_extra={
            "description": "英雄原始资料。文档列出常用字段，其他来源字段会原样透传。",
            "example": {
                "id": "11450",
                "name": "亚索",
                "price": "1",
                "species": "1|3",
                "class": "2",
                "skillName": "斩钢闪",
                "showHeroTag": "1",
                "heroPaint": "Yasuo",
                "tftHeroId": "TFT18_Yasuo",
            },
        },
    )

    id: str | None = Field(default=None, description="英雄 ID", examples=["11450"])
    name: str | None = Field(default=None, description="英雄名称", examples=["亚索"])
    price: str | None = Field(default=None, description="英雄费用", examples=["1"])
    species: str | None = Field(default=None, description="羁绊 ID，多个值通常使用竖线分隔", examples=["1|3"])
    hero_class: str | None = Field(default=None, alias="class", description="职业 ID，多个值通常使用竖线分隔", examples=["2"])
    skillName: str | None = Field(default=None, description="技能名称", examples=["斩钢闪"])
    showHeroTag: str | None = Field(default=None, description="是否可展示。1 表示可展示", examples=["1"])
    heroPaint: str | None = Field(default=None, description="英雄皮肤或资源标识", examples=["Yasuo"])
    tftHeroId: str | None = Field(default=None, description="TFT 英雄 ID", examples=["TFT18_Yasuo"])


class HeroListResponse(BaseModel):
    meta: HeroMetaResponse = Field(description="数据源元信息")
    cache: HeroCacheResponse = Field(description="服务端缓存信息")
    total: int = Field(description="当前筛选条件命中的英雄总数", examples=[58])
    items: list[HeroPayload] = Field(description="英雄列表")


class HeroDetailResponse(BaseModel):
    hero: HeroPayload = Field(description="英雄详情")


class TraitMetaResponse(BaseModel):
    version: str = Field(description="数据源版本号", examples=["17.17.3"])
    season: str = Field(description="赛季标识", examples=["S18"])
    setId: str = Field(description="玩法或数据集合 ID", examples=["17"])
    time: str = Field(description="数据源更新时间", examples=["2026-05-21 10:16:44"])
    sourceUrl: str = Field(description="羁绊数据来源地址", examples=[TRAIT_SOURCE_URL])


class TraitPayload(BaseModel):
    model_config = ConfigDict(
        extra="allow",
        json_schema_extra={
            "description": "羁绊等级效果原始资料。文档列出常用字段，其他来源字段会原样透传。",
            "example": {
                "id": 83100101,
                "checkId": "402",
                "name": "木灵族",
                "type": 0,
                "color": "1",
                "level": 1,
                "maxLevel": "4",
                "num": "3",
                "numList": "3|5|7|10",
                "values": "3|5|7|10",
                "picture": "https://game.gtimg.cn/images/lol/act/jkzlk/mode17s18/trait/s17_trait_icon_astronaut.png",
                "prefix": "【木灵族】吸引木灵，木灵会以木灵的方式强化【木灵族】的技能。",
                "desc2": "(3)2，100【生命上限】",
                "realDesc": "(3)2，100【生命上限】",
                "setid": "17",
                "mapID": "3",
            },
        },
    )

    id: int | str | None = Field(default=None, description="羁绊效果 ID。每个羁绊的每个等级对应一条记录", examples=[83100101])
    checkId: str | None = Field(default=None, description="羁绊组 ID。同一羁绊不同等级通常拥有相同 checkId", examples=["402"])
    name: str | None = Field(default=None, description="羁绊名称", examples=["木灵族"])
    type: int | str | None = Field(default=None, description="羁绊类型", examples=[0])
    color: str | None = Field(default=None, description="羁绊等级颜色或档位标识", examples=["1"])
    level: int | str | None = Field(default=None, description="当前羁绊等级", examples=[1])
    maxLevel: str | None = Field(default=None, description="羁绊最大等级", examples=["4"])
    num: str | None = Field(default=None, description="激活当前等级所需数量", examples=["3"])
    numList: str | None = Field(default=None, description="所有可激活档位，多个值通常使用竖线分隔", examples=["3|5|7|10"])
    values: str | None = Field(default=None, description="效果数值列表，多个值通常使用竖线分隔", examples=["3|5|7|10"])
    picture: str | None = Field(default=None, description="羁绊图标地址")
    prefix: str | None = Field(default=None, description="羁绊基础效果描述")
    desc: str | None = Field(default=None, description="包含占位符的完整效果描述")
    desc2: str | None = Field(default=None, description="面向展示的分档效果描述")
    realDesc: str | None = Field(default=None, description="当前等级对应的实际效果描述")
    setid: str | None = Field(default=None, description="数据集合 ID", examples=["17"])
    mapID: str | None = Field(default=None, description="地图或模式 ID", examples=["3"])


class TraitListResponse(BaseModel):
    meta: TraitMetaResponse = Field(description="数据源元信息")
    cache: HeroCacheResponse = Field(description="服务端缓存信息")
    total: int = Field(description="当前筛选条件命中的羁绊效果总数", examples=[83])
    items: list[TraitPayload] = Field(description="羁绊效果列表")


class TraitDetailResponse(BaseModel):
    trait: TraitPayload = Field(description="羁绊效果详情")


class HexMetaResponse(BaseModel):
    version: str = Field(description="数据源版本号", examples=["17.17.3"])
    season: str = Field(description="赛季标识", examples=["S18"])
    setId: str = Field(description="玩法或数据集合 ID", examples=["17"])
    time: str = Field(description="数据源更新时间", examples=["2026-05-21 10:16:44"])
    sourceUrl: str = Field(description="强化符文数据来源地址", examples=[HEX_SOURCE_URL])


class HexPayload(BaseModel):
    model_config = ConfigDict(
        extra="allow",
        json_schema_extra={
            "description": "强化符文原始资料。文档列出常用字段，其他来源字段会原样透传。",
            "example": {
                "id": "1002",
                "name": "存心失利",
                "desc": "在输掉你的战斗环节之后，获得2金币和一次免费的商店刷新。",
                "icon": "https://game.gtimg.cn/images/lol/act/jkzlk/gamedata/hex/calculatedloss2.png",
                "level": "2",
                "is_legend": 0,
                "hero_enhancement_type": "0",
                "fetterId": "",
                "fetterType": "0",
            },
        },
    )

    id: str | None = Field(default=None, description="强化符文 ID", examples=["1002"])
    name: str | None = Field(default=None, description="强化符文名称", examples=["存心失利"])
    desc: str | None = Field(default=None, description="强化符文效果描述")
    icon: str | None = Field(default=None, description="强化符文图标地址")
    level: str | None = Field(default=None, description="强化符文等级或稀有度档位", examples=["2"])
    is_legend: int | str | None = Field(default=None, description="是否为传说相关符文标识", examples=[0])
    hero_enhancement_type: str | None = Field(default=None, description="英雄强化类型标识", examples=["0"])
    fetterId: str | None = Field(default=None, description="关联羁绊 ID，没有关联时通常为空", examples=[""])
    fetterType: str | None = Field(default=None, description="关联羁绊类型标识", examples=["0"])


class HexListResponse(BaseModel):
    meta: HexMetaResponse = Field(description="数据源元信息")
    cache: HeroCacheResponse = Field(description="服务端缓存信息")
    total: int = Field(description="当前筛选条件命中的强化符文总数", examples=[279])
    items: list[HexPayload] = Field(description="强化符文列表")


class HexDetailResponse(BaseModel):
    hex: HexPayload = Field(description="强化符文详情")


class GodMetaResponse(BaseModel):
    version: str = Field(description="数据源版本号", examples=["17.17.3"])
    season: str = Field(description="赛季标识", examples=["S18"])
    setId: str = Field(description="玩法或数据集合 ID", examples=["17"])
    time: str = Field(description="数据源更新时间", examples=["2026-05-21 10:16:44"])
    sourceUrl: str = Field(description="神明数据来源地址", examples=[GOD_SOURCE_URL])


class GodWishPayload(BaseModel):
    model_config = ConfigDict(extra="allow")

    id: int | str | None = Field(default=None, description="神明奖励或愿望 ID", examples=[1702010])
    name: str | None = Field(default=None, description="奖励或愿望名称", examples=["财富探险"])
    desc: str | None = Field(default=None, description="奖励或愿望效果描述")
    icon: str | None = Field(default=None, description="奖励或愿望图标地址")
    dragon: int | str | None = Field(default=None, description="是否为神明特殊奖励标识", examples=[0])
    type: str | None = Field(default=None, description="奖励类型标识，多个值通常使用竖线分隔", examples=["1|2"])


class GodStagePayload(BaseModel):
    model_config = ConfigDict(extra="allow")

    num: int | str | None = Field(default=None, description="阶段编号或触发阶段", examples=[2])
    wishes: list[GodWishPayload] = Field(default_factory=list, description="当前阶段可选奖励或愿望列表")


class GodPayload(BaseModel):
    model_config = ConfigDict(
        extra="allow",
        json_schema_extra={
            "description": "神明原始资料。包含神明基础信息以及各阶段奖励/愿望数据。",
            "example": {
                "godId": 2,
                "godName": "奥瑞利安·索尔 造物之神",
                "tex": "https://game.gtimg.cn/images/lol/act/jkzlk/mode17s18/godreward/tft17_god_aurelionsol_neutral_splash.png",
                "godIcon": "",
                "godTips": "奥瑞利安·索尔提供有回报的探险",
                "stages": [
                    {
                        "num": 2,
                        "wishes": [
                            {
                                "id": 1702010,
                                "name": "财富探险",
                                "desc": "当你积攒到50金币时，获得一个基础装备锻造器和4金币。",
                                "icon": "https://game.gtimg.cn/images/lol/act/jkzlk/mode17s18/godreward/tft17_benefit_aurelionsol_delayedgold_stage2_icon.png",
                                "dragon": 0,
                                "type": "1|2",
                            }
                        ],
                    }
                ],
            },
        },
    )

    godId: int | str | None = Field(default=None, description="神明 ID", examples=[2])
    godName: str | None = Field(default=None, description="神明名称", examples=["奥瑞利安·索尔 造物之神"])
    tex: str | None = Field(default=None, description="神明立绘或背景图地址")
    godIcon: str | None = Field(default=None, description="神明图标地址")
    godTips: str | None = Field(default=None, description="神明玩法提示或简介")
    stages: list[GodStagePayload] = Field(default_factory=list, description="神明各阶段奖励或愿望配置")


class GodListResponse(BaseModel):
    meta: GodMetaResponse = Field(description="数据源元信息")
    cache: HeroCacheResponse = Field(description="服务端缓存信息")
    total: int = Field(description="当前筛选条件命中的神明总数", examples=[9])
    items: list[GodPayload] = Field(description="神明列表")


class GodDetailResponse(BaseModel):
    god: GodPayload = Field(description="神明详情")


class EquipMetaResponse(BaseModel):
    version: str = Field(description="数据源版本号", examples=["17.17.3"])
    season: str = Field(description="赛季标识", examples=["S18"])
    setId: str = Field(description="玩法或数据集合 ID", examples=["17"])
    time: str = Field(description="数据源更新时间", examples=["2026-05-21 10:16:44"])
    sourceUrl: str = Field(description="装备数据来源地址", examples=[EQUIP_SOURCE_URL])


class EquipPayload(BaseModel):
    model_config = ConfigDict(
        extra="allow",
        json_schema_extra={
            "description": "装备原始资料。文档列出常用字段，其他来源字段会原样透传。",
            "example": {
                "id": "1001",
                "name": "暴风之剑",
                "type": "基础装备",
                "basicDesc": "+10物理加成",
                "desc": "",
                "picture": "https://game.gtimg.cn/images/lol/act/jkzlk/gamedata/equip/1001.png",
                "icon": "1001",
                "synthesis1": "0",
                "synthesis2": "0",
                "fetterID": "",
                "EffectType": "0",
                "tftEquipId": "0",
                "setID": "17",
                "mapID": "2",
                "planID": "17",
                "sort": "0",
            },
        },
    )

    id: str | None = Field(default=None, description="装备 ID", examples=["1001"])
    name: str | None = Field(default=None, description="装备名称", examples=["暴风之剑"])
    type: str | None = Field(default=None, description="装备类型，例如基础装备、成装、纹章等", examples=["基础装备"])
    basicDesc: str | None = Field(default=None, description="装备基础属性描述", examples=["+10物理加成"])
    desc: str | None = Field(default=None, description="装备效果描述")
    picture: str | None = Field(default=None, description="装备图片地址")
    icon: str | None = Field(default=None, description="装备图标 ID 或资源标识", examples=["1001"])
    synthesis1: str | None = Field(default=None, description="合成材料 1 的装备 ID。0 通常表示不可由材料合成", examples=["0"])
    synthesis2: str | None = Field(default=None, description="合成材料 2 的装备 ID。0 通常表示不可由材料合成", examples=["0"])
    fetterID: str | None = Field(default=None, description="关联羁绊 ID，没有关联时通常为空", examples=[""])
    EffectType: str | None = Field(default=None, description="装备效果类型标识", examples=["0"])
    tftEquipId: str | None = Field(default=None, description="TFT 装备 ID", examples=["0"])
    setID: str | None = Field(default=None, description="数据集合 ID", examples=["17"])
    mapID: str | None = Field(default=None, description="地图或模式 ID", examples=["2"])
    planID: str | None = Field(default=None, description="玩法方案 ID", examples=["17"])
    sort: str | None = Field(default=None, description="排序值", examples=["0"])


class EquipListResponse(BaseModel):
    meta: EquipMetaResponse = Field(description="数据源元信息")
    cache: HeroCacheResponse = Field(description="服务端缓存信息")
    total: int = Field(description="当前筛选条件命中的装备总数", examples=[278])
    items: list[EquipPayload] = Field(description="装备列表")


class EquipDetailResponse(BaseModel):
    equip: EquipPayload = Field(description="装备详情")
