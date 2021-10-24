const tokenTable = 'refreshTokens';

export function makeTokenModel({database}) {
  return Object.freeze({
    insert,
    findByField,
    removeByField,
  });

  async function insert(data) {
    return (await database(tokenTable).insert(data));
  }

  async function findByField(obj) {
    return (await database(tokenTable).select().where(obj).first());
  }

  async function removeByField(obj) {
    return (await database(tokenTable).where(obj).del());
  }
}
