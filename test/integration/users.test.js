import {users, invalidUsers} from '../data';
import {expect} from '../';
import {cleanDatabaseTable} from './';
import {UserAPI} from './API';

describe('Users', () => {
  afterEach(async () => {
    await cleanDatabaseTable('users');
  });

  it('Registers a new user', async () => {
    const response = await UserAPI.registerUser(users[0]);
    expect(response.statusCode).to.equal(200);
  });

  it('Cannot register invalid user', async () => {
    const response = await UserAPI.registerUser(invalidUsers[0]);
    expect(response.statusCode).to.equal(400);
  });

  it('Can login to a specific user', async () => {
    await UserAPI.registerUser(users[0]);
    const login = await UserAPI.loginUser({
      email: users[0].email,
      password: users[0].password,
    });
    expect(login.statusCode).to.equal(200);
    expect(login.body.user).to.have.property('accessToken');
    expect(login.body.user).to.have.property('refreshToken');
  });

  it('Cannot login with invalid credentials', async () => {
    await UserAPI.registerUser(users[0]);
    const invalidCreds = {
      email: users[0].email,
      password: users[1].password,
    };
    const login = await UserAPI.loginUser(invalidCreds);
    expect(login.statusCode).to.equal(401);
  });

  it('Can fetch new access token for user', async () => {
    await UserAPI.registerUser(users[0]);
    const login = await UserAPI.loginUser({
      email: users[0].email,
      password: users[0].password,
    });
    const newAccessToken = await UserAPI.getToken(login.body.user.refreshToken);
    expect(newAccessToken.statusCode).to.equal(200);
    expect(newAccessToken.body.user).to.have.property('accessToken');
  });

  it('Can logout user and invalidate token', async () => {
    await UserAPI.registerUser(users[0]);
    const login = await UserAPI.loginUser({
      email: users[0].email,
      password: users[0].password,
    });
    const logout = await UserAPI.logoutUser(login.body.user.refreshToken);
    const oldRefreshTokenTest = await UserAPI
        .getToken(login.body.user.refreshToken);
    expect(logout.statusCode).to.equal(200);
    expect(oldRefreshTokenTest.statusCode).to.equal(401);
  });
});
