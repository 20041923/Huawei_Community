import requests
import time
from typing import List, Dict, Optional
from utils.logger import logger
from utils.config import Config, COOKIES, HEADERS


class PostCrawler:
    def __init__(self):
        self.base_url = Config.BASE_URL
        self.cookies = COOKIES
        self.headers = HEADERS
        self.session = requests.Session()
        self.session.cookies.update(self.cookies)
        self.session.headers.update(self.headers)

    def get_posts(self, section_id: str, page: int = 1) -> Optional[Dict]:
        """获取指定页面的帖子列表"""
        url = f"{self.base_url}/xsapi/user/sections/posts/list/{section_id}/{page}/{Config.POSTS_PER_PAGE}"

        params = {
            'flag': 'all',
            'sortBy': 'replyTime',
            'searchType': 'all',
            'cityId': '',
            'categoryId': '',
        }

        try:
            response = self.session.get(url, params=params, timeout=Config.REQUEST_TIMEOUT)
            response.raise_for_status()
            data = response.json()
            print(data)
            if data.get('message') == 'success':
                return data.get('data', {})
            else:
                logger.error(f"获取帖子列表失败: {data.get('message')}")
                return None

        except requests.RequestException as e:
            logger.error(f"请求帖子列表失败: {e}")
            return None

    def get_all_posts(self, section_id: str, start_page: int = 1) -> List[Dict]:
        """获取所有帖子"""
        all_posts = []
        current_page = start_page

        while True:
            logger.info(f"正在获取第 {current_page} 页的帖子...")

            result = self.get_posts(section_id, current_page)
            if not result:
                break

            posts = result.get('list', [])
            if not posts:
                logger.info("没有更多帖子了")
                break

            all_posts.extend(posts)
            logger.info(f"第 {current_page} 页获取到 {len(posts)} 个帖子")

            # 检查是否还有更多页面
            total_pages = result.get('totalPage', 0)
            if current_page >= total_pages:
                logger.info(f"已到达最后一页，共 {total_pages} 页")
                break

            current_page += 1
            time.sleep(1)  # 避免请求过快

        return all_posts