"""
 * Log 模型
 * Author: 孙洪达
 * Time: 2023/11/16
 * Mail: iamoumeng@aliyun.com
"""

import datetime
from app.models import PrefixerBase
from sqlalchemy import Column, Integer, String,JSON,DateTime


class Log(PrefixerBase):

    __incomplete_tablename__ = 'log'

    id = Column(Integer, primary_key=True, autoincrement=True)
    uid = Column(Integer,default=0)
    event = Column(String(32),default="")
    data = Column(JSON,default={})
    ip = Column(String(32),default="")
    createtime = Column(DateTime, default=datetime.datetime.now)

class Action:
    def __init__(self, request) -> None:
        self.Session = request.ctx.session

    async def Insert(self, uid=0, event="",data={},ip=""):
        self.Session.add(Log(uid=uid, event=event,data=data,ip=ip))
        await self.Session.commit()