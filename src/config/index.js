if (process.env.NODE_ENV !== 'production') {
  require('dotenv').config();
}

module.exports = {
  NAME_LENGTH: 30,
  DESCRIPTION_LENGTH: 120,
  UUID_LENGTH: 36,
  HEALTH_ENDPOINT: '/api/v1/health',
  TASKS_ENDPOINT: '/api/v1/tasks',
  PORT: process.env.PORT || 3000,
  NODE_ENV: process.env.NODE_ENV || 'development',
  DB_NAME: process.env.DB_NAME || 'task-list',
  DB_HOST: process.env.DB_HOST,
  DB_PORT: process.env.DB_PORT || 3306,
  DB_USER: process.env.DB_USER,
  DB_PASSWORD: process.env.DB_PASSWORD,
};
