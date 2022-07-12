-include .env
.PHONY: all db build app start stop unit-test integration-test clean

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
	ENV=test python -m migrations.bootstrap
	alembic --config migrations/alembic.ini upgrade head
	ENV=test alembic --config migrations/alembic.ini upgrade head

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

unit-test :
	ENV=test python -m unittest -v tests/unit/test_*.py

integration-test :
	ENV=test python -m unittest -v tests/integration/test_*.py

clean : stop
	-docker rm ${db_dev} ${db_test} ${app}
