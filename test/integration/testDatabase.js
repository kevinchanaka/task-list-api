process.env.NODE_ENV = 'test';

const {app} = require('../../src/app');
const {database} = require('../../src/db');

module.exports = {app, database};
