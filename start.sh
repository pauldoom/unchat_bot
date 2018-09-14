#!/usr/bin/env bash
docker run --network=unchat_default --env-file unchat_bot.env -it unchat-python-bot python service.py $*
