from routers.admin.base import router as admin_router
from routers.admin.moderMng import router as admin_moder_mng_router
from routers.moderator.ban import router as moder_ban_router
from routers.user.message_logger import router as user_message_logger

routers = [
    admin_router,
    admin_moder_mng_router,
    moder_ban_router,
    user_message_logger,
]