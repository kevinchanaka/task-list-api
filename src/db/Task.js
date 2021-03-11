const database = require('../db');
const taskTable = 'tasks';

const Task = {
  async insert(data) {
    await database(taskTable).insert(data);
  },

  async findAll() {
    return (await database(taskTable).select());
  },

  async findById(id) {
    return (await database(taskTable).select().where({id: id}).first());
  },

  async delete(id) {
    await database(taskTable).where({id: id}).del();
  },

  async update(data) {
    await database(taskTable).where({id: data.id}).update(data);
  },
};

module.exports = Task;
