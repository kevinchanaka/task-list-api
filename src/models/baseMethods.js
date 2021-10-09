// implements a number of base functions for CRUD database operations

export function makeBaseMethods(database, table) {
  return Object.freeze({
    insert,
    findAll,
    findById,
    remove,
    update,
  });

  async function insert(data) {
    // throws error on invalid insert, returns [0] otherwise
    return (await database(table).insert(data));
  }

  async function findAll() {
    // returns empty list if nothing is found
    return (await database(table).select());
  }

  async function findById(id) {
    // returns undefined if nothing is found
    // 'where' query returns empty list
    // 'first' returns undefined if list is empty
    return (await database(table).select().where({id: id}).first());
  }

  async function remove(id) {
    // returns number of deleted elements
    return (await database(table).where({id: id}).del());
  }

  async function update(data) {
    // raises error on invalid update, returns number of updated elements
    return (await database(table).where({id: data.id}).update(data));
  }
}
