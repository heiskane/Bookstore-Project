#! /usr/bin/env bash
# https://github.com/tiangolo/full-stack-fastapi-postgresql/blob/master/%7B%7Bcookiecutter.project_slug%7D%7D/backend/app/tests-start.sh

set -e

python /app/app/backend_pre_start.py

bash ./scripts/test.sh "$@"