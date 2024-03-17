
from http import HTTPStatus
from dataclasses import dataclass
import uvicorn
from asgiref.wsgi import WsgiToAsgi
from flask import Flask, Response, request

from telegram import Update
from telegram.ext import (
    Application,
    CallbackContext,
    ExtBot,
    ContextTypes,
)

import env
from .handlers.main import register_handlers


URL = "https://5cc3-46-63-28-245.ngrok-free.app"
PORT = 8000



@dataclass
class WebhookUpdate:
    user_id: int


class CustomContext(CallbackContext[ExtBot, dict, dict, dict]):
    @classmethod
    def from_update(
        cls,
        update: object,
        application: "Application",
    ) -> "CustomContext":
        if isinstance(update, WebhookUpdate):
            return cls(application=application, user_id=update.user_id)
        return super().from_update(update, application)


async def run_bot() -> None:
    context_types = ContextTypes(context=CustomContext)
    application = (Application.builder().token(env.Keys.TOKEN).updater(None).context_types(context_types).build())
    await application.bot.set_webhook(url=f"{URL}/telegram", allowed_updates=Update.ALL_TYPES)
    await register_handlers(application)
    flask_app = Flask(__name__)

    @flask_app.post("/telegram")  # type: ignore[misc]
    async def telegram() -> Response:
        await application.update_queue.put(Update.de_json(data=request.json, bot=application.bot))
        return Response(status=HTTPStatus.OK)

    @flask_app.route("/")
    async def index():
        return "Hello, World!"

    webserver = uvicorn.Server(
        config=uvicorn.Config(
            app=WsgiToAsgi(flask_app),
            port=PORT,
            use_colors=False,
            host="127.0.0.1",
        )
    )

    async with application:
        await application.start()
        await webserver.serve()
        await application.stop()







