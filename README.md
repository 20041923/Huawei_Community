# 华为心声社区---华为家事---帖子+评论爬虫

## 项目描述

这是一个基于 Python 开发的爬虫脚本，用于爬取华为心声社区的帖子和评论数据。该项目支持断点续爬、优雅退出和数据保存功能，旨在帮助用户获取和分析华为心声社区的公开数据。

## 功能特性

- 支持爬取华为心声社区的帖子列表
- 支持爬取每个帖子的评论数据
- 支持断点续爬，保存爬取进度
- 支持优雅退出，处理中断信号
- 自动保存数据到 CSV 文件
- 完善的日志记录系统
- 支持配置文件自定义爬虫行为

## 技术栈

- **编程语言**：Python 3.8+
- **核心库**：requests
- **数据处理**：csv, json, re
- **日志系统**：自定义日志模块
- **文件操作**：os, datetime

## 项目结构

```
Huawei_Community/
├── main.py                # 主入口文件
├── crawler/               # 爬虫模块
│   ├── __init__.py
│   ├── post_crawler.py    # 帖子爬取器
│   └── comment_crawler.py # 评论爬取器
├── storage/               # 数据存储模块
│   ├── __init__.py
│   └── data_saver.py      # 数据保存器
├── utils/                 # 工具模块
│   ├── __init__.py
│   ├── config.py          # 配置文件
│   └── logger.py          # 日志工具
├── data/                  # 数据存储目录
│   ├── all_comments_detailed.csv  # 详细评论数据
│   └── progress.json      # 爬取进度数据
├── logs/                  # 日志目录
├── requirements.txt       # 依赖包列表
└── README.md              # 项目说明文档
```

## 安装

### 1. 克隆仓库

```bash
git clone https://github.com/your-username/huawei-xinsheng-crawler.git
cd Huawei_Community
```

### 2. 安装依赖

```bash
# 使用 pip 安装依赖
pip install -r requirements.txt
```

### 3. 配置设置

修改 `utils/config.py` 文件，设置以下参数：

- `BASE_URL`：华为心声社区的基础 URL
- `COOKIES`：登录后的 cookies（需要手动获取）
- `HEADERS`：请求头信息
- `REQUEST_TIMEOUT`：请求超时时间
- `MAX_RETRIES`：最大重试次数
- `RETRY_DELAY`：重试延迟时间
- `POSTS_PER_PAGE`：每页帖子数量
- `COMMENTS_PER_PAGE`：每页评论数量
- `LOG_DIR`：日志目录
- `LOG_LEVEL`：日志级别
- `DATA_DIR`：数据存储目录
- `SAVE_FORMAT`：数据保存格式

## 使用方法

### 基本使用

```bash
# 运行爬虫
python main.py

# 查看帮助（如果实现了命令行参数）
python main.py --help
```

### 自定义版块

在 `main.py` 文件中修改 `section_id` 参数，指定要爬取的版块 ID：

```python
def main():
    """主函数"""
    # 可以在这里指定不同的版块ID
    section_id = "713534611705233409"  # 默认版块ID

    crawler = HuaweiXinshengCrawler(section_id)
    crawler.run()
```

## 数据结构

### 帖子数据

```python
{
    'uuid': '帖子唯一标识',
    'title': '帖子标题',
    'content': '帖子内容',
    'author': '作者信息',
    'publishTime': '发布时间',
    'replyCount': '回复数量',
    'viewCount': '浏览数量'
    # 其他字段...
}
```

### 评论数据

```python
{
    'uuid': '评论唯一标识',
    'content': '评论内容',
    'author': '评论作者',
    'publishTime': '评论时间',
    'likeCount': '点赞数量'
    # 其他字段...
}
```

## 数据存储

爬取的数据会保存到以下文件：

- `data/all_comments_detailed.csv`：详细的评论数据
- `data/progress.json`：爬取进度数据（用于断点续爬）

## 日志系统

日志文件会保存在 `logs/` 目录下，命名格式为 `crawler_YYYYMMDD_HHMMSS.log`。

## 注意事项

1. **合法性**：本项目仅用于学习和研究目的，请遵守相关网站的 robots.txt 规则和法律法规
2. **登录状态**：需要在 `utils/config.py` 中设置有效的 cookies 才能正常爬取
3. **请求频率**：爬虫已内置延迟机制，避免请求过快导致被封禁
4. **断点续爬**：如果爬虫被中断，下次运行时会从上次的进度继续

## 常见问题

### 1. 爬虫无法获取数据

- 检查 `COOKIES` 是否正确设置
- 检查网络连接是否正常
- 检查 `BASE_URL` 是否正确

### 2. 爬虫被封禁

- 减少请求频率
- 更换 IP 地址
- 更换 cookies

### 3. 数据保存失败

- 检查文件权限
- 检查磁盘空间
- 检查数据格式是否正确

## 贡献

欢迎贡献代码和提出建议！请按照以下步骤进行：

1. Fork 本仓库
2. 创建特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 打开 Pull Request

## 许可证

本项目使用 [MIT](LICENSE) 许可证

## 联系方式

- 作者：Your Name
- 邮箱：your.email@example.com
- 项目链接：[https://github.com/your-username/huawei-xinsheng-crawler](https://github.com/your-username/huawei-xinsheng-crawler)

---

*如有任何问题或建议，请随时联系我。*