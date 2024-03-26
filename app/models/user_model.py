"""
 * APP 模型
 * Author: 孙洪达
 * Time: 2023/11/16
 * Mail: iamoumeng@aliyun.com
"""

import datetime

from app.models import PrefixerBase
from sqlalchemy import Column, Integer, String,BigInteger, DateTime, select, func


class User(PrefixerBase):

    __incomplete_tablename__ = 'user'

    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(32))
    password = Column(String(32))
    salt = Column(String(32))
    lastloginip = Column(BigInteger)
    lastlogintime = Column(DateTime, default=datetime.datetime.now)
    createtime = Column(DateTime, default=datetime.datetime.now)

    def to_dict(self):
        return {
            "username": self.username,
            "last_login_ip": self.lastloginip,
            "last_login_time": self.lastlogintime.strftime('%Y-%m-%d %H:%M:%S'),
            "create_time": self.createtime.strftime('%Y-%m-%d %H:%M:%S'),
        }
    

class Action:
    def __init__(self, request) -> None:
        self.Session = request.ctx.session

    async def Get(self,username):
        stmt = select(User).filter_by(username=username)
        result = await self.Session.execute(stmt)
        record = result.scalar()

        if not record:
            return False
        
        return record

    async def GetById(self,id):
        stmt = select(User).filter_by(id=id)
        result = await self.Session.execute(stmt)
        record = result.scalar()

        if not record:
            return False
        
        return record

    async def Insert(self, username, password,salt):
        self.Session.add(User(username=username, password=password,salt=salt))
        await self.Session.commit()
    
    async def UpdateLoginInfo(self,record,ip):
        record.lastlogintime = datetime.datetime.now()
        record.lastloginip = ip
        await self.Session.commit()
    
                
            

