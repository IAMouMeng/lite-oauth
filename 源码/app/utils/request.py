"""
 * 参数验证
 * Author: 孙洪达
 * Time: 2023/11/12
 * Mail: iamoumeng@aliyun.com
"""

from functools import wraps
from app.utils.response import response


def AuthParam(*keys):
    def wrapper(func):
        @wraps(func)
        async def AuthParam(request=None, *args, **kwargs):
            if request.method == 'POST' and request.json:
                for i in keys:
                    if i not in request.json.keys():
                        return response.error("参数缺失",500)
                    elif not request.json[i]:
                        return response.error("请确保必填项不为空",400)
                    
            elif request.method == 'GET' and request.args:
                for i in keys:
                    if i not in request.args.keys():
                        return response.error("参数缺失",500)
            else:
                return response.error("参数缺失",500)
            return await func(request, *args, **kwargs)

        return AuthParam

    return wrapper
