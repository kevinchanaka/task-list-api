const taskSchema = require('../schema/task');
const Task = require('../db/Task');

// TODO:
// Add logic to include id within task metadata, this should be a UUID
// and NOT derived from database

module.exports = class TaskService {
  _taskObj(data) {
    const {error, value} = taskSchema.validate(data);
    if (error) {
      return null;
    }
    return value;
  }

  async createTask(data) {
    let task = this._taskObj(data);
    if (task != null) {
      task = await Task.insert(task);
    }
    return task;
  }

  async getTasks() {
    const tasks = await Task.findAll();
    return tasks;
  }

  async getTask(id) {
    const task = await Task.findById(id);
    return task;
  }

  async deleteTask(id) {
    const removedTask = await Task.delete(id);
    return removedTask;
  }

  async modifyTask({id: _id, ...data}) {
    let task = this._taskObj(data);
    if (task != null) {
      task = await Task.update({id: _id, ...data});
    }
    return task;
  }
};

