const {TaskModel} = require('../db');
const makeTaskService = require('./TaskService');
const TaskService = makeTaskService({TaskModel});

module.exports = {TaskService, makeTaskService};
