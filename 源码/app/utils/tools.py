"""
 * 工具函数
 * Author: 孙洪达
 * Time: 2023/11/16
 * Mail: iamoumeng@aliyun.com
"""

import uuid
import hashlib
import random
import string

# 获取客户端真实IP地址
def getClientIp(request):
    possibleHeaders = ['X-Forwarded-For', 'X-Real-IP', 'CF-Connecting-IP']
    
    for header in possibleHeaders:
        clientIp = request.headers.get(header)
        if clientIp:
            break
    else:
        clientIp = request.remote_addr
        if not clientIp:
            clientIp = request.ip

    return clientIp

# MD5 + 盐值 加密
def strToMd5(str,salt):
    return hashlib.md5((str.join(salt)).encode()).hexdigest()

# 生成随机字符
def randomStr(length=4):
    str_list = [random.choice(string.ascii_letters + string.digits) for i in range(length)]
    return ''.join(str_list)

# 生成随机 UUID
def randomUuid():
    return str(uuid.uuid4())