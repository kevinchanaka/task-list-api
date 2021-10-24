import dotenv from 'dotenv';

export let LOG_TYPE;

if (process.env.NODE_ENV == 'production') {
  LOG_TYPE = 'combined';
} else {
  LOG_TYPE = 'dev';
  dotenv.config();
}

export const NODE_ENV = process.env.NODE_ENV || 'development';
export const HEALTH_ENDPOINT = '/api/v1/health';
export const TASKS_ENDPOINT = '/api/v1/tasks';
export const USERS_ENDPOINT = '/api/v1/users';
export const PORT = process.env.PORT || 3000;

export const NAME_LENGTH = 60;
export const UUID_LENGTH = 36;
export const HASH_LENGTH = 60;
export const TIMESTAMP_LENGTH = 11;
export const DEFAULT_LENGTH = 255;

export const DB_NAME = process.env.DB_NAME || 'tasklist';
export const DB_HOST = process.env.DB_HOST || 'localhost';
export const DB_PORT = process.env.DB_PORT || 33061;
export const DB_TEST_PORT = process.env.DB_TEST_PORT || 33062;
export const DB_USER = process.env.DB_USER;
export const DB_PASSWORD = process.env.DB_PASSWORD;

export const ACCESS_TOKEN_SECRET = process.env.ACCESS_TOKEN_SECRET;
export const ACCESS_TOKEN_EXPIRY = '5m';
export const REFRESH_TOKEN_SECRET = process.env.REFRESH_TOKEN_SECRET;
export const REFRESH_TOKEN_EXPIRY_DAYS = 1;
