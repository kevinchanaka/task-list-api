const NOT_FOUND = {message: 'Task not found'};
const INVALID = {message: 'Invalid task'};
const DELETED = {message: 'Task deleted'};
const MODIFIED = {message: 'Task modified'};

function makeTaskController({TaskService}) {
  return Object.freeze({
    getTasks,
    getTask,
    postTask,
    deleteTask,
    putTask,
  });

  async function getTasks() {
    const tasks = await TaskService.getTasks();
    return {statusCode: 200, body: tasks};
  }

  async function getTask(httpRequest) {
    let retVal;
    const task = await TaskService.getTask(httpRequest.params.id);
    if (task != null) {
      retVal = {statusCode: 200, body: task};
    } else {
      retVal = {statusCode: 404, body: NOT_FOUND};
    }
    return retVal;
  }

  async function postTask(httpRequest) {
    let retVal;
    const createTask = await TaskService.createTask(httpRequest.body);
    if (createTask.error) {
      retVal = {statusCode: 404, body: INVALID};
    } else {
      retVal = {statusCode: 200, body: createTask.value};
    }
    return retVal;
  }

  // TODO: make function return different message if task does not exist
  async function deleteTask(httpRequest) {
    await TaskService.deleteTask(httpRequest.params.id);
    return {statusCode: 200, body: DELETED};
  }

  // TODO: make function return different message if task does not exist
  async function putTask(httpRequest) {
    let retVal;
    const modifyTask = await TaskService
        .modifyTask({id: httpRequest.params.id, ...httpRequest.body});
    if (modifyTask.error) {
      retVal = {statusCode: 404, body: INVALID};
    } else {
      retVal = {statusCode: 200, body: MODIFIED};
    }
    return retVal;
  }
}

module.exports = makeTaskController;
