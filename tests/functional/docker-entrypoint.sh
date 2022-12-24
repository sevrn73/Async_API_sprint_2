#!/bin/sh

exec python manage.py collectstatic --no-input & python manage.py wait_for_db

exec python utils/wait_for_es.py
      & python utils/wait_for_redis.py
      & pytest src