-include .env
PHONY=db run

.env :
	./env.sh

db :
	docker run --name db-task-list \
	  --restart unless-stopped \
	  -p 5432:5432 \
	  -e POSTGRES_PASSWORD=test123 \
	  -d postgres

db-shell :
	docker exec -it db-task-list psql -U postgres -d postgres

run : .env
	set -o allexport && . ./.env && set +o allexport && gow run cmd/main.go
