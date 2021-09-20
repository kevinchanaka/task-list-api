import request from 'supertest';
import {expect} from '../';
import {app} from './';
import {HEALTH_ENDPOINT} from '../../src/config';

describe('Application health', () => {
  it('should be healthy', async () => {
    const res = await request(app).get(HEALTH_ENDPOINT);
    expect(res.status).to.equal(200);
  });

  it('should return 404 on invalid path', async () => {
    const res = await request(app).get('/foobar');
    expect(res.status).to.equal(404);
  });
});
