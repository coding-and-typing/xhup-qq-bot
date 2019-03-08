## 拆小鹤-QQ-前端

小鹤音形拆字、赛文、成绩记录系统的 QQ 前端（开发中）。

此前端只是一个 xhup-club-api 与酷Q之间的代理层！只处理两边消息格式的转换，不承担任何业务逻辑。


### docker-coolq

先 cd 到 scripts 文件夹内，

1. 启动：`bash run_coolq.sh`
1. 更新并重启：`bash upgrade_and_restart_coolq.sh`
1. 远程 UI：`http://$SERVER_IP:9000/`

配置见 `.env`

