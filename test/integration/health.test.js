import {request} from './';
import {expect} from '../';
import {HEALTH_ENDPOINT} from '../../src/config';

describe('Application health', () => {
  it('should be healthy', async () => {
    const res = await request.get(HEALTH_ENDPOINT);
    expect(res.status).to.equal(200);
  });

  it('should return 404 on invalid path', async () => {
    const res = await request.get('/foobar');
    expect(res.status).to.equal(404);
  });
});
