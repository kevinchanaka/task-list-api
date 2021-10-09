import {makeBaseMethods} from './baseMethods';
const taskTable = 'tasks';

export function makeTaskModel({database}) {
  const baseMethods = makeBaseMethods(database, taskTable);

  return Object.freeze({
    ...baseMethods,
  });
}
