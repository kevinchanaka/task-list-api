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
	log.Println("Loading dependencies...")
	// Declare list of dependencies here (DI)
	config := util.NewConfig()
	appStore := store.NewDatabaseStore(config)
	appService := service.NewService(appStore, config)
	appServer := server.NewServer(appService, config)

	log.Printf("Starting server in %v mode...", config.Environment)
	http.ListenAndServe(":5000", appServer.Router)
}
