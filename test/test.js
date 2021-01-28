const chai = require('chai');
const expect = chai.expect;
const chaiSubset = require('chai-subset');
chai.use(chaiSubset);
const app = require('../src/app');
const request = require('supertest');

const knex = require('knex');
const config = require('../knexfile')[process.env.NODE_ENV || 'development'];
const database = knex(config);

require('dotenv').config();
const headers = {'Content-Type': 'application/json'};
const task = {name: 'task1', description: 'desc1'};
const tasks = [
  {name: 'task1', description: 'desc1'},
  {name: 'task2', description: 'desc2'},
  {name: 'task3', description: 'desc3'},
];

describe('Application health', () => {
  it('should be healthy', async () => {
    const res = await request(app).get('/health');
    expect(res.status).to.equal(200);
  });

  it('should return 404 on invalid path', async () => {
    const res = await request(app).get('/foobar');
    expect(res.status).to.equal(404);
  });
});

describe('Tasks', () => {
  beforeEach(async () => {
    await database('tasks').select().del();
  });

  after(async () => {
    await database.destroy();
  });

  describe('POST /tasks', () => {
    it('should be able to add a task', async () => {
      const res = await request(app).post('/tasks').set(headers).send(task);
      expect(res.status).to.equal(200);
      expect(res.body).to.have.property('id');
      expect(res.body.id).to.be.a('number');
    });

    it('should not be able to pass any null field(s)', async () => {
      const res = await request(app).post('/tasks').set(headers);
      expect(res.status).to.equal(404);
    });
  });

  describe('GET /tasks', () => {
    it('should return all tasks', async () => {
      tasks.forEach(async (task) => {
        await request(app).post('/tasks').set(headers).send(task);
      });
      const res = await request(app).get('/tasks');
      expect(res.status).to.equal(200);
      expect(res.body).to.have.lengthOf(tasks.length);
    });

    it('should return specific task if it exists', async () => {
      const taskId = (await request(app).post('/tasks').set(headers)
          .send(task)).body.id;
      const getTask = await request(app).get(`/tasks/${taskId}`);
      expect(getTask.status).to.equal(200);
      expect(getTask.body).to.containSubset(task);
    });

    it('should return 404 for non-existent task or invalid id', async () => {
      let taskNotExist = await request(app).get('/tasks/1');
      expect(taskNotExist.status).to.equal(404);
      taskNotExist = await request(app).get('/tasks/foobar');
      expect(taskNotExist.status).to.equal(404);
    });
  });

  describe('PUT /tasks', () => {
    it('should be able to modify an existing task', async () => {
      const taskId = (await request(app).post('/tasks').set(headers)
          .send(task)).body.id;
      const modifiedTask = {name: 'task2', description: 'task2'};
      const modifyTask = await request(app).put(`/tasks/${taskId}`)
          .set(headers).send(modifiedTask);
      expect(modifyTask.status).to.equal(200);
      const getTask = await request(app).get(`/tasks/${taskId}`);
      expect(getTask.body).to.containSubset(modifiedTask);
    });
  });

  describe('DELETE /tasks', () => {
    it('should be able to delete a task', async () => {
      const taskId = (await request(app).post('/tasks').set(headers)
          .send(task)).body.id;
      const delTask = await request(app).delete(`/tasks/${taskId}`);
      expect(delTask.status).to.equal(200);
      const getTask = await request(app).get(`/tasks/${taskId}`);
      expect(getTask.status).to.equal(404);
    });
  });
});

