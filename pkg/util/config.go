package util

import (
	"log"
	"os"
	"time"
)

type Config struct {
	Environment        string
	DbName             string
	DbUser             string
	DbPassword         string
	DbHost             string
	DbPort             string
	AccessTokenSecret  string
	RefreshTokenSecret string
	AccessTokenExpiry  time.Duration
	RefreshTokenExpiry time.Duration
}

func NewConfig() Config {

	appConfig := Config{}

	appConfig.Environment = getEnvVarDefault("ENVIRONMENT", "development")

	appConfig.DbName = getEnvVar("DB_NAME")
	appConfig.DbUser = getEnvVar("DB_USER")
	appConfig.DbPassword = getEnvVar("DB_PASSWORD")
	appConfig.DbHost = getEnvVarDefault("DB_HOST", "127.0.0.1")
	appConfig.DbPort = getEnvVarDefault("DB_PORT", "5432")

	appConfig.AccessTokenSecret = getEnvVar("ACCESS_TOKEN_SECRET")
	appConfig.RefreshTokenSecret = getEnvVar("REFRESH_TOKEN_SECRET")
	appConfig.AccessTokenExpiry = time.Minute * 60
	appConfig.RefreshTokenExpiry = time.Hour * 24 * 3

	if appConfig.Environment == "development" {
		appConfig.AccessTokenExpiry = time.Minute * 10
		appConfig.RefreshTokenExpiry = time.Minute * 20
	}

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
