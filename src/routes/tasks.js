const express = require('express');
const router = express.Router();

const knex = require('knex');
const config = require('../../knexfile')[process.env.NODE_ENV || 'development'];
const database = knex(config);

router.get('/', function(req, res) {
  database('tasks').select().then(function(tasks) {
    res.json(tasks);
  }).catch(function(error) {
    res.json(error);
  });
});

router.get('/:id', function(req, res) {
  database('tasks').select().where({id: req.params.id}).then(function(task) {
    res.json(task);
  }).catch(function(error) {
    res.json(error);
  });
});

router.post('/', function(req, res) {
  console.log(req.body);
  database('tasks').insert({
    'name': req.body.name,
    'description': req.body.description,
  }).then(function(result) {
    res.json(result);
  }).catch(function(error) {
    res.json(error);
  });
});

router.delete('/:id', function(req, res) {
  console.log(req.params.id);
  database('tasks').where({id: req.params.id}).del().then(function(result) {
    res.json(result);
  }).catch(function(error) {
    res.json(error);
  });
});

router.put('/:id', function(req, res) {
  console.log(req.params.id);
  console.log(req.body);
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
