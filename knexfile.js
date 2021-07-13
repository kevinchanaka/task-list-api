const {DB_NAME, DB_HOST, DB_PORT,
  DB_USER, DB_PASSWORD} = require('./src/config');

module.exports = {
  development: {
    client: 'mysql2',
    connection: {
      host: '127.0.0.1',
      port: 33061,
      user: DB_USER,
      password: DB_PASSWORD,
      database: DB_NAME,
    },
  },

  test: {
    client: 'mysql2',
    connection: {
      host: '127.0.0.1',
      port: 33062,
      user: DB_USER,
      password: DB_PASSWORD,
      database: DB_NAME,
    },
  },

  production: {
    client: 'mysql2',
    connection: {
      host: DB_HOST,
      port: DB_PORT,
      user: DB_USER,
      password: DB_PASSWORD,
      database: DB_NAME,
    },
  },
};
