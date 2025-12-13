from apscheduler.schedulers.asyncio import AsyncIOScheduler  # type: ignore
from apscheduler.triggers.cron import CronTrigger  # type: ignore
from sqlalchemy.ext.asyncio import AsyncSession
import httpx

from app.apps.user.service import UserService
from app.db import transactional
from app.settings import TelegramSettings


scheduler = AsyncIOScheduler()


@scheduler.scheduled_job(trigger=CronTrigger(minute="*/10"))  # type: ignore
@transactional
async def notify_inactive_users(session: AsyncSession) -> None:
    settings = TelegramSettings()  # type: ignore
    user_service = UserService(session=session)
    inactive_users = await user_service.list_inactive()
    for user in inactive_users:
        async with httpx.AsyncClient() as client:
            await client.post(
                f"https://api.telegram.org/bot{settings.token}/sendMessage",
                params={"chat_id": user.id, "text": "Кажется пора позаниматься"},
            )
        await user_service.update_activity(user.id)
