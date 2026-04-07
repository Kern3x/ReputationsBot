#!/bin/sh
set -e

alembic upgrade head
exec python start_bot.py
