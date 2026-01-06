"""
设置管理路由
"""
import os
from fastapi import APIRouter, Depends
from pydantic import BaseModel
from typing import Optional
from src.api.dependencies import get_current_user
from src.infrastructure.config.env_manager import env_manager
from src.infrastructure.config.settings import ai_settings, notification_settings, scraper_settings


router = APIRouter(prefix="/api/settings", tags=["settings"])


class NotificationSettingsModel(BaseModel):
    """通知设置模型"""
    NTFY_TOPIC_URL: Optional[str] = None
    BARK_URL: Optional[str] = None
    TELEGRAM_BOT_TOKEN: Optional[str] = None
    TELEGRAM_CHAT_ID: Optional[str] = None


class AISettingsModel(BaseModel):
    """AI设置模型"""
    OPENAI_API_KEY: Optional[str] = None
    OPENAI_BASE_URL: Optional[str] = None
    OPENAI_MODEL_NAME: Optional[str] = None
    SKIP_AI_ANALYSIS: Optional[bool] = None
    PROXY_URL: Optional[str] = None


@router.get("/notifications")
async def get_notification_settings(username: str = Depends(get_current_user)):
    """获取通知设置"""
    return {
        "NTFY_TOPIC_URL": env_manager.get_value("NTFY_TOPIC_URL", ""),
        "BARK_URL": env_manager.get_value("BARK_URL", ""),
        "TELEGRAM_BOT_TOKEN": env_manager.get_value("TELEGRAM_BOT_TOKEN", ""),
        "TELEGRAM_CHAT_ID": env_manager.get_value("TELEGRAM_CHAT_ID", "")
    }


@router.put("/notifications")
async def update_notification_settings(
    settings: NotificationSettingsModel,
    username: str = Depends(get_current_user)
):
    """更新通知设置"""
    updates = settings.dict(exclude_none=True)
    success = env_manager.update_values(updates)
    if success:
        return {"message": "通知设置已成功更新"}
    return {"message": "更新通知设置失败"}


@router.get("/status")
async def get_system_status(username: str = Depends(get_current_user)):
    """获取系统状态"""
    state_file = "xianyu_state.json"
    login_state_exists = os.path.exists(state_file)

    # 检查 .env 文件
    env_file_exists = os.path.exists(".env")

    # 检查关键环境变量是否设置
    openai_api_key = env_manager.get_value("OPENAI_API_KEY", "")
    openai_base_url = env_manager.get_value("OPENAI_BASE_URL", "")
    openai_model_name = env_manager.get_value("OPENAI_MODEL_NAME", "")
    ntfy_topic_url = env_manager.get_value("NTFY_TOPIC_URL", "")

    return {
        "ai_configured": ai_settings.is_configured(),
        "notification_configured": notification_settings.has_any_notification_enabled(),
        "headless_mode": scraper_settings.run_headless,
        "running_in_docker": scraper_settings.running_in_docker,
        "login_state_file": {
            "exists": login_state_exists,
            "path": state_file
        },
        "env_file": {
            "exists": env_file_exists,
            "openai_api_key_set": bool(openai_api_key),
            "openai_base_url_set": bool(openai_base_url),
            "openai_model_name_set": bool(openai_model_name),
            "ntfy_topic_url_set": bool(ntfy_topic_url)
        }
    }


class AISettingsModel(BaseModel):
    """AI设置模型"""
    OPENAI_API_KEY: Optional[str] = None
    OPENAI_BASE_URL: Optional[str] = None
    OPENAI_MODEL_NAME: Optional[str] = None
    SKIP_AI_ANALYSIS: Optional[bool] = None


@router.get("/ai")
async def get_ai_settings(username: str = Depends(get_current_user)):
    """获取AI设置"""
    return {
        "OPENAI_API_KEY": env_manager.get_value("OPENAI_API_KEY", ""),
        "OPENAI_BASE_URL": env_manager.get_value("OPENAI_BASE_URL", ""),
        "OPENAI_MODEL_NAME": env_manager.get_value("OPENAI_MODEL_NAME", ""),
        "SKIP_AI_ANALYSIS": env_manager.get_value("SKIP_AI_ANALYSIS", "false").lower() == "true"
    }


@router.put("/ai")
async def update_ai_settings(
    settings: AISettingsModel,
    username: str = Depends(get_current_user)
):
    """更新AI设置"""
    updates = {}
    if settings.OPENAI_API_KEY is not None:
        updates["OPENAI_API_KEY"] = settings.OPENAI_API_KEY
    if settings.OPENAI_BASE_URL is not None:
        updates["OPENAI_BASE_URL"] = settings.OPENAI_BASE_URL
    if settings.OPENAI_MODEL_NAME is not None:
        updates["OPENAI_MODEL_NAME"] = settings.OPENAI_MODEL_NAME
    if settings.SKIP_AI_ANALYSIS is not None:
        updates["SKIP_AI_ANALYSIS"] = str(settings.SKIP_AI_ANALYSIS).lower()

    success = env_manager.update_values(updates)
    if success:
        return {"message": "AI设置已成功更新"}
    return {"message": "更新AI设置失败"}


@router.post("/ai/test")
async def test_ai_settings(
    settings: dict,
    username: str = Depends(get_current_user)
):
    """测试AI模型设置是否有效"""
    try:
        from openai import OpenAI
        import httpx
        
        # 优先使用前端传入的配置，如果缺少则回退到环境变量
        api_key = (settings.get("OPENAI_API_KEY") or env_manager.get_value("OPENAI_API_KEY", "")).strip('"')
        base_url = (settings.get("OPENAI_BASE_URL") or env_manager.get_value("OPENAI_BASE_URL", "")).strip('"')
        model_name = (settings.get("OPENAI_MODEL_NAME") or env_manager.get_value("OPENAI_MODEL_NAME", "")).strip('"')
        # 注意：前端可能不传 PROXY_URL，此时应检查环境变量
        proxy_url = (settings.get("PROXY_URL") or env_manager.get_value("PROXY_URL", "")).strip('"')

        print(f"AI测试 - BASE_URL: {base_url}, MODEL: {model_name}, PROXY: {proxy_url}")

        # 创建OpenAI客户端
        client_params = {
            "api_key": api_key,
            "base_url": base_url,
            "timeout": httpx.Timeout(30.0),
        }

        # 如果有代理设置
        if proxy_url:
            # 必须设置 verify=False 以支持本地自签名证书代理
            client_params["http_client"] = httpx.Client(
                proxy=proxy_url,
                verify=False
            )

        client = OpenAI(**client_params)

        # 测试连接
        response = client.chat.completions.create(
            model=model_name,
            messages=[
                {"role": "user", "content": "Hello"}
            ],
            max_tokens=10
        )

        return {
            "success": True,
            "message": "AI模型连接测试成功！",
            "response": response.choices[0].message.content if response.choices else "No response"
        }
    except Exception as e:
        print(f"AI测试失败详情: {e}")
        import traceback
        traceback.print_exc()
        return {
            "success": False,
            "message": f"AI模型连接测试失败: {str(e)}"
        }
