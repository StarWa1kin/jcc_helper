from fastapi import APIRouter

from app.schemas import HealthResponse, ServiceMessageResponse

router = APIRouter(tags=["基础接口"])


@router.get(
    "/",
    summary="服务根路径",
    description="用于确认服务已启动并可以正常响应请求。",
    response_description="服务运行提示信息",
    response_model=ServiceMessageResponse,
)
async def root() -> ServiceMessageResponse:
    return {"message": "JCC Server is running"}


@router.get(
    "/health",
    summary="健康检查",
    description="返回服务健康状态，可用于部署平台、网关或监控系统探活。",
    response_description="服务健康状态",
    response_model=HealthResponse,
)
async def health() -> HealthResponse:
    return {"status": "ok"}

