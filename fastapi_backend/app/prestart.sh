#! /usr/bin/env bash

# Wait for database to be ready
python /app/app/backend_pre_start.py

# Run migrations
alembic upgrade head