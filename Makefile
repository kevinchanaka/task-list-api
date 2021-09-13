-include .env
.PHONY: all db build app start stop clean

network=task-list
db_dev=db-task-list-dev
db_test=db-task-list-test
app=task-list-api

all : db

.env:
	./deploy/config/generate-env.sh

db : .env
	docker network create ${network}
	docker run --name ${db_dev} -d \
	  --network ${network} \
	  -e MYSQL_ROOT_PASSWORD=${DB_PASSWORD} \
	  -e MYSQL_DATABASE=${DB_NAME} \
	  -e MYSQL_USER=${DB_USER} \
	  -e MYSQL_PASSWORD=${DB_PASSWORD} \
	  -p 33061:3306 \
	  mysql:8
	docker run --name ${db_test} -d \
	  --network ${network} \
	  -e MYSQL_ROOT_PASSWORD=${DB_PASSWORD} \
	  -e MYSQL_DATABASE=${DB_NAME} \
	  -e MYSQL_USER=${DB_USER} \
	  -e MYSQL_PASSWORD=${DB_PASSWORD} \
	  -p 33062:3306 \
	  mysql:8
	sleep 60
	npx knex --env development migrate:latest
	npx knex --env test migrate:latest

build :
	docker build -t ${app} .

app : .env
	docker run --name ${app} -d \
	  --network ${network} \
	  -e DB_HOST=${db_dev} \
	  -e DB_NAME=${DB_NAME} \
	  -e DB_PORT=3306 \
	  -e DB_USER=${DB_USER} \
	  -e DB_PASSWORD=${DB_PASSWORD} \
	  -p 3000:3000 \
	  ${app}

start :
	-docker start ${db_dev} ${db_test} ${app}

stop :
	-docker stop ${db_dev} ${db_test} ${app}

clean : stop
	-docker rm ${db_dev} ${db_test} ${app}
	-docker network rm ${network}
