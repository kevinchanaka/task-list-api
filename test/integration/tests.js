import {destroyDatabaseConnection} from './';
import './users.test';
import './health.test';
import './tasks.test';

after(async () => {
  await destroyDatabaseConnection();
});
