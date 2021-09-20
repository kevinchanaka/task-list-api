const taskTable = 'tasks';

export function makeTaskModel({database}) {
  return Object.freeze({
    insert,
    findAll,
    findById,
    remove,
    update,
  });

  async function insert(data) {
    // throws error on invalid insert, returns [0] otherwise
    return (await database(taskTable).insert(data));
  }

  async function findAll() {
    // returns empty list if nothing is found
    return (await database(taskTable).select());
  }

  async function findById(id) {
    // returns undefined if nothing is found
    // 'where' query returns empty list
    // 'first' returns undefined if list is empty
    return (await database(taskTable).select().where({id: id}).first());
  }

  async function remove(id) {
    // returns number of deleted elements
    return (await database(taskTable).where({id: id}).del());
  }

  async function update(data) {
    // raises error on invalid update, returns number of updated elements
    return (await database(taskTable).where({id: data.id}).update(data));
  }
}
