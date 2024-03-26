"""
 * 配置文件
 * Author: 孙洪达
 * Time: 2023/11/12
 * Mail: iamoumeng@aliyun.com
"""

from enum import Enum

class config(Enum):

    """GEETEST"""
    GEETEST_SERVER = 'http://gcaptcha4.geetest.com'
    GEETEST_ID = '123'
    GEETEST_KEY = '123'
    GEETEST_CAPTCHA_URL = f'{GEETEST_SERVER}/validate?captcha_id={GEETEST_ID}'

    """SYSTEM"""
    APP_VERSION = "1.0.0" # 软件版本
    TICKET_EXPIRY_SECOND = 300 # 凭证过期时间
    
    """JWT"""
    # JWT Token 下发 | 旧项目保留 后边可能会用到
    # JWT_KEY = b"\xba\xf2\x75\xc2\x09\x72\xba\x36\x40\xd3\x8c\x63\x50\x65\x27\xec"
    # JWT_INDATE = 604800

    """MYSQL"""
    DB_HOST = '127.0.0.1'
    DB_PORT = 3306
    DB_PREFIX = 'oauth_'
    DB_NAME = 'oauth2'
    DB_USERNAME = 'oauth2'
    DB_PASSWORD = 'oauth2'
