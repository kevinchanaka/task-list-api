// Using test database
process.env.NODE_ENV = 'test';

import {app} from '../../src/app';
import {database} from '../../src/db';

export {app, database};
