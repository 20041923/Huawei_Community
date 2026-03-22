import logging
import os
from datetime import datetime
from utils.config import Config


def setup_logger():
    """设置日志配置"""
    if not os.path.exists(Config.LOG_DIR):
        os.makedirs(Config.LOG_DIR)

    log_filename = datetime.now().strftime("crawler_%Y%m%d_%H%M%S.log")
    log_path = os.path.join(Config.LOG_DIR, log_filename)

    logging.basicConfig(
        level=getattr(logging, Config.LOG_LEVEL),
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(log_path, encoding='utf-8'),
            logging.StreamHandler()
        ]
    )

    return logging.getLogger(__name__)


logger = setup_logger()