#!/bin/sh
set -eu
python3 -m json.tool data/projects.json >/dev/null
docker compose config >/dev/null
docker compose up -d --build
sleep 2
curl -f http://127.0.0.1:8088/ >/dev/null
curl -f http://127.0.0.1:8088/data/projects.json >/dev/null
echo "PJ-CORE Control запущен: http://127.0.0.1:8088"
