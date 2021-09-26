import {v4 as uuidv4} from 'uuid';

export function makeTaskService({TaskModel}) {
  return Object.freeze({
    createTask,
    getTasks,
    getTask,
    deleteTask,
    modifyTask,
  });

  function makeTaskObj(data) {
    const task = {
      id: uuidv4(),
      name: data.name,
      description: data.description,
    };
    return task;
  }

  async function createTask(data) {
    const task = makeTaskObj(data);
    await TaskModel.insert(task);
    return task;
  }

  async function getTasks() {
    return await TaskModel.findAll();
  }

  // retrieves a specific task, returns undefined if task does not exist
  async function getTask(id) {
    return await TaskModel.findById(id);
  }

  // deletes a task, returns undefined if task does not exist
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

  // modifies task, returns modified task if successful
  // otherwise, returns undefined
  async function modifyTask(data) {
    let retVal;
    const currentTask = await getTask(data.id);
    if (currentTask != null) {
      await TaskModel.update(data);
      retVal = data;
    }
    return retVal;
  }
};
