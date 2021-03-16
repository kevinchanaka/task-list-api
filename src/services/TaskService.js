const taskSchema = require('../schema/task');

function makeTaskService({TaskModel}) {
  return Object.freeze({
    createTask,
    getTasks,
    getTask,
    deleteTask,
    modifyTask,
  });

  function makeTaskObj(data) {
    const {error, value} = taskSchema.validate(data);
    // If error is undefined, task is invalid
    return {error: error, value: value};
  }

  async function createTask(data) {
    const task = makeTaskObj(data);
    if (!task.error) {
      await TaskModel.insert(task.value);
    }
    return task;
  }

  async function getTasks() {
    return await TaskModel.findAll();
  }

  async function getTask(id) {
    return await TaskModel.findById(id);
  }

  async function deleteTask(id) {
    await TaskModel.remove(id);
  }

  async function modifyTask(data) {
    const task = makeTaskObj(data);
    if (!task.error) {
      await TaskModel.update(task.value);
    }
    return task;
  }
};

module.exports = makeTaskService;

