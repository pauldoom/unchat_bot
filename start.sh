#!/usr/bin/env bash
docker run --network=unchat_default --env-file unchat_bot.env -it unchat-python-bot
# docker-compose --project-name unchat -f docker-compose.yml up -d