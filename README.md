## 拆小鹤

小鹤双拼QQ群拆字机器人

使用 nonebot 与 CQ-HTTP-API 与酷Q 通信

## docker 镜像更新

```shell
docker stop cqhttp-coolq
docker pull richardchien/cqhttp:latest

# 移除旧镜像
docker rmi $(docker images | grep "none" | awk '{print $3}')

bash ./flypy_bot/scripts/run_coolq_docker.sh
```

## docker-coolq 远程 UI

`http://$SERVER_IP:9000/`

配置见 `.env`