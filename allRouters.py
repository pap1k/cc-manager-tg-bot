from routers.admin.base import router as admin_router
from routers.admin.moderMng import router as admin_moder_mng_router
from routers.moderator.ban import router as moder_ban_router
from routers.user.message_logger import router as user_message_logger
from routers.admin.test_cmd import router as test_commands_router
from routers.moderator.parser import router as moder_parser_router
from routers.moderator.banlog import router as moder_banlog_router

routers = [
    admin_router,
    admin_moder_mng_router,
    moder_ban_router,
    user_message_logger,
    test_commands_router,
    moder_parser_router,
    moder_banlog_router,
]