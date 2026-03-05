"""
SoulGuard异常处理模块
"""

import logging
import traceback
from datetime import datetime

logger = logging.getLogger('soulguard')

class SoulGuardException(Exception):
    """SoulGuard基础异常"""
    pass

class MemoryException(SoulGuardException):
    """记忆系统异常"""
    pass

class StorageException(SoulGuardException):
    """存储异常"""
    pass

def handle_exception(func):
    """异常处理装饰器"""
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            error_msg = f"[{datetime.now()}] {func.__name__}: {str(e)}"
            logger.error(error_msg)
            logger.error(traceback.format_exc())
            
            # 保存错误到文件
            with open('/root/.openclaw/soulguard/logs/errors.log', 'a') as f:
                f.write(error_msg + '\n')
                f.write(traceback.format_exc() + '\n')
            
            # 返回默认值
            return None
    return wrapper
