#!/bin/sh -e
# https://github.com/tiangolo/full-stack-fastapi-postgresql/blob/master/%7B%7Bcookiecutter.project_slug%7D%7D/backend/app/scripts/format.sh

set -x

isort --force-single-line-imports app
autoflake --remove-all-unused-imports --recursive --in-place app --exclude=__init__.py
black app
