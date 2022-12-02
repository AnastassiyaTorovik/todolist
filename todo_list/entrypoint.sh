#!/bin/sh

set -e

echo "Waiting for postgres..."

while ! nc -z todo-list-db 5432; do
  sleep 0.1
done

python todo_list/manage.py create_db

exec "$@"