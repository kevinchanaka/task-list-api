import {users, invalidUsers} from '../data';
import {expect} from '../';
import {cleanDatabaseTable} from './';
import {UserAPI} from './API';

describe('Users', () => {
  afterEach(async () => {
    await cleanDatabaseTable('users');
  });

  it('Registers a new user', async () => {
    const res = await UserAPI.registerUser(users[0]);
    expect(res.statusCode).to.equal(200);
  });

  it('Cannot register invalid user', async () => {
    const res = await UserAPI.registerUser(invalidUsers[0]);
    expect(res.statusCode).to.equal(400);
  });

  it('Can login to a specific user', async () => {
    await UserAPI.registerUser(users[0]);
    const res = await UserAPI.loginUser({
      email: users[0].email,
      password: users[0].password,
    });
    expect(res.statusCode).to.equal(200);
    expect(res.body.user).to.have.property('accessToken');
  });

  it('Cannot login with invalid credentials', async () => {
    await UserAPI.registerUser(users[0]);
    const invalidCreds = {
      email: users[0].email,
      password: users[1].password,
    };
    const res = await UserAPI.loginUser(invalidCreds);
    expect(res.statusCode).to.equal(401);
  });

  it('Can fetch new access token for user', async () => {
    await UserAPI.registerUser(users[0]);
    const login = await UserAPI.loginUser({
      email: users[0].email,
      password: users[0].password,
    });
    const res = await UserAPI.getToken(login.headers['set-cookie'][0]);
    expect(res.statusCode).to.equal(200);
    expect(res.body.user).to.have.property('accessToken');
  });

  it('Can logout user and invalidate token', async () => {
    await UserAPI.registerUser(users[0]);
    const login = await UserAPI.loginUser({
      email: users[0].email,
      password: users[0].password,
    });
    const cookie = login.headers['set-cookie'][0];
    const logout = await UserAPI.logoutUser(cookie);
    const res = await UserAPI.getToken(cookie);
    expect(logout.statusCode).to.equal(200);
    expect(res.statusCode).to.equal(401);
  });
});
