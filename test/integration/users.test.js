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
    expect(res.headers['set-cookie']).to.have.lengthOf(2);
  });

  it('Cannot login with invalid credentials', async () => {
    await UserAPI.registerUser(users[0]);
    const invalidCreds = {
      email: users[0].email,
      password: users[1].password,
    };
    const res = await UserAPI.loginUser(invalidCreds);
    expect(res.statusCode).to.equal(400);
  });

  it('Can fetch new access token for user', async () => {
    await UserAPI.registerUser(users[0]);
    const login = await UserAPI.loginUser({
      email: users[0].email,
      password: users[0].password,
    });
    const res = await UserAPI.getToken(login.headers['set-cookie'][1]);
    expect(res.statusCode).to.equal(200);
    expect(res.headers['set-cookie']).to.have.lengthOf(1);
  });

  it('Can logout user and invalidate token', async () => {
    await UserAPI.registerUser(users[0]);
    const login = await UserAPI.loginUser({
      email: users[0].email,
      password: users[0].password,
    });
    const refreshToken = login.headers['set-cookie'][1];
    const logout = await UserAPI.logoutUser(refreshToken);
    const res = await UserAPI.getToken(refreshToken);
    expect(logout.statusCode).to.equal(200);
    expect(res.statusCode).to.equal(400);
  });
});
