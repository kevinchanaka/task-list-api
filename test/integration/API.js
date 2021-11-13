import {TASKS_ENDPOINT, USERS_ENDPOINT} from '../../src/config';
import {request} from './';

function makeTaskAPI() {
  return Object.freeze({
    addTask,
    getTasks,
    getTask,
    modifyTask,
    deleteTask,
  });

  async function addTask(task) {
    return await request.post(TASKS_ENDPOINT).send(task);
  }

  async function getTasks() {
    return await request.get(TASKS_ENDPOINT);
  }

  async function getTask(taskId) {
    return await request.get(`${TASKS_ENDPOINT}/${taskId}`);
  }

  async function modifyTask(taskId, task) {
    return await request.put(`${TASKS_ENDPOINT}/${taskId}`).send(task);
  }

  async function deleteTask(taskId) {
    return await request.delete(`${TASKS_ENDPOINT}/${taskId}`);
  }
}

function makeUserAPI() {
  return Object.freeze({
    registerUser,
    loginUser,
    getToken,
    logoutUser,
  });

  async function registerUser(user) {
    return await request.post(`${USERS_ENDPOINT}/register`).send(user);
  }

  async function loginUser(creds) {
    return await request.post(`${USERS_ENDPOINT}/login`).send(creds);
  }

  async function getToken(refreshToken) {
    return await request.post(`${USERS_ENDPOINT}/token`)
        .send({token: refreshToken});
  }

  async function logoutUser(refreshToken) {
    return await request.post(`${USERS_ENDPOINT}/logout`)
        .send({token: refreshToken});
  }
}

export const TaskAPI = makeTaskAPI();
export const UserAPI = makeUserAPI();
