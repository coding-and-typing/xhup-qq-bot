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
             --network host \
             -v ~/coolq:/home/user/coolq \
             -e COOLQ_ACCOUNT=$COOLQ_ACCOUNT  \
             -e VNC_PASSWD=$VNC_PASSWD \
             -e FORCE_ENV=$FORCE_ENV \
             -e CQHTTP_USE_HTTP=no \
             -e CQHTTP_USE_WS_REVERSE=yes  \
             -e CQHTTP_ACCESS_TOKEN=$CQHTTP_ACCESS_TOKEN  \
             -e CQHTTP_WS_REVERSE_API_URL=$CQHTTP_WS_REVERSE_API_URL  \
             -e CQHTTP_WS_REVERSE_EVENT_URL=$CQHTTP_WS_REVERSE_EVENT_URL  \
             -e CQHTTP_SERVE_DATA_FILES=$CQHTTP_SERVE_DATA_FILES  \
             richardchien/cqhttp:latest

#sudo docker run -ti --rm --name cqhttp-coolq \   #
#             -d \   # daemon，后台运行
#             --network host \   # host 模式下，容器的 localhost，就是宿主机的 localhost。即与宿主机共用网络
#             -v ~/coolq:/home/user/coolq \   # 将容器的 /home/user/coolq 文件夹映射到宿主机
#             -e COOLQ_ACCOUNT=$COOLQ_ACCOUNT  \   # 酷Q 账号（QQ账号）
#             -e VNC_PASSWD=$VNC_PASSWD \     # nvc 密码
#             -e FORCE_ENV=$FORCE_ENV \       # 强制覆盖原有配置，否则配置不会更新。。
#             -e CQHTTP_USE_HTTP=no \         # 关闭 http api
#             -e CQHTTP_USE_WS_REVERSE=yes  \  # 启用反向 websocket api
#             -e CQHTTP_ACCESS_TOKEN=$CQHTTP_ACCESS_TOKEN  \  # api 连接时需要的 token
#             -e CQHTTP_SECRET=$CQHTTP_SECRET \   # secret 用于数据签名，反向 websocket 中不需要（因为握手阶段没有数据要传输）
#             -e CQHTTP_WS_REVERSE_API_URL=$CQHTTP_WS_REVERSE_API_URL  \
#             -e CQHTTP_WS_REVERSE_EVENT_URL=$CQHTTP_WS_REVERSE_EVENT_URL  \
#             -e CQHTTP_SERVE_DATA_FILES=$CQHTTP_SERVE_DATA_FILES  \  # 允许访问 data 文件夹中的文件
#             richardchien/cqhttp:latest
