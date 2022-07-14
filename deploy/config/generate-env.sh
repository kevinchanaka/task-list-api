#!/bin/bash

generate_string () {
    echo `cat /dev/urandom | tr -dc 'a-zA-Z0-9' | fold -w $1 | head -n 1`
}

cat << EOF > .env
DB_NAME=tasklist
DB_USER=task-list
DB_PASSWORD=$(generate_string 16)
DB_ADMIN_USER=root
DB_ADMIN_PASSWORD=$(generate_string 16)
DB_HOST=127.0.0.1
DB_PORT=33061
DB_TEST_PORT=33062
ACCESS_TOKEN_SECRET=$(generate_string 128)
REFRESH_TOKEN_SECRET=$(generate_string 128)
FLASK_ENV=development
ALEMBIC_CONFIG=migrations/alembic.ini
EOF
