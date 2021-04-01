const {NODE_ENV} = require('../config');
const knex = require('knex');
const config = require('../../knexfile')[NODE_ENV];
const database = knex(config);

const makeTaskModel = require('./TaskModel');
const TaskModel = makeTaskModel({database});

module.exports = {database, TaskModel, makeTaskModel};
