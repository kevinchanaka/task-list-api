import {tasks, invalidTasks} from '../data';
import {expect} from '../';
import {TaskModel, TaskController} from './';

describe('TaskController', () => {
  beforeEach(async () => {
    await TaskModel.destroy();
  });

  it('lists tasks', async () => {
    const response = await TaskController.getTasks();
    expect(response.statusCode).to.equal(200);
  });

  it('adds a valid task', async () => {
    const response = await TaskController.postTask({
      body: tasks[0],
    });
    expect(response.statusCode).to.equal(200);
  });

  it('can modify a task', async () => {
    const response = await TaskController.postTask({
      body: tasks[0],
    });
    expect(response.statusCode).to.equal(200);
    const modifyTask = await TaskController.putTask({
      params: {id: response.body.id},
      body: tasks[1],
    });
    expect(modifyTask.statusCode).to.equal(200);
  });


  it('unable to add an invalid task', async () => {
    const response = await TaskController.postTask({
      body: invalidTasks[0],
    });
    expect(response.statusCode).to.equal(404);
  });

  it('unable to retrieve task that does not exist', async () => {
    const response = await TaskController.getTask({
      params: {id: 'foobar'},
    });
    expect(response.statusCode).to.equal(404);
  });

  it('unable to delete task that does not exist', async () => {
    const response = await TaskController.deleteTask({
      params: {id: 'foobar'},
    });
    expect(response.statusCode).to.equal(404);
  });

  it('unable to modify task that does not exist', async () => {
    const response = await TaskController.putTask({
      params: {id: 'foobar'},
      body: tasks[0],
    });
    expect(response.statusCode).to.equal(404);
  });
});
