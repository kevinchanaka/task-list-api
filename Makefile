-include .env
PHONY=db run test

QUERIES = $(shell cat queries.sql)
DB_TEST_PORT = 5433

.env :
	./env.sh

db :
	docker run --name db-task-list \
	  --restart unless-stopped \
	  -p ${DB_PORT}:5432 \
	  -e POSTGRES_USER=${DB_USER} \
	  -e POSTGRES_PASSWORD=${DB_PASSWORD} \
	  -e POSTGRES_DB=${DB_NAME} \
	  -d postgres
	sleep 5
	docker exec -u ${DB_USER} db-task-list psql -d ${DB_NAME} -c "$(QUERIES)"

db-shell :
	docker exec -it db-task-list psql -U postgres -d postgres

db-test :
	docker run --name db-task-list-test \
	  --restart unless-stopped \
	  -p ${DB_TEST_PORT}:5432 \
	  -e POSTGRES_USER=${DB_USER} \
	  -e POSTGRES_PASSWORD=${DB_PASSWORD} \
	  -e POSTGRES_DB=${DB_NAME} \
	  -d postgres
	sleep 5
	docker exec -u ${DB_USER} db-task-list-test psql -d ${DB_NAME} -c "$(QUERIES)"

run : .env
	set -o allexport && . ./.env && set +o allexport && gow run cmd/main.go

integration-test: .env
	set -o allexport && . ./.env && set +o allexport && DB_PORT=${DB_TEST_PORT} go test -v ./test
