const userTable = 'users';

export function makeUserModel({database}) {
  return Object.freeze({
    insert,
    findByField,
  });

  async function insert(data) {
    return (await database(userTable).insert(data));
  }

  async function findByField(obj) {
    return (await database(userTable).select().where(obj).first());
  }
}
