import dotenv from 'dotenv';

if (process.env.NODE_ENV !== 'production') {
  dotenv.config();
}

export const NODE_ENV = process.env.NODE_ENV || 'development';

export const HEALTH_ENDPOINT = '/api/v1/health';
export const TASKS_ENDPOINT = '/api/v1/tasks';
export const PORT = process.env.PORT || 3000;

export const NAME_LENGTH = 30;
export const DESCRIPTION_LENGTH = 120;
export const UUID_LENGTH = 36;

export const DB_NAME = process.env.DB_NAME || 'tasklist';
export const DB_HOST = process.env.DB_HOST || 'localhost';
export const DB_PORT = process.env.DB_PORT || 33061;
export const DB_TEST_PORT = process.env.DB_TEST_PORT || 33062;
export const DB_USER = process.env.DB_USER;
export const DB_PASSWORD = process.env.DB_PASSWORD;
