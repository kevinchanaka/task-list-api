import {NAME_LENGTH, DEFAULT_LENGTH} from '../src/config';

export const userId = 'de8ee50a-0633-449c-97e1-e25d77c7e6aa';

export const tasks = [
  {name: 'task1', description: 'desc1'},
  {name: 'task2', description: 'desc2'},
  {name: 'task3', description: 'desc3'},
];

export const invalidTasks = [
  {name: null, description: 'desc1'},
  {name: 'task1', description: null},
  {name: null, description: null},
  {name: 'a'.repeat(NAME_LENGTH + 1),
    description: 'b'.repeat(DEFAULT_LENGTH + 1)},
];

export const users = [
  {name: 'foobar', password: 'foobar123', email: 'foobar@example.com'},
  {name: 'deadbeef', password: 'deadbeef123', email: 'deadbeef@example.com'},
  {name: 'nodejs', password: 'rules', email: 'nodejs@example.com'},
];

export const invalidUsers = [
  {name: null, password: 'foobar123', email: 'foobar@example.com'},
  {name: 'nodejs', password: 'rules', email: 'nodejs'},
];
