#!/bin/bash

cat << EOF > .env
DB_NAME=tasklist
DB_USER=task-list
DB_PASSWORD=$(cat /dev/urandom | tr -dc 'a-zA-Z0-9' | fold -w 16 | head -n 1)
DB_HOST=127.0.0.1
DB_PORT=33061
DB_TEST_PORT=33062
EOF