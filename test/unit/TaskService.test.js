import {tasks, invalidTasks} from '../data';
import {expect} from '../';
import {TaskModel, TaskService} from './';

describe('TaskService', () => {
  beforeEach(async () => {
    await TaskModel.destroy();
  });

  it('adds a valid task', async () => {
    const task = await TaskService.createTask(tasks[0]);
    expect(task.value).to.containSubset(tasks[0]);
    expect(task.error).to.be.an('undefined');
  });

  it('unable to add an invalid task', async () => {
    const invalidTask = await TaskService.createTask(invalidTasks[0]);
    expect(invalidTask.error).to.not.be.an('undefined');
  });

  it('lists tasks', async () => {
    for (const task of tasks) {
      await TaskService.createTask(task);
    }
    const taskList = await TaskService.getTasks();
    expect(taskList).to.be.a('array');
    expect(taskList.length).to.equal(tasks.length);
    expect(taskList[0]).to.containSubset(tasks[0]);
  });

  it('retrieves a specific task', async () => {
    const task = await TaskService.createTask(tasks[0]);
    const getTask = await TaskService.getTask(task.value.id);
    expect(getTask).to.containSubset(task.value);
  });

  it('deletes a task', async () => {
    const addedTasks = [];
    for (const task of tasks) {
      const addTask = await TaskService.createTask(task);
      addedTasks.push(addTask.value);
    }
    const deletedTask = await TaskService.deleteTask(addedTasks[1].id);
    const getTask = await TaskService.getTask(addedTasks[1].id);
    expect(getTask).to.be.an('undefined');
    expect(deletedTask).to.equal(addedTasks[1].id);
  });

  it('modifies an existing task', async () => {
    const task = await TaskService.createTask(tasks[0]);
    const modifiedTask = await TaskService
        .modifyTask({id: task.value.id, ...tasks[1]});
    const getTask = await TaskService.getTask(task.value.id);
    expect(getTask).to.containSubset(modifiedTask.value);
  });

  it('unable to delete or modify task that does not exist', async () => {
    const task1 = await TaskService.deleteTask('foobar');
    expect(task1).to.be.an('undefined');
    const task2 = await TaskService.modifyTask(tasks[0]);
    expect(task2).to.be.an('undefined');
  });
});


