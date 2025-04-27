-include .env
PHONY=db run

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

db-shell :
	docker exec -it db-task-list psql -U postgres -d postgres

run : .env
	set -o allexport && . ./.env && set +o allexport && gow run cmd/main.go
