#!/usr/bin/env bash


sudo docker stop cqhttp-coolq
sudo docker pull richardchien/cqhttp:latest

# 移除旧镜像
sudo docker rmi $(docker images | grep "none" | awk '{print $3}')

bash run_coolq.sh
