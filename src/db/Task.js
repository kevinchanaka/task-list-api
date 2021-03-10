const {NODE_ENV} = require('../config');
const knex = require('knex');
const config = require('../../knexfile')[NODE_ENV];
const database = knex(config);
const taskTable = 'tasks';

// only interacting with DB here, NOTHING ELSE i.e. no data validation
// should be used to implement other methods for relational data
// e.g. retrieving all posts for a given user

class Task {
  async insert(data) {
    const taskId = await database(taskTable).insert(data);
    return {id: taskId[0], ...data};
  }

  async findAll() {
    return (await database(taskTable).select());
  }

  async findById(id) {
    return (await database(taskTable).select().where({id: id}).first());
  }

  async delete(id) {
    const output = await database(taskTable).where({id: id}).del();
    return output;
  }

  async update({id: _id, ...data}) {
    const output = await database(taskTable).where({id: _id}).update(data);
    return output;
  }
}

module.exports = new Task();
