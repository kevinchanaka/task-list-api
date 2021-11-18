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
    const {refreshToken} = await TokenService.generateRefreshToken(userId);
    expect(await TokenService.verifyRefreshToken(refreshToken))
        .to.not.equal(undefined);
  });

  it('deletes refresh token', async () => {
    const {refreshToken} = await TokenService.generateRefreshToken(userId);
    await TokenService.deleteRefreshToken(refreshToken);
    expect(await TokenModel.findAllByField({token: refreshToken})).to.be.empty;
  });
});


