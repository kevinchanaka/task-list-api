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
      userId: data.userId,
    };
    return task;
  }

  function removeUserId(task) {
    return {
      id: task.id,
      name: task.name,
      description: task.description,
    };
  }

  async function createTask(userId, data) {
    const taskObj = makeTaskObj({
      userId: userId,
      ...data,
    });
    await TaskModel.insert(taskObj);
    return removeUserId(taskObj);
  }

  async function getTasks(userId) {
    const tasks = await TaskModel.findAllByField({userId: userId});
    return tasks.map((task) => removeUserId(task));
  }

  // retrieves a specific task, returns undefined if task does not exist
  async function getTask(userId, taskId) {
    const task = await TaskModel.findByField({userId: userId, id: taskId});
    if (task) {
      return removeUserId(task);
    }
  }

  // deletes a task, returns undefined if task does not exist
  // otherwise, returns ID of deleted task
  async function deleteTask(userId, taskId) {
    let retVal = undefined;
    const task = await getTask(userId, taskId);
    if (task != null) {
      await TaskModel.removeByField({userId: userId, id: taskId});
      retVal = task.id;
    }
    return retVal;
  }

  // modifies task, returns modified task if successful
  // otherwise, returns undefined
  async function modifyTask(userId, taskId, data) {
    const currentTask = await getTask(userId, taskId);
    if (currentTask != null) {
      const updatedTask = {
        id: taskId,
        userId: userId,
        ...data,
      };
      await TaskModel.update(updatedTask);
      return removeUserId(updatedTask);
    }
  }
};
