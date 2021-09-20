import {taskSchema} from '../schema/task';

export function makeTaskService({TaskModel}) {
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
    if (task.error == null) {
      await TaskModel.insert(task.value);
    }
    return task;
  }

  async function getTasks() {
    return await TaskModel.findAll();
  }

  // retrieves a specific task, returns undefined if task does not exist
  async function getTask(id) {
    return await TaskModel.findById(id);
  }

  // deletes a task, returns undefined if task does not exists
  // otherwise, returns ID of deleted task
  async function deleteTask(id) {
    let retVal;
    const task = await getTask(id);
    if (task != null) {
      await TaskModel.remove(id);
      retVal = id;
    }
    return retVal;
  }

  // modifies task, returns full modified task if successful
  // otherwise, returns undefined
  async function modifyTask(data) {
    let retVal;
    const currentTask = await getTask(data.id);
    if (currentTask != null) {
      const updatedTask = makeTaskObj(data);
      if (updatedTask.error == null) {
        await TaskModel.update(updatedTask.value);
        retVal = updatedTask;
      }
    }
    return retVal;
  }
};
