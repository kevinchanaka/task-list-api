const {NODE_ENV} = require('../config');
const knex = require('knex');
const config = require('../../knexfile')[NODE_ENV];
const database = knex(config);

module.exports = database;
