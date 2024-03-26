"""
 * APP 模型
 * Author: 孙洪达
 * Time: 2023/11/16
 * Mail: iamoumeng@aliyun.com
"""

import datetime
from app.models import PrefixerBase
from sqlalchemy import Column, Integer, String,BigInteger, DateTime, select, func


class App(PrefixerBase):

    __incomplete_tablename__ = 'app'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(32))
    client_id = Column(BigInteger)
    client_serect = Column(String(32))
    redirect_uri = Column(String(32))
    createtime = Column(DateTime, default=datetime.datetime.now)

class Action:
    def __init__(self, request) -> None:
        self.Session = request.ctx.session

    async def Get(self,client_id):
        stmt = select(App).filter_by(client_id=client_id)
        result = await self.Session.execute(stmt)
        record = result.scalar()

        if not record:
            return False
        
        return record