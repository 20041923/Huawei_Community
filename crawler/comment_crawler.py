import requests
import time
from typing import List, Dict, Optional
from utils.logger import logger
from utils.config import Config, COOKIES, HEADERS


class CommentCrawler:
    def __init__(self, data_saver=None):
        self.base_url = Config.BASE_URL
        self.cookies = COOKIES
        self.headers = HEADERS
        self.session = requests.Session()
        self.session.cookies.update(self.cookies)
        self.session.headers.update(self.headers)
        self.data_saver = data_saver

    def get_comments(self, post_uuid: str, page: int = 1) -> Optional[Dict]:
        """获取指定帖子的评论"""
        url = f"{self.base_url}/xsapi/user/v1/posts/{post_uuid}/comments/list"

        json_data = {
            'uuid': post_uuid,
            'pageParam': {
                'curPage': page,
                'pageSize': Config.COMMENTS_PER_PAGE,
            },
            'sortBy': 0,
            'maskIds': [],
        }

        for attempt in range(Config.MAX_RETRIES):
            try:
                response = self.session.post(url, json=json_data, timeout=Config.REQUEST_TIMEOUT)
                response.raise_for_status()
                data = response.json()

                if data.get('message') == 'success':
                    return data.get('data', {})
                else:
                    logger.warning(f"获取评论失败 (尝试 {attempt + 1}/{Config.MAX_RETRIES}): {data.get('message')}")

            except requests.RequestException as e:
                logger.warning(f"请求评论失败 (尝试 {attempt + 1}/{Config.MAX_RETRIES}): {e}")

            if attempt < Config.MAX_RETRIES - 1:
                time.sleep(Config.RETRY_DELAY * (attempt + 1))

        return None

    def get_all_comments(self, post_uuid: str, save_callback=None) -> List[Dict]:
        """获取帖子的所有评论，支持实时保存"""
        all_comments = []
        current_page = 1

        while True:
            logger.info(f"正在获取帖子 {post_uuid} 的第 {current_page} 页评论...")
            result = self.get_comments(post_uuid, current_page)
            if not result:
                break
            comments = result.get('list', [])
            if not comments:
                logger.info(f"帖子 {post_uuid} 没有更多评论了")
                break

            # 添加到总列表
            all_comments.extend(comments)
            logger.info(f"帖子 {post_uuid} 第 {current_page} 页获取到 {len(comments)} 条评论")

            # 实时保存回调（用于保存进度）
            if save_callback:
                save_callback(post_uuid, all_comments)

            # 检查是否还有更多页面
            page_info = result.get('page', {})
            total_pages = page_info.get('totalPages', 0)
            if current_page >= total_pages:
                logger.info(f"帖子 {post_uuid} 已到达最后一页，共 {total_pages} 页")
                break

            current_page += 1
            time.sleep(1)  # 避免请求过快

        return all_comments

    def get_comments_with_progress(self, post_uuid: str, post_text: str, progress_saver) -> List[Dict]:
        """获取评论并实时保存进度"""
        all_comments = []
        current_page = 1

        try:
            while True:
                if not progress_saver.is_running:
                    logger.info("爬虫被终止，保存当前进度...")
                    # 保存已获取的部分评论
                    if all_comments and self.data_saver:
                        self.data_saver.save_partial_comments(post_uuid, post_text, all_comments, "interrupted")
                    break

                logger.info(f"正在获取帖子 {post_uuid} 的第 {current_page} 页评论...")

                result = self.get_comments(post_uuid, current_page)
                if not result:
                    break

                comments = result.get('list', [])
                if not comments:
                    logger.info(f"帖子 {post_uuid} 没有更多评论了")
                    break

                # 添加到总列表
                all_comments.extend(comments)
                logger.info(f"帖子 {post_uuid} 第 {current_page} 页获取到 {len(comments)} 条评论")

                # 立即保存当前进度
                progress_saver.save_current_post_progress(post_uuid, all_comments)

                # 检查是否还有更多页面
                page_info = result.get('page', {})
                total_pages = page_info.get('totalPages', 0)
                if current_page >= total_pages:
                    logger.info(f"帖子 {post_uuid} 已到达最后一页，共 {total_pages} 页")
                    break

                current_page += 1
                time.sleep(1)  # 避免请求过快

        except KeyboardInterrupt:
            logger.info("用户中断，保存当前进度...")
            if all_comments and self.data_saver:
                self.data_saver.save_partial_comments(post_uuid, post_text, all_comments, "user_interrupt")
            raise

        return all_comments
