import {expect} from '../';
import {userId} from '../data';
import {TokenModel, TokenService} from './';

describe('TokenService', () => {
  afterEach(async () => {
    await TokenModel.destroy();
  });

  it('generates valid access token', async () => {
    const accessToken = TokenService.generateAccessToken(userId);
    expect(TokenService.verifyAccessToken(accessToken.token))
        .to.not.equal(undefined);
  });

  it('generates valid refresh token', async () => {
    const refreshToken = await TokenService.generateRefreshToken(userId);
    expect(await TokenService.verifyRefreshToken(refreshToken.token))
        .to.not.equal(undefined);
  });

  it('deletes refresh token', async () => {
    const refreshToken = await TokenService.generateRefreshToken(userId);
    await TokenService.deleteRefreshToken(refreshToken.token);
    expect(await TokenModel.findAllByField({token: refreshToken.token}))
        .to.be.empty;
  });
});


