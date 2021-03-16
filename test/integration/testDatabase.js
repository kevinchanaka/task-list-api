// declare a database and application for testing
const knex = require('knex');

const {makeTaskModel} = require('../../src/db');
const {makeTaskService} = require('../../src/services');
const {makeTaskController} = require('../../src/controllers');
const {makeApp} = require('../../src/app');

// creating test database
const config = require('../../knexfile')['test'];
const database = knex(config);

// creating test app
const TaskModel = makeTaskModel({database});
const TaskService = makeTaskService({TaskModel});
const TaskController = makeTaskController({TaskService});
const app = makeApp({TaskController});

module.exports = {app, database};
