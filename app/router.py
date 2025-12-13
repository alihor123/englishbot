from aiogram import Dispatcher, Router

from app.apps.user.router import router as user_router
from app.apps.progress.router import router as progress_router
from app.apps.tasks.router import router as task_router


router = Router()


def use_routes(dp: Dispatcher) -> None:
    router.include_router(user_router)
    router.include_router(progress_router)
    router.include_router(task_router)
    dp.include_router(router)
