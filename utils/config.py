# 配置设置

class Config:
    # 基础配置
    BASE_URL = "https://xinsheng.huawei.com"
    
    # 请求配置
    REQUEST_TIMEOUT = 30
    MAX_RETRIES = 3
    RETRY_DELAY = 2
    
    # 分页配置
    POSTS_PER_PAGE = 50
    COMMENTS_PER_PAGE = 20
    
    # 日志配置
    LOG_DIR = "logs"
    LOG_LEVEL = "INFO"
    
    # 数据存储
    DATA_DIR = "data"
    SAVE_FORMAT = "csv_advanced"

#  cookies 和 headers 需要用户根据实际情况设置
COOKIES = {
    'SESSION': 'OGZkZTQ2MDktMjU1MC00MDk3LWIyMjAtNTJmNGJiZGJhYmYz',
    'sensorsdata2015jssdkcross': '%7B%22distinct_id%22%3A%2219d15a9437a1d3-0a8c536fe1a8c5-4c657b58-1327104-19d15a9437bdb5%22%2C%22first_id%22%3A%22%22%2C%22props%22%3A%7B%7D%2C%22identities%22%3A%22eyIkaWRlbnRpdHlfY29va2llX2lkIjoiMTlkMTVhOTQzN2ExZDMtMGE4YzUzNmZlMWE4YzUtNGM2NTdiNTgtMTMyNzEwNC0xOWQxNWE5NDM3YmRiNSJ9%22%2C%22history_login_id%22%3A%7B%22name%22%3A%22%22%2C%22value%22%3A%22%22%7D%2C%22%24device_id%22%3A%2219d15a9437a1d3-0a8c536fe1a8c5-4c657b58-1327104-19d15a9437bdb5%22%7D',
    'sajssdk_2015_cross_new_user': '1',
}

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    "Accept": "application/json, text/plain, */*",
    "Accept-Language": "zh-CN,zh;q=0.9",
    "Accept-Encoding": "gzip, deflate, br",
    "Content-Type": "application/json",
    "X-Requested-With": "XMLHttpRequest",
    "Origin": "https://xinsheng.huawei.com",
    "Referer": "https://xinsheng.huawei.com/cn/index.html",
    "Connection": "keep-alive",
    "Sec-Fetch-Dest": "empty",
    "Sec-Fetch-Mode": "cors",
    "Sec-Fetch-Site": "same-origin"
}
