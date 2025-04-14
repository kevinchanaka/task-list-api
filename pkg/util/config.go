package util

import (
	"log"
	"os"
)

type Config struct {
	DbName             string
	DbUser             string
	DbPassword         string
	DbHost             string
	DbPort             string
	AccessTokenSecret  string
	RefreshTokenSecret string
}

func NewConfig() Config {

	appConfig := Config{}

	appConfig.DbName = getEnvVar("DB_NAME")
	appConfig.DbUser = getEnvVar("DB_USER")
	appConfig.DbPassword = getEnvVar("DB_PASSWORD")
	appConfig.DbHost = getEnvVarDefault("DB_HOST", "127.0.0.1")
	appConfig.DbPort = getEnvVarDefault("DB_PORT", "5432")

	appConfig.AccessTokenSecret = getEnvVar("ACCESS_TOKEN_SECRET")
	appConfig.RefreshTokenSecret = getEnvVar("REFRESH_TOKEN_SECRET")

	return appConfig
}

func getEnvVar(name string) string {
	envVar := os.Getenv(name)
	if envVar == "" {
		log.Fatalf("invalid configuration: environment variable %s not defined", name)
	}
	return envVar
}

func getEnvVarDefault(name string, defaultValue string) string {
	envVar := os.Getenv(name)
	if envVar == "" {
		return defaultValue
	}
	return envVar
}
