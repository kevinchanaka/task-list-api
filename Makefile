-include .env
.PHONY: all db build app start stop clean test

db_dev=db-task-list-dev
db_test=db-task-list-test
app=task-list-api

all : db

.env:
	./deploy/config/generate-env.sh

db : .env
	docker run --name ${db_dev} -d \
	  -e MYSQL_ROOT_PASSWORD=${DB_ADMIN_PASSWORD} \
	  -p 33061:3306 \
	  mysql:8
	docker run --name ${db_test} -d \
	  -e MYSQL_ROOT_PASSWORD=${DB_ADMIN_PASSWORD} \
	  -p 33062:3306 \
	  mysql:8
	sleep 60
	python -m migrations.bootstrap

build :
	docker build -t ${app} .

app : .env
	docker run --name ${app} -d \
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
