"""
 * user 路由
 * Author: 孙洪达
 * Time: 2023/11/16
 * Mail: iamoumeng@aliyun.com
"""
import hmac
import requests

from sanic.blueprints import Blueprint

from app.utils import tools
from app.utils.response import response
from app.utils.request import AuthParam
from app.models.user_model import Action as UserAction
from app.models.log_model import Action as LogAction
from app.models.app_model import Action as AppAction
from app.models.ticket_model import Action as TicketAction


user = Blueprint(name="apiUser", url_prefix="/user")

# 用户登录
@user.route("/login", ["POST"])
@AuthParam("username","password","client_id","vertify")
async def userLogin(request):
    username = request.json["username"]
    password = request.json["password"]
    clientId = request.json["client_id"]
    vertify = request.json["vertify"]

    clientIp = tools.getClientIp(request=request)
    
    appInfo = await AppAction(request=request).Get(client_id=clientId)

    if not appInfo:
        return response.error("客户端不存在")

    vertify["captcha_id"] = request.app.config.GEETEST_ID.value
    
    vertify["sign_token"] = hmac.new(
        request.app.config.GEETEST_KEY.value.encode(),
        request.json["vertify"]["lot_number"].encode(),
        digestmod='SHA256'
    ).hexdigest()

    vertifyResult = requests.post(
        url=request.app.config.GEETEST_CAPTCHA_URL.value,
        params=vertify
    ).json()
    
    if vertifyResult["result"] != "success":
        await LogAction(request=request).Insert(
            0,
            f"【{appInfo.name}】 验证失败",
            request.json,
            clientIp
        )
        
        return response.error("验证失败，请重试")
    
    userInfo = await UserAction(request=request).Get(username=username)
    
    if not userInfo or userInfo.password != tools.strToMd5(password,userInfo.salt):
        await LogAction(request=request).Insert(
            0,
            f"【{appInfo.name}】 登录失败",
            request.json,
            vertifyResult["captcha_args"]["user_ip"] # 极验IP可信度更高
        )
        
        return response.error("用户名或密码错误")
    
    await LogAction(request=request).Insert(
        userInfo.id,f"【{appInfo.name}】 授权登录 {username}",
        request.json,vertifyResult["captcha_args"]["user_ip"]
    )
    
    await UserAction(request=request).UpdateLoginInfo(
        userInfo,
        vertifyResult["captcha_args"]["user_ip"]
    )

    ticket = tools.randomUuid()
    
    await TicketAction(request=request).Insert(
        userInfo.id,
        client_id=appInfo.client_id,
        ticket=ticket,
        ip=vertifyResult["captcha_args"]["user_ip"],
        expiry_second=request.app.config.TICKET_EXPIRY_SECOND.value
    )

    return response.succWithData({
        "ticket":ticket,
        "redirect_uri":appInfo.redirect_uri
    },"登录成功")
    
# 用户注册
@user.route("/register", ["POST"])
@AuthParam("username","password","client_id","vertify")
async def userReg(request):
    username = request.json["username"]
    password = request.json["password"]
    clientId = request.json["client_id"]
    vertify = request.json["vertify"]

    clientIp = tools.getClientIp(request=request)
    
    appInfo = await AppAction(request=request).Get(client_id=clientId)

    if not appInfo:
        return response.error("客户端不存在")

    vertify["captcha_id"] = request.app.config.GEETEST_ID.value
    
    vertify["sign_token"] = hmac.new(
        request.app.config.GEETEST_KEY.value.encode(),
        request.json["vertify"]["lot_number"].encode(),
        digestmod='SHA256'
    ).hexdigest()

    vertifyResult = requests.post(
        url=request.app.config.GEETEST_CAPTCHA_URL.value,
        params=vertify
    ).json()
    
    if vertifyResult["result"] != "success":
        await LogAction(request=request).Insert(
            0,
            "验证失败",
            request.json,
            clientIp
        )
        
        return response.error("验证失败，请重试")
    
    userInfo = await UserAction(request=request).Get(username=username)
    
    if userInfo:
        await LogAction(request=request).Insert(
            0,
            f"【{appInfo.name}】重复注册",
            request.json,
            vertifyResult["captcha_args"]["user_ip"] # 极验IP可信度更高
        )
        
        return response.error("用户名已存在")
    
    salt = tools.randomStr(4) # 生成盐值
    password = tools.strToMd5(password,salt)
    
    await UserAction(request=request).Insert(username=username,password=password,salt=salt)
    
    await LogAction(request=request).Insert(
        0,f"【{appInfo.name}】 用户注册  {username}",
        request.json,vertifyResult["captcha_args"]["user_ip"]
    )
    
    return response.success("注册成功")