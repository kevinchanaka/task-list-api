// ONLY use this file for database interactions
const taskTable = 'tasks';

export function makeTaskModel({database}) {
  return Object.freeze({
    insert,
    update,
    findByField,
    findAllByField,
    removeByField,
  });

  async function insert(data) {
    // throws error on invalid insert, returns [0] otherwise
    return (await database(taskTable).insert(data));
  }

  async function update(data) {
    // raises error on invalid update, returns number of updated elements
    return (await database(taskTable).where({id: data.id}).update(data));
  }

  async function findByField(obj) {
    // returns single object that has all keys within object
    return (await database(taskTable).select().where(obj).first());
  }

  async function findAllByField(obj) {
    // returns all objects that has all keys within object
    return (await database(taskTable).select().where(obj));
  }

  async function removeByField(obj) {
    // removes entries that match all keys within object
    return (await database(taskTable).where(obj).del());
  }
}
