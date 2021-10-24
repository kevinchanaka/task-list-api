import {users, invalidUsers} from '../data';
import {expect} from '../';
import {request, cleanDatabaseTable} from './';
import {USERS_ENDPOINT} from '../../src/config';

async function registerUser(user) {
  return await request.post(`${USERS_ENDPOINT}/register`).send(user);
}

async function loginUser(creds) {
  return await request.post(`${USERS_ENDPOINT}/login`).send(creds);
}

async function getToken(refreshToken) {
  return await request.post(`${USERS_ENDPOINT}/token`)
      .send({token: refreshToken});
}

async function logoutUser(refreshToken) {
  return await request.post(`${USERS_ENDPOINT}/logout`)
      .send({token: refreshToken});
}

describe('Users', () => {
  afterEach(async () => {
    await cleanDatabaseTable('users');
  });

  it('Registers a new user', async () => {
    const response = await registerUser(users[0]);
    expect(response.statusCode).to.equal(200);
  });

  it('Cannot register invalid user', async () => {
    const response = await registerUser(invalidUsers[0]);
    expect(response.statusCode).to.equal(400);
  });

  it('Can login to a specific user', async () => {
    await registerUser(users[0]);
    const login = await loginUser({
      email: users[0].email,
      password: users[0].password,
    });
    expect(login.statusCode).to.equal(200);
    expect(login.body).to.have.property('accessToken');
    expect(login.body).to.have.property('refreshToken');
  });

  it('Cannot login with invalid credentials', async () => {
    await registerUser(users[0]);
    const invalidCreds = {
      email: users[0].email,
      password: users[1].password,
    };
    const login = await loginUser(invalidCreds);
    expect(login.statusCode).to.equal(401);
  });

  it('Can fetch new access token for user', async () => {
    await registerUser(users[0]);
    const login = await loginUser({
      email: users[0].email,
      password: users[0].password,
    });
    const newAccessToken = await getToken(login.body.refreshToken);
    expect(newAccessToken.statusCode).to.equal(200);
    expect(newAccessToken.body).to.have.property('accessToken');
  });

  it('Can logout user and invalidate token', async () => {
    await registerUser(users[0]);
    const login = await loginUser({
      email: users[0].email,
      password: users[0].password,
    });
    const logout = await logoutUser(login.body.refreshToken);
    const oldRefreshTokenTest = await getToken(login.body.refreshToken);
    expect(logout.statusCode).to.equal(200);
    expect(oldRefreshTokenTest.statusCode).to.equal(401);
  });
});
