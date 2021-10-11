#!/usr/bin/env bash
# https://github.com/tiangolo/full-stack-fastapi-postgresql/blob/master/%7B%7Bcookiecutter.project_slug%7D%7D/backend/app/scripts/test.sh

set -e
set -x

pytest --cov=app --cov-report=term-missing app/tests "${@}"