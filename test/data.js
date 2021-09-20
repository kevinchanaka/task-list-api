export const tasks = [
  {name: 'task1', description: 'desc1'},
  {name: 'task2', description: 'desc2'},
  {name: 'task3', description: 'desc3'},
];

export const invalidTasks = [
  {name: null, description: 'desc1'},
  {name: 'task1', description: null},
  {name: null, description: null},
  {name: 'a'.repeat(31), description: 'b'.repeat(121)},
];
