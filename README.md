## 拆小鹤-QQ-前端

小鹤音形拆字、赛文、成绩记录系统的 QQ 前端（开发中）。

此前端只是一个 xhup-club-api 与酷Q之间的代理层！只处理两边消息格式的转换，不承担任何业务逻辑。

## 开发环境

首先需要确保 xhup-club-api 已经可用，否则 xhup-qq-bot 会一直尝试重连。

1. 在项目根目录下添加配置文件 `.env`，配置模板见 `demo.env`
1. 启动 CoolQ 并安装 CQHttp 插件（Windows），配置好参数。
1. `python run.py` 启动 xhup-qq-bot

## 生产环境部署

1. 在 scripts 中添加配置文件 prod.env，配置模板见 `demo.env`
1. 启动 xhup-qq-bot：`bash scripts/deploy.sh`
1. CoolQ 远程 UI：`http://$SERVER_IP:9000/`

