"""
 * Ticket 模型
 * Author: 孙洪达
 * Time: 2023/11/16
 * Mail: iamoumeng@aliyun.com
"""

import datetime
from app.models import PrefixerBase
from sqlalchemy import Column, Integer, String,BigInteger, DateTime, select


class Ticket(PrefixerBase):

    __incomplete_tablename__ = 'ticket'

    id = Column(Integer, primary_key=True, autoincrement=True)
    uid = Column(Integer)
    client_id = Column(BigInteger)
    ticket = Column(String(32))
    used_time = Column(DateTime, default=None)
    ip = Column(String(32))
    expiredtime = Column(DateTime)
    createtime = Column(DateTime, default=datetime.datetime.now)
    


class Action:
    def __init__(self, request) -> None:
        self.Session = request.ctx.session

    async def Get(self,ticket):
        stmt = select(Ticket).filter_by(ticket=ticket)
        result = await self.Session.execute(stmt)
        record = result.scalar()

        if not record:
            return False
        
        return record
    
    async def Insert(self, uid, client_id,ticket,ip,expiry_second):
        expiry_time  = datetime.datetime.now() + datetime.timedelta(seconds=expiry_second)
        self.Session.add(Ticket(uid=uid, client_id=client_id,ticket=ticket,ip=ip,expiredtime=expiry_time))
        await self.Session.commit()
    
    async def UpdateUsedTime(self,record):
        record.used_time = datetime.datetime.now()
        await self.Session.commit()
    