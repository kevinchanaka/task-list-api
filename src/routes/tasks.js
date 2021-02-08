const {NODE_ENV} = require('../../config');
const express = require('express');
const router = new express.Router();

const knex = require('knex');
const config = require('../../knexfile')[NODE_ENV];
const database = knex(config);

const taskSchema = require('../schema/task');

router.get('/', async (req, res) => {
  try {
    const tasks = await database('tasks').select();
    res.json(tasks);
  } catch (error) {
    console.log(error);
    res.status(500).json({message: 'Internal error'});
  }
});

router.get('/:id', async (req, res) => {
  try {
    const task = await database('tasks').select().where({id: req.params.id})
        .first();
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
  const data = {name: req.body.name, description: req.body.description};
  const validate = taskSchema.validate(data);
  if (validate.error) {
    res.status(404).json({message: 'Invalid task'});
  } else {
    try {
      const addTask = await database('tasks').insert(data);
      res.json({message: 'Task added', id: addTask[0]});
    } catch (error) {
      console.log(error);
      res.status(500).json({message: 'Internal error'});
    }
  }
});

router.delete('/:id', async (req, res) => {
  try {
    await database('tasks').where({id: req.params.id}).del();
    res.json({message: 'Task deleted'});
  } catch (error) {
    console.log(error);
    res.status(500).json({message: 'Internal error'});
  }
});

router.put('/:id', async (req, res) => {
  const data = {name: req.body.name, description: req.body.description};
  const validate = taskSchema.validate(data);
  if (validate.error) {
    res.status(404).json({message: 'Invalid task'});
  } else {
    try {
      await database('tasks').where({id: req.params.id}).update(data);
      res.json({message: 'Task modified'});
    } catch (error) {
      console.log(error);
      res.status(500).json({message: 'Internal error'});
    }
  }
});

module.exports = router;
