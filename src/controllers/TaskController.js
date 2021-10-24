import {taskSchema} from '../validations/task';
const NOT_FOUND = {message: 'Task not found'};
const INVALID = {message: 'Invalid task'};
const DELETED = {message: 'Task deleted'};

export function makeTaskController({TaskService}) {
  return Object.freeze({
    getTasks,
    getTask,
    postTask,
    deleteTask,
    putTask,
  });

  async function getTasks(request) {
    const tasks = await TaskService.getTasks(request.user.id);
    return {statusCode: 200, body: {tasks: tasks}};
  }

  async function getTask(request) {
    let retVal;
    const task = await TaskService.getTask(request.user.id, request.params.id);
    if (task) {
      retVal = {statusCode: 200, body: {task: task}};
    } else {
      retVal = {statusCode: 404, body: NOT_FOUND};
    }
    return retVal;
  }

  async function postTask(request) {
    let retVal;
    const {error} = taskSchema.validate(request.body);
    if (error) {
      retVal = {statusCode: 404, body: INVALID};
    } else {
      const task = await TaskService.createTask(request.user.id,
          request.body);
      retVal = {statusCode: 200, body: {task: task}};
    }
    return retVal;
  }

  async function deleteTask(request) {
    let retVal;
    const taskId = await TaskService.deleteTask(request.user.id,
        request.params.id);
    if (taskId) {
      retVal = {statusCode: 200, body: DELETED};
    } else {
      retVal = {statusCode: 404, body: NOT_FOUND};
    }
    return retVal;
  }

  async function putTask(request) {
    let retVal;
    const {error} = taskSchema.validate(request.body);
    if (error) {
      retVal = {statusCode: 404, body: INVALID};
    } else {
      const modifyTask = await TaskService.modifyTask(request.user.id,
          request.params.id,
          {...request.body},
      );
      if (modifyTask) {
        retVal = {statusCode: 200, body: {task: modifyTask}};
      } else {
        retVal = {statusCode: 404, body: NOT_FOUND};
      }
    }
    return retVal;
  }
}
