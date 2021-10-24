import {expect} from '../';
import {userId} from '../data';
import {TokenModel, TokenService} from './';

describe('TokenService', () => {
  afterEach(async () => {
    await TokenModel.destroy();
  });

  it('generates valid access token', async () => {
    const token = TokenService.generateAccessToken(userId);
    expect(TokenService.verifyAccessToken(token)).to.not.equal(undefined);
  });

  it('generates valid refresh token', async () => {
    const token = await TokenService.generateRefreshToken(userId);
    expect(await TokenService.verifyRefreshToken(token))
        .to.not.equal(undefined);
  });

  it('deletes refresh token', async () => {
    const token = await TokenService.generateRefreshToken(userId);
    await TokenService.deleteRefreshToken(token);
    expect(await TokenModel.findAllByField({token: token})).to.be.empty;
  });
});


