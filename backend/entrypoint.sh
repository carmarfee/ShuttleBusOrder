#!/bin/sh

# 等待 MySQL 准备就绪
# 我们需要安装 netcat (nc) 来检查端口
echo "Waiting for mysql..."
while ! nc -z mysql 3306; do
  sleep 0.1
done
echo "MySQL started"

# 执行传递给脚本的原始命令 (也就是 uvicorn)
exec "$@"