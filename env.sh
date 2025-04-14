#!/bin/bash

generate_string () {
    echo `cat /dev/urandom | tr -dc 'a-zA-Z0-9' | fold -w $1 | head -n 1`
}

cat << EOF > .env
DB_NAME=postgres
DB_USER=postgres
DB_PASSWORD=test123
DB_HOST=127.0.0.1
DB_PORT=5432
ACCESS_TOKEN_SECRET=$(generate_string 128)
REFRESH_TOKEN_SECRET=$(generate_string 128)
EOF
