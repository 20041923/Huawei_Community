import json
import csv
import os
import re
from datetime import datetime
from utils.config import Config


class DataSaver:
    def __init__(self):
        self.data_dir = Config.DATA_DIR
        self.save_format = Config.SAVE_FORMAT
        self._ensure_data_dir()

    def _ensure_data_dir(self):
        """确保数据目录存在"""
        if not os.path.exists(self.data_dir):
            os.makedirs(self.data_dir)

    def _extract_text_from_html(self, html_content):
        """从HTML内容中提取纯文本"""
        if not html_content:
            return ""

        # 方法1: 使用正则表达式去除HTML标签
        text = re.sub(r'<[^>]+>', '', html_content)

        # 方法2: 处理常见的HTML实体
        text = text.replace('&nbsp;', ' ').replace('&amp;', '&').replace('&lt;', '<').replace('&gt;', '>')

        # 去除多余的空格和换行
        text = re.sub(r'\s+', ' ', text).strip()

        return text

    def _extract_plain_text(self, content):
        """提取纯文本内容，处理HTML格式"""
        if not content:
            return ""

        # 如果内容包含HTML标签
        if '<' in content and '>' in content:
            return self._extract_text_from_html(content)

        return content.strip()

    def save_comments(self, post_uuid, comments, post_info=None, post_text=""):
        """保存评论数据"""
        if self.save_format == "json":
            self._save_as_json(post_uuid, comments, post_info, post_text)
        elif self.save_format == "csv":
            self._save_as_csv_simple(comments, post_uuid, post_text)
        elif self.save_format == "csv_advanced":
            self._save_as_csv_advanced(comments, post_uuid, post_text)

    def _save_as_json(self, post_uuid, comments, post_info, post_text):
        """保存为JSON格式"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"comments_{post_uuid}_{timestamp}.json"
        filepath = os.path.join(self.data_dir, filename)

        data = {
            "post_uuid": post_uuid,
            "post_text": post_text,
            "post_info": post_info,
            "comments": comments,
            "crawl_time": timestamp,
            "comment_count": len(comments)
        }

        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        print(f"✅ 成功保存 {len(comments)} 条评论到 {filename}")

    def _save_as_csv_simple(self, comments, post_uuid, post_text):
        """简单CSV保存 - 只保存content"""
        filename = "comments_content_only.csv"
        filepath = os.path.join(self.data_dir, filename)
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # 提取content字段
        comments_to_save = []
        for comment in comments:
            content = comment.get('content', '')
            if content and content.strip():  # 只保存非空内容
                comments_to_save.append({
                    'post_uuid': post_uuid,
                    'post_text': post_text,
                    'content': self._extract_plain_text(content),
                    'crawl_time': timestamp
                })

        if comments_to_save:
            file_exists = os.path.exists(filepath)

            with open(filepath, 'a', newline='', encoding='utf-8-sig') as f:
                writer = csv.DictWriter(f, fieldnames=['post_uuid', 'post_text', 'content', 'crawl_time'])

                if not file_exists:
                    writer.writeheader()

                writer.writerows(comments_to_save)

            print(f"✅ 成功追加 {len(comments_to_save)} 条评论到 {filename}")
        else:
            print("⚠️ 没有找到有效的评论内容")

    def _save_as_csv_advanced(self, comments, post_uuid, post_text):
        """高级CSV保存 - 保存更多字段"""
        filename = "all_comments_detailed.csv"
        filepath = os.path.join(self.data_dir, filename)
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        comments_to_save = []
        for comment in comments:
            # 提取常用字段
            create_time = int(comment.get('createTime', '')) / 1000
            # print(create_time)
            comment_data = {
                'post_uuid': post_uuid,
                'post_text': post_text,
                'content': self._extract_plain_text(comment.get('content', '')),
                'comment_id': comment.get('commentId', ''),
                'user_name': comment.get('maskName', ''),
                'create_time': datetime.fromtimestamp(create_time).strftime("%Y-%m-%d %H:%M:%S"),
                'crawl_time': timestamp
            }
            # print(comment_data)

            # 只保存有内容的评论
            if comment_data['content'] and comment_data['content'].strip():
                comments_to_save.append(comment_data)

        if comments_to_save:
            file_exists = os.path.exists(filepath)

            with open(filepath, 'a', newline='', encoding='utf-8-sig') as f:
                fieldnames = ['post_uuid', 'post_text', 'content', 'comment_id', 'user_name', 'create_time',
                              'crawl_time']
                writer = csv.DictWriter(f, fieldnames=fieldnames)

                if not file_exists:
                    writer.writeheader()

                writer.writerows(comments_to_save)

            print(f"✅ 成功追加 {len(comments_to_save)} 条详细评论到 {filename}")

    def save_progress(self, current_page, processed_posts, current_post_uuid=None, current_post_comments=None):
        """保存爬取进度 - 增强版，支持保存当前帖子进度"""
        progress_file = os.path.join(self.data_dir, "progress.json")

        progress_data = {
            "last_page": current_page,
            "processed_posts": processed_posts,
            "last_update": datetime.now().isoformat()
        }

        # 如果提供了当前帖子的信息，也保存下来
        if current_post_uuid and current_post_comments is not None:
            progress_data["current_post"] = {
                "uuid": current_post_uuid,
                "comments_count": len(current_post_comments),
                "comments": current_post_comments  # 保存已获取的评论
            }

        with open(progress_file, 'w', encoding='utf-8') as f:
            json.dump(progress_data, f, ensure_ascii=False, indent=2)

        print(f"💾 进度已保存: 第{current_page}页, 已处理{len(processed_posts)}个帖子")

    def load_progress(self):
        """加载爬取进度"""
        progress_file = os.path.join(self.data_dir, "progress.json")
        if os.path.exists(progress_file):
            with open(progress_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        return None

    def save_partial_comments(self, post_uuid,post_text, comments, reason="interrupted"):
        """保存部分评论数据（用于中断时保存）"""
        if comments:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"partial_comments_{post_uuid}_{reason}_{timestamp}.json"
            filepath = os.path.join(self.data_dir, filename)

            data = {
                "post_uuid": post_uuid,
                "post_text":post_text,
                "comments": comments,
                "comment_count": len(comments),
                "crawl_time": timestamp,
                "status": "partial",
                "reason": reason
            }

            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)

            print(f"🔄 保存部分评论数据: {len(comments)} 条评论到 {filename}")
            return True
        return False
