package main

import (
	"log"
	"net/http"

	"example/task-list/pkg/server"
	"example/task-list/pkg/service"
	"example/task-list/pkg/store"
	"example/task-list/pkg/util"
)

func main() {
	log.Println("Loading config...")
	config := util.NewConfig()

	log.Println("Loading dependencies...")
	// Declare list of dependencies here (DI)
	appStore := store.NewDatabaseStore(config)
	appService := service.NewService(appStore, config)
	appServer := server.NewServer(appService, config)

	log.Println("Starting server...")
	http.ListenAndServe(":5000", appServer.Router)
}
