import time
import signal
import sys
from crawler.post_crawler import PostCrawler
from crawler.comment_crawler import CommentCrawler
from storage.data_saver import DataSaver
from utils.logger import logger


class HuaweiXinshengCrawler:
    def __init__(self, section_id: str = "713534611705233409"):
        self.section_id = section_id
        self.post_crawler = PostCrawler()
        self.data_saver = DataSaver()
        self.comment_crawler = CommentCrawler(self.data_saver)
        self.is_running = True

        # 设置信号处理，优雅退出
        signal.signal(signal.SIGINT, self.signal_handler)
        signal.signal(signal.SIGTERM, self.signal_handler)

    def signal_handler(self, signum, frame):
        """处理中断信号"""
        logger.info("接收到退出信号，正在保存进度...")
        self.is_running = False

    def save_current_post_progress(self, post_uuid, current_comments):
        """保存当前帖子进度"""
        progress = self.data_saver.load_progress()
        if progress:
            processed_posts = set(progress.get('processed_posts', []))
        else:
            processed_posts = set()

        # 保存进度，包括当前帖子的部分评论
        self.data_saver.save_progress(
            progress.get('last_page', 1) if progress else 1,
            list(processed_posts),
            post_uuid,
            current_comments
        )

    def run(self):
        """运行爬虫"""
        logger.info("开始爬取华为心声社区数据...")

        # 加载进度
        progress = self.data_saver.load_progress()
        if progress:
            start_page = progress.get('last_page', 1)
            processed_posts = set(progress.get('processed_posts', []))

            # 检查是否有中断的帖子
            current_post = progress.get('current_post')
            if current_post:
                post_uuid = current_post.get('uuid')
                existing_comments = current_post.get('comments', [])
                logger.info(f"发现中断的帖子 {post_uuid}，已有 {len(existing_comments)} 条评论")
                # 这里可以处理恢复中断的帖子，为了简化我们先跳过

            logger.info(f"从上次进度继续: 第 {start_page} 页，已处理 {len(processed_posts)} 个帖子")
        else:
            start_page = 1
            processed_posts = set()

        # 获取所有帖子
        posts = self.post_crawler.get_all_posts(self.section_id, start_page)
        logger.info(f"共获取到 {len(posts)} 个帖子")

        # 爬取每个帖子的评论
        for i, post in enumerate(posts):
            if not self.is_running:
                logger.info("爬虫被终止，退出循环")
                break

            post_uuid = post.get('uuid')
            post_text = post.get('title')
            if not post_uuid or post_uuid in processed_posts:
                logger.info(f"跳过帖子 {post_uuid} (已处理)")
                continue

            logger.info(f"正在处理第 {i + 1}/{len(posts)} 个帖子: {post_uuid} - {post_text}")

            try:
                # 获取评论（带实时进度保存）
                comments = self.comment_crawler.get_comments_with_progress(post_uuid, post_text, self)
                logger.info(f"帖子 {post_uuid} 共获取到 {len(comments)} 条评论")

                # 保存评论到CSV
                self.data_saver.save_comments(post_uuid, comments, post, post_text)

                # 标记为已处理
                processed_posts.add(post_uuid)

                # 保存进度（不包含当前帖子评论，因为已经完成）
                self.data_saver.save_progress(start_page, list(processed_posts))

                logger.info(f"✅ 成功完成帖子 {post_uuid} 的爬取")

            except KeyboardInterrupt:
                logger.info("用户中断爬取")
                break
            except Exception as e:
                logger.error(f"处理帖子 {post_uuid} 时发生错误: {e}")
                # 即使出错，也保存进度
                self.data_saver.save_progress(start_page, list(processed_posts))

            # 添加延迟，避免请求过快
            if self.is_running:
                time.sleep(2)

        if self.is_running:
            logger.info("🎉 爬取完成！")
        else:
            logger.info("⏸️ 爬取被中断，进度已保存")


def main():
    """主函数"""
    # 可以在这里指定不同的版块ID
    section_id = "713534611705233409"  # 默认版块ID

    crawler = HuaweiXinshengCrawler(section_id)
    crawler.run()


if __name__ == "__main__":
    main()
