#!/usr/bin/env bash

###########
#
#  运行 酷Q-cqhttp Docker 版
#
# Note 1: CQ-HTTP 称以它自己为服务端的情况为正向，而以 NoneBot 为服务端，由 CQ-HTTP 来请求 NoneBot 的情形为反向
#       这里使用的是反向 WebSocket，以 NoneBot 为服务器，CQ-HTTP 主动通过配置好的上报接口向 NoneBot 发起连接。
#
# Note 2: 运行完后，可以进 `scripts/coolq/app\io.github.richardchien.coolqhttpapi\$COOLQ_ACCOUNT.ini`检查配置。
#
# Note 3: 需要在项目根目录下运行！而不是在 scripts 文件夹下运行！
###########

# 将 prod.env 中的 key=value 导入到当前环境变量中，忽略注释行和换行
set -a
. ./prod.env
set +a

docker-compose pull
docker compose up -d
