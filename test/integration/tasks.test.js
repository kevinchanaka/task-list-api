import {tasks, invalidTasks, users} from '../data';
import {expect} from '../';
import {cleanDatabaseTable, setupUser} from './';
import {TaskAPI} from './API';

describe('Tasks', () => {
  afterEach(async () => {
    await cleanDatabaseTable('tasks');
  });

  before(async () => {
    await setupUser(users[0]);
  });

  after(async () => {
    await cleanDatabaseTable('users');
  });

  describe('POST tasks', () => {
    it('should be able to add a task', async () => {
      const res = await TaskAPI.addTask(tasks[0]);
      expect(res.status).to.equal(200);
    });

    it('should not be able to add invalid tasks', async () => {
      for (const task of invalidTasks) {
        const res = await TaskAPI.addTask(task);
        expect(res.status).to.equal(404);
      }
    });
  });

  describe('GET tasks', () => {
    it('should return all tasks', async () => {
      for (const task of tasks) {
        await TaskAPI.addTask(task);
      }
      const res = await TaskAPI.getTasks();
      expect(res.status).to.equal(200);
      expect(res.body.tasks).to.have.lengthOf(tasks.length);
    });

    it('should return specific task if it exists', async () => {
      const taskId = (await TaskAPI.addTask(tasks[0])).body.task.id;
      const res = await TaskAPI.getTask(taskId);
      expect(res.status).to.equal(200);
      expect(res.body.task).to.containSubset(tasks[0]);
    });

    it('should return 404 for non-existent task or invalid id', async () => {
      const res1 = await TaskAPI.getTask('1');
      expect(res1.status).to.equal(404);
      const res2 = await TaskAPI.getTask('foobar');
      expect(res2.status).to.equal(404);
    });
  });

  describe('PUT tasks', () => {
    it('should be able to modify an existing task', async () => {
      const taskId = (await TaskAPI.addTask(tasks[0])).body.task.id;
      const modifiedTask = tasks[1];
      const res1 = await TaskAPI.modifyTask(taskId, modifiedTask);
      expect(res1.status).to.equal(200);
      const res2 = await TaskAPI.getTask(taskId);
      expect(res2.body.task).to.containSubset(modifiedTask);
    });

    it('should not be able to make a task invalid', async () => {
      const taskId = (await TaskAPI.addTask(tasks[0])).body.task.id;
      for (const task of invalidTasks) {
        const res1 = await TaskAPI.modifyTask(taskId, task);
        const res2 = await TaskAPI.getTask(taskId);
        expect(res1.status).to.equal(404);
        expect(res2.body.task).to.containSubset(tasks[0]);
      }
    });
  });

  describe('DELETE /tasks', () => {
    it('should be able to delete a task', async () => {
      const taskId = (await TaskAPI.addTask(tasks[0])).body.task.id;
      const res1 = await TaskAPI.deleteTask(taskId);
      expect(res1.status).to.equal(200);
      const res2 = await TaskAPI.getTask(taskId);
      expect(res2.status).to.equal(404);
    });
  });
});
