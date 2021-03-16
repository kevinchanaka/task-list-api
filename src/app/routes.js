const express = require('express');
const expressCallback = require('../helpers/express-callback');

function makeRoutes({TaskController}) {
  const TasksRouter = new express.Router();
  const HealthRouter = new express.Router();

  TasksRouter.get('/', expressCallback(TaskController.getTasks));
  TasksRouter.get('/:id', expressCallback(TaskController.getTask));
  TasksRouter.post('/', expressCallback(TaskController.postTask));
  TasksRouter.delete('/:id', expressCallback(TaskController.deleteTask));
  TasksRouter.put('/:id', expressCallback(TaskController.putTask));

  HealthRouter.get('/', (req, res) => {
    res.json({message: 'API is running'});
  });

  return {TasksRouter, HealthRouter};
}

module.exports = makeRoutes;
