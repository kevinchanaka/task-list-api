import bcrypt from 'bcrypt';
import {v4 as uuidv4} from 'uuid';
const saltRounds = 10;

export function makeUserService({UserModel}) {
  return Object.freeze({
    createUser,
    getUserById,
    validateUserCreds,
  });

  async function makeUserObj(data) {
    const hash = await bcrypt.hash(data.password, saltRounds);
    const user = {
      id: uuidv4(),
      name: data.name,
      passwordHash: hash,
      email: data.email,
    };
    return user;
  }

  async function getUserById(id) {
    const user = await UserModel.findByField({id: id});
    if (user) {
      return {
        id: user.id,
        name: user.name,
        email: user.email,
      };
    } else {
      return undefined;
    }
  }

  async function createUser(data) {
    // returns user when created, undefined if user does not exist
    if (!await UserModel.findByField({email: data.email})) {
      const user = await makeUserObj(data);
      await UserModel.insert(user);
      return {
        id: user.id,
        name: user.name,
        email: user.email,
      };
    }
  }

  async function validateUserCreds(data) {
    // returns user object if valid, otherwise returns undefined
    const user = await UserModel.findByField({email: data.email});
    if (user && await bcrypt.compare(data.password, user.passwordHash)) {
      return {
        id: user.id,
        name: user.name,
        email: user.email,
      };
    }
  }
}
