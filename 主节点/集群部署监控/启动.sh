#!/bin/bash

cd "$(dirname "$0")"

# 启动 Consul agent
consul agent -dev -config-dir=./consul.d &

# 启动 Docker Compose
docker-compose up -d
