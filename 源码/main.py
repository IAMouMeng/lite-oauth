"""
 * 初始化程序
 * Author: 孙洪达
 * Time: 2023/11/12
 * Mail: iamoumeng@aliyun.com
"""

from sanic import Sanic
from sanic_jinja2 import SanicJinja2

from app.config import config
from app.api import *

from app.models import Engine
from app.utils.error import CustomErrorHandler

from contextvars import ContextVar
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.asyncio import AsyncSession

app = Sanic(__name__, error_handler=CustomErrorHandler())

app.static("/static", "app/static")

app.config.update(config.__dict__)
app.config.jinja = SanicJinja2(app,pkg_name="app",pkg_path="views")

_sessionmaker = sessionmaker(Engine, AsyncSession, expire_on_commit=False)

_base_model_session_ctx = ContextVar("session")


@app.middleware("request")
async def inject_session(request):
    request.ctx.session = _sessionmaker()
    request.ctx.session_ctx_token = _base_model_session_ctx.set(
        request.ctx.session)


@app.middleware("response")
async def close_session(request, response):
    if hasattr(request.ctx, "session_ctx_token"):
        _base_model_session_ctx.reset(request.ctx.session_ctx_token)
        await request.ctx.session.close()

app.blueprint(root)

if __name__ == '__main__':
    app.run(host="127.0.0.1", port=7800, debug=True, auto_reload=True)