const express = require('express');
const router = new express.Router();

const knex = require('knex');
const config = require('../../knexfile')[process.env.NODE_ENV || 'development'];
const database = knex(config);

const taskSchema = require('../schema/task');

router.get('/', function(req, res) {
  database('tasks').select().then(function(tasks) {
    res.json(tasks);
  }).catch(function(error) {
    res.json(error);
  });
});

router.get('/:id', function(req, res) {
  database('tasks').select().where({id: req.params.id}).first()
      .then(function(task) {
        if (task != null) {
          res.json(task);
        } else {
          res.status(404).json({message: 'Task not found'});
        }
      }).catch(function(error) {
        res.json(error);
      });
});

router.post('/', function(req, res) {
  const data = {name: req.body.name, description: req.body.description};
  const validate = taskSchema.validate(data);
  if (validate.error) {
    res.status(404).json({message: 'Invalid task'});
  } else {
    database('tasks').insert(data).then(function(result) {
      res.json({message: 'Task added', id: result[0]});
    }).catch(function(error) {
      res.json(error);
    });
  }
});

router.delete('/:id', function(req, res) {
  database('tasks').where({id: req.params.id}).del().then(function(result) {
    res.json(result);
  }).catch(function(error) {
    res.json(error);
  });
});

router.put('/:id', function(req, res) {
  database('tasks').where({id: req.params.id}).update({
    'name': req.body.name,
    'description': req.body.description,
  }).then(function(result) {
    res.json(result);
  }).catch(function(error) {
    res.json(error);
  });
});

module.exports = router;
