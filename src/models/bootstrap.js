import knex from 'knex';
import knexConfig from '../../knexfile';
import {NODE_ENV, DB_NAME, DB_USER, DB_PASSWORD,
  DB_ADMIN_USER, DB_ADMIN_PASSWORD} from '../config';

const config = knexConfig[NODE_ENV];
config.connection.user = DB_ADMIN_USER,
config.connection.password = DB_ADMIN_PASSWORD;
config.connection.database = '';
const db = knex(config);

(async () => {
  try {
    await db.raw(`CREATE DATABASE IF NOT EXISTS ${DB_NAME}`);
    await db.raw(`CREATE USER IF NOT EXISTS '${DB_USER}'@'%'
        IDENTIFIED BY '${DB_PASSWORD}'`);
    await db.raw(`GRANT ALL ON ${DB_NAME}.* TO '${DB_USER}'@'%'`);
  } catch (error) {
    console.log(error);
  }
  db.destroy();
})();


