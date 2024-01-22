"""
 * oauth 路由
 * Author: 孙洪达
 * Time: 2023/11/25
 * Mail: iamoumeng@aliyun.com
"""
from datetime import datetime
from sanic.blueprints import Blueprint

from app.utils import tools
from app.utils.response import response
from app.utils.request import AuthParam
from app.models.app_model import Action as AppAction
from app.models.log_model import Action as LogAction
from app.models.ticket_model import Action as TicketAction
from app.models.user_model import Action as UserAction


oauth = Blueprint(name="apiOauth", url_prefix="/oauth")


# Oauth 登录
@oauth.route("/authorize", ["GET"])
async def authorize(request):
    return await handleResponse(request=request,type="authorize")

# Oauth 注册
@oauth.route("/register", ["GET"])
async def register(request):
    return await handleResponse(request=request,type="register")

@oauth.route("/check", ["POST"])
@AuthParam("ticket","client_id","client_serect")
async def check(request):
    
    ticket = request.json["ticket"]
    clientId = request.json["client_id"]
    clientSerect = request.json["client_serect"]
    
    clientIp = tools.getClientIp(request=request)
    
    ticketData = await TicketAction(request=request).Get(ticket=ticket)
    
    appInfo = await AppAction(request=request).Get(client_id=clientId)

    if not appInfo or appInfo.client_serect != clientSerect:
        return response.error("无权验证")
    
    if not ticketData or ticketData.used_time:
        return response.error("凭据无效")
    
    if datetime.now() > ticketData.expiredtime:
        return response.error("凭据过期")
    
    await TicketAction(request=request).UpdateUsedTime(ticketData)
    
    userInfo = await UserAction(request=request).GetById(ticketData.uid)
    
    if not userInfo:
        return response.error("用户不存在")
    
    await LogAction(request=request).Insert(
        userInfo.id,
        f"【{appInfo.name}】 客户端凭据验证",
        request.json,
        clientIp # 极验IP可信度更高
    )
    
    return response.succWithData(userInfo.to_dict(),"验证成功") # 授权 用户数据
    

async def handleResponse(request,type):
    responseType = request.args.get("response_type")
    clientId = request.args.get("client_id")
    redirectUri = request.args.get("redirect_uri")
    
    appInfo = await AppAction(request=request).Get(client_id=clientId)

    if not appInfo:
        return response.error("客户端不存在")

    if not redirectUri:
        redirectUri = appInfo.redirect_uri
    
    if type == "authorize":
        page = "oauth/login.html"
    else:
        page = "oauth/register.html"
        
    if responseType == "code":
        return request.app.config.jinja.render(
            page, request,data={
                "GEETEST_ID":request.app.config.GEETEST_ID.value,
                "client_id":appInfo.client_id,
                "redirect_uri":redirectUri
            }
        )
        
    return response.error("不受支持的凭证方式")
    
    
