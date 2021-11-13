import defaults from 'superagent-defaults';
import supertest from 'supertest';
import {app} from '../../src/app';
import {database} from '../../src/models';
import {USERS_ENDPOINT} from '../../src/config';

const headers = {'Content-Type': 'application/json'};
const request = defaults(supertest(app));
request.set(headers);

// Defining common functions used in test cases

// clean up DB table
export async function cleanDatabaseTable(table) {
  await database(table).select().del();
}

// sets up users to test protected API endpoints
export async function setupUser(user) {
  await request.post(`${USERS_ENDPOINT}/register`).send(user);
  const res = await request.post(`${USERS_ENDPOINT}/login`).send({
    email: user.email,
    password: user.password,
  });
  request.set({'Authorization': 'Bearer ' + res.body.user.accessToken});
  return {};
}

// destroy database connection (need to run this after test cases)
export async function destroyDatabaseConnection() {
  await database.destroy();
}

export {request};
