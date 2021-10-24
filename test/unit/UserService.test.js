import {users} from '../data';
import {expect} from '../';
import {UserModel, UserService} from './';

describe('UserService', () => {
  afterEach(async () => {
    await UserModel.destroy();
  });

  it('registers a new user', async () => {
    const user = await UserService.createUser(users[0]);
    expect(user.name).to.equal(users[0].name);
    expect(user.email).to.equal(users[0].email);
  });

  it('validates a user', async () => {
    const user = await UserService.createUser(users[0]);
    const validUser = await UserService.validateUserCreds({
      email: users[0].email,
      password: users[0].password,
    });
    expect(validUser).to.deep.equal(user);
  });

  it('does not register user that already exists', async () => {
    await UserService.createUser(users[0]);
    const user = await UserService.createUser(users[0]);
    expect(user).to.be.equal(undefined);
  });
});


