const taskSchema = require('../schema/task');
const Task = require('../db/Task');

const TaskService = {
  makeTaskObj(data) {
    const {error, value} = taskSchema.validate(data);
    // If error is undefined, task is invalid
    return {error: error, value: value};
  },

  async createTask(data) {
    const task = this.makeTaskObj(data);
    if (!task.error) {
      await Task.insert(task.value);
    }
    return task;
  },

  async getTasks() {
    return await Task.findAll();
  },

  async getTask(id) {
    return await Task.findById(id);
  },

  async deleteTask(id) {
    await Task.delete(id);
  },

  async modifyTask(data) {
    const task = this.makeTaskObj(data);
    if (!task.error) {
      await Task.update(task.value);
    }
    return task;
  },
};

module.exports = TaskService;

