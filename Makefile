-include .env
.PHONY: all db build app start stop unit-test integration-test clean

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
	  -e MYSQL_ROOT_PASSWORD=${DB_ADMIN_PASSWORD} \
	  -p 33061:3306 \
	  mysql:8
	docker run --name ${db_test} -d \
	  --network ${network} \
	  -e MYSQL_ROOT_PASSWORD=${DB_ADMIN_PASSWORD} \
	  -p 33062:3306 \
	  mysql:8
	sleep 60
	pipenv run bootstrap
	ENV=test pipenv run bootstrap
	pipenv run migrate
	ENV=test pipenv run migrate

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
	  -e ACCESS_TOKEN_SECRET=${ACCESS_TOKEN_SECRET} \
	  -e REFRESH_TOKEN_SECRET=${REFRESH_TOKEN_SECRET} \
	  -p 5000:8000 \
	  ${app}

start :
	-docker start ${db_dev} ${db_test} ${app}

stop :
	-docker stop ${db_dev} ${db_test} ${app}

unit-test :
	ENV=test pipenv run python -m unittest -v tests/unit/test_*.py

integration-test :
	ENV=test pipenv run python -m unittest -v tests/integration/test_*.py

clean : stop
	-docker rm ${db_dev} ${db_test} ${app}
	-docker network rm ${network}
