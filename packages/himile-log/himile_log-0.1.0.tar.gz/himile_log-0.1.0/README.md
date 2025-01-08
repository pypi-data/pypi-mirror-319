使用示例
```
from himile_log import get_default_logger

my_logger = get_default_logger()

my_logger.info('hello')
```
自定义日志对象
```
from himile_log import setup_logger

logger = setup_logger(logs_dir="logs", log_level="INFO")

logger.info('hello')
```