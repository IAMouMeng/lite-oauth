"""
 * API 初始化
 * Author: 孙洪达
 * Time: 2023/11/12
 * Mail: iamoumeng@aliyun.com
"""

from .oauth import oauth
from .user import user
from sanic.blueprints import Blueprint

blueprints = [
    oauth,
    user
]

root = Blueprint.group(*blueprints, url_prefix="/")
