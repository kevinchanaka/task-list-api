-include .env

dev-db : 
	docker run --name task-list-dev-db -d \
	  -e MYSQL_ROOT_PASSWORD=${DB_PASSWORD} \
	  -e MYSQL_DATABASE=${DB_NAME} \
	  -e MYSQL_USER=${DB_USER} \
	  -e MYSQL_PASSWORD=${DB_PASSWORD} \
	  -p 33061:3306 mysql:8

test-db :
	docker run --name task-list-test-db -d \
	  -e MYSQL_ROOT_PASSWORD=${DB_PASSWORD} \
	  -e MYSQL_DATABASE=${DB_NAME} \
	  -e MYSQL_USER=${DB_USER} \
	  -e MYSQL_PASSWORD=${DB_PASSWORD} \
	  -p 33062:3306 mysql:8

start :
	docker start task-list-dev-db task-list-test-db

stop :
	docker stop task-list-dev-db task-list-test-db

all: dev-db test-db

cleanup : stop
	docker rm task-list-dev-db task-list-test-db
