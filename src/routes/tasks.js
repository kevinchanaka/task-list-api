const express = require('express');
const router = new express.Router();

const TaskServiceClass = require('../services/TaskService');
const TaskService = new TaskServiceClass();

router.get('/', async (req, res) => {
  try {
    const tasks = await TaskService.getTasks();
    res.json(tasks);
  } catch (error) {
    console.log(error);
    res.status(500).json({message: 'Internal error'});
  }
});

router.get('/:id', async (req, res) => {
  try {
    const task = await TaskService.getTask(req.params.id);
    if (task != null) {
      res.json(task);
    } else {
      res.status(404).json({message: 'Task not found'});
    }
  } catch (error) {
    console.log(error);
    res.status(500).json({message: 'Internal error'});
  }
});

router.post('/', async (req, res) => {
  try {
    const createTask = await TaskService.createTask(req.body);
    if (createTask == null) {
      res.status(404).json({message: 'Invalid task'});
    } else {
      res.json(createTask);
    }
  } catch (error) {
    res.status(500).json({message: 'Internal error'});
  }
});

router.delete('/:id', async (req, res) => {
  try {
    await TaskService.deleteTask(req.params.id);
    res.json({message: 'Task deleted'});
  } catch (error) {
    console.log(error);
    res.status(500).json({message: 'Internal error'});
  }
});

router.put('/:id', async (req, res) => {
  const data = {name: req.body.name, description: req.body.description};
  try {
    const modifyTask = await TaskService
        .modifyTask({id: req.params.id, ...data});
    if (modifyTask == null) {
      res.status(404).json({message: 'Invalid task'});
    } else {
      res.json({message: 'Task modified'});
    }
  } catch (error) {
    res.status(500).json({message: 'Internal error'});
  }
});

module.exports = router;
