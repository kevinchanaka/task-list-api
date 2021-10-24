import {tasks, userId} from '../data';
import {expect} from '../';
import {TaskModel, TaskService} from './';

describe('TaskService', () => {
  afterEach(async () => {
    await TaskModel.destroy();
  });

  it('lists tasks', async () => {
    for (const task of tasks) {
      await TaskService.createTask(userId, task);
    }
    const taskList = await TaskService.getTasks(userId);
    expect(taskList.length).to.equal(tasks.length);
    expect(taskList[0]).to.containSubset(tasks[0]);
  });

  it('retrieves a specific task', async () => {
    const task = await TaskService.createTask(tasks[0]);
    const getTask = await TaskService.getTask(task.id);
    expect(getTask).to.containSubset(task);
  });

  it('deletes a task', async () => {
    const task = await TaskService.createTask(userId, tasks[0]);
    const deletedTask = await TaskService.deleteTask(userId, task.id);
    const getTask = await TaskService.getTask(userId, task.id);
    expect(deletedTask).to.equal(task.id);
    expect(getTask).to.be.an('undefined');
  });

  it('modifies an existing task', async () => {
    const task = await TaskService.createTask(userId, tasks[0]);
    const modifiedTask = await TaskService
        .modifyTask(userId, task.id, {...tasks[1]});
    const getTask = await TaskService.getTask(userId, task.id);
    expect(getTask).to.containSubset(modifiedTask);
  });

  it('unable to delete or modify task that does not exist', async () => {
    const task1 = await TaskService.deleteTask(userId, 'foobar');
    expect(task1).to.be.an('undefined');
    const task2 = await TaskService.modifyTask(userId, tasks[0]);
    expect(task2).to.be.an('undefined');
  });
});


