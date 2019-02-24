#!/usr/bin/env bash

###########
#
#  运行 酷Q-cqhttp Docker 版
#
# Note 1: CQ-HTTP 称以它自己为服务端的情况为正向，而以 NoneBot 为服务端，由 CQ-HTTP 来请求 NoneBot 的情形为反向
#       这里使用的是反向 WebSocket，以 NoneBot 为服务器，CQ-HTTP 主动通过配置好的上报接口向 NoneBot 发起连接。
#
# Note 2: 运行完后，可以进 `scripts/coolq/app\io.github.richardchien.coolqhttpapi\$COOLQ_ACCOUNT.ini`检查配置。
###########

# 加载配置（环境变量）
source ../.env

# 运行 酷Q-cqhttp 的 container
# 只需要映射 9000 端口，用于通过 noVNC 连接酷Q的GUI
# 因为与 nonebot 是通过反向 WebSocket 通信，是 CQ-HTTP 请求外面的 nonebot，因此不需要额外的 port
sudo docker run -ti --rm --name cqhttp-coolq \
             -d \
             -v ~/coolq:/home/user/coolq \
             -e COOLQ_ACCOUNT=$COOLQ_ACCOUNT  \
             -e VNC_PASSWD=$VNC_PASSWD \
             -p 9000:9000 \
             -e FORCE_ENV=$FORCE_ENV \
             -e CQHTTP_USE_HTTP=no \
             -e CQHTTP_USE_WS_REVERSE=yes  \
             -e CQHTTP_ACCESS_TOKEN=$CQHTTP_ACCESS_TOKEN  \
             -e CQHTTP_SECRET=$CQHTTP_SECRET \
             -e CQHTTP_WS_REVERSE_API_URL=$CQHTTP_WS_REVERSE_API_URL  \
             -e CQHTTP_WS_REVERSE_EVENT_URL=$CQHTTP_WS_REVERSE_EVENT_URL  \
             -e CQHTTP_SERVE_DATA_FILES=$CQHTTP_SERVE_DATA_FILES  \
             richardchien/cqhttp:latest


