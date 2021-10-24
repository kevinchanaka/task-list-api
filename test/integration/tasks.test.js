import {tasks, invalidTasks, users} from '../data';
import {expect} from '../';
import {request, cleanDatabaseTable, setupUser} from './';
import {TASKS_ENDPOINT} from '../../src/config';

let userTokenHeader;

// should create taskAPI and userAPI class
async function addTask(userTokenHeader, task) {
  return await request.post(TASKS_ENDPOINT).set(userTokenHeader)
      .send(task);
}

async function getTasks(userTokenHeader) {
  return await request.get(TASKS_ENDPOINT).set(userTokenHeader);
}

async function getTask(userTokenHeader, taskId) {
  return await request.get(`${TASKS_ENDPOINT}/${taskId}`).set(userTokenHeader);
}

async function modifyTask(userTokenHeader, taskId, task) {
  return await request.put(`${TASKS_ENDPOINT}/${taskId}`).set(userTokenHeader)
      .send(task);
}

async function deleteTask(userTokenHeader, taskId) {
  return await request.delete(`${TASKS_ENDPOINT}/${taskId}`)
      .set(userTokenHeader);
}


describe('Tasks', () => {
  afterEach(async () => {
    await cleanDatabaseTable('tasks');
  });

  before(async () => {
    userTokenHeader = await setupUser(users[0]);
  });

  after(async () => {
    await cleanDatabaseTable('users');
  });

  describe('POST tasks', () => {
    it('should be able to add a task', async () => {
      const res = await addTask(userTokenHeader, tasks[0]);
      expect(res.status).to.equal(200);
    });

    it('should not be able to add invalid tasks', async () => {
      for (const task of invalidTasks) {
        const res = await addTask(userTokenHeader, task);
        expect(res.status).to.equal(404);
      }
    });
  });

  describe('GET tasks', () => {
    it('should return all tasks', async () => {
      for (const task of tasks) {
        await addTask(userTokenHeader, task);
      }
      const res = await getTasks(userTokenHeader);
      expect(res.status).to.equal(200);
      expect(res.body.tasks).to.have.lengthOf(tasks.length);
    });

    it('should return specific task if it exists', async () => {
      const taskId = (await addTask(userTokenHeader, tasks[0])).body.task.id;
      const res = await getTask(userTokenHeader, taskId);
      expect(res.status).to.equal(200);
      expect(res.body.task).to.containSubset(tasks[0]);
    });

    it('should return 404 for non-existent task or invalid id', async () => {
      const res1 = await getTask(userTokenHeader, '1');
      expect(res1.status).to.equal(404);
      const res2 = await getTask(userTokenHeader, 'foobar');
      expect(res2.status).to.equal(404);
    });
  });

  describe('PUT tasks', () => {
    it('should be able to modify an existing task', async () => {
      const taskId = (await addTask(userTokenHeader, tasks[0])).body.task.id;
      const modifiedTask = tasks[1];
      const res1 = await modifyTask(userTokenHeader, taskId, modifiedTask);
      expect(res1.status).to.equal(200);
      const res2 = await getTask(userTokenHeader, taskId);
      expect(res2.body.task).to.containSubset(modifiedTask);
    });

    it('should not be able to make a task invalid', async () => {
      const taskId = (await addTask(userTokenHeader, tasks[0])).body.task.id;
      for (const task of invalidTasks) {
        const res1 = await modifyTask(userTokenHeader, taskId, task);
        const res2 = await getTask(userTokenHeader, taskId);
        expect(res1.status).to.equal(404);
        expect(res2.body.task).to.containSubset(tasks[0]);
      }
    });
  });

  describe('DELETE /tasks', () => {
    it('should be able to delete a task', async () => {
      const taskId = (await addTask(userTokenHeader, tasks[0])).body.task.id;
      const res1 = await deleteTask(userTokenHeader, taskId);
      expect(res1.status).to.equal(200);
      const res2 = await getTask(userTokenHeader, taskId);
      expect(res2.status).to.equal(404);
    });
  });
});
