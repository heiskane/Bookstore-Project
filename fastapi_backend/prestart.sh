#! /usr/bin/env bash

# Wait for database to be ready
sleep 10;

# Create tables
python /app/create_tables.py