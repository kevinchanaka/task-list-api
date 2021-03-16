const makeTaskController = require('./TaskController');
const {TaskService} = require('../services');

const TaskController = makeTaskController({TaskService});

module.exports = {TaskController, makeTaskController};
