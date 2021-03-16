const taskTable = 'tasks';

function makeTaskModel({database}) {
  return Object.freeze({
    insert,
    findAll,
    findById,
    remove,
    update,
  });

  async function insert(data) {
    await database(taskTable).insert(data);
  }

  async function findAll() {
    return (await database(taskTable).select());
  }

  async function findById(id) {
    return (await database(taskTable).select().where({id: id}).first());
  }

  async function remove(id) {
    await database(taskTable).where({id: id}).del();
  }

  async function update(data) {
    await database(taskTable).where({id: data.id}).update(data);
  }
}

module.exports = makeTaskModel;
