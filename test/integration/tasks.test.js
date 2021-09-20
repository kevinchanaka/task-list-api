import request from 'supertest';
import {tasks, invalidTasks} from '../data';
import {expect} from '../';
import {app, database} from './';
import {TASKS_ENDPOINT} from '../../src/config';

const headers = {'Content-Type': 'application/json'};

describe('Tasks', () => {
  beforeEach(async () => {
    await database('tasks').select().del();
  });

  after(async () => {
    await database.destroy();
  });

  describe('POST tasks', () => {
    it('should be able to add a task', async () => {
      const res = await request(app).post(TASKS_ENDPOINT)
          .set(headers).send(tasks[0]);
      expect(res.status).to.equal(200);
      expect(res.body).to.have.property('id');
    });

    it('should not be able to add invalid tasks', async () => {
      for (const task of invalidTasks) {
        const res = await request(app).post(TASKS_ENDPOINT)
            .set(headers).send(task);
        expect(res.status).to.equal(404);
      }
    });
  });

  describe('GET tasks', () => {
    it('should return all tasks', async () => {
      for (const task of tasks) {
        await request(app).post(TASKS_ENDPOINT).set(headers).send(task);
      }
      const res = await request(app).get(TASKS_ENDPOINT);
      expect(res.status).to.equal(200);
      expect(res.body).to.have.lengthOf(tasks.length);
    });

    it('should return specific task if it exists', async () => {
      const taskId = (await request(app).post(TASKS_ENDPOINT).set(headers)
          .send(tasks[0])).body.id;
      const getTask = await request(app).get(`${TASKS_ENDPOINT}/${taskId}`);
      expect(getTask.status).to.equal(200);
      expect(getTask.body).to.containSubset(tasks[0]);
    });

    it('should return 404 for non-existent task or invalid id', async () => {
      let taskNotExist = await request(app).get(`${TASKS_ENDPOINT}/1`);
      expect(taskNotExist.status).to.equal(404);
      taskNotExist = await request(app).get(`${TASKS_ENDPOINT}/foobar`);
      expect(taskNotExist.status).to.equal(404);
    });
  });

  describe('PUT tasks', () => {
    it('should be able to modify an existing task', async () => {
      const taskId = (await request(app).post(TASKS_ENDPOINT).set(headers)
          .send(tasks[0])).body.id;
      const modifiedTask = tasks[1];
      const modifyTask = await request(app).put(`${TASKS_ENDPOINT}/${taskId}`)
          .set(headers).send(modifiedTask);
      expect(modifyTask.status).to.equal(200);
      const getTask = await request(app).get(`${TASKS_ENDPOINT}/${taskId}`);
      expect(getTask.body).to.containSubset(modifiedTask);
    });

    it('should not be able to make a task invalid', async () => {
      const taskId = (await request(app).post(TASKS_ENDPOINT).set(headers)
          .send(tasks[0])).body.id;
      for (const task of invalidTasks) {
        const modifyTask = await request(app).put(`${TASKS_ENDPOINT}/${taskId}`)
            .set(headers).send(task);
        const getTask = await request(app).get(`${TASKS_ENDPOINT}/${taskId}`);
        expect(modifyTask.status).to.equal(404);
        expect(getTask.body).to.containSubset(tasks[0]);
      }
    });
  });

  describe('DELETE /tasks', () => {
    it('should be able to delete a task', async () => {
      const taskId = (await request(app).post(TASKS_ENDPOINT).set(headers)
          .send(tasks[0])).body.id;
      const delTask = await request(app).delete(`${TASKS_ENDPOINT}/${taskId}`);
      expect(delTask.status).to.equal(200);
      const getTask = await request(app).get(`${TASKS_ENDPOINT}/${taskId}`);
      expect(getTask.status).to.equal(404);
    });
  });
});
