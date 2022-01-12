/* Implements user authentication */
export function makeAuthService({UserService, TokenService}) {
  async function registerUser(credentials) {
    return await UserService.createUser(credentials);
  }

  async function loginUser(credentials) {
    let retVal;
    const user = await UserService.validateUserCreds({
      email: credentials.email,
      password: credentials.password,
    });
    if (user) {
      const accessToken = TokenService.generateAccessToken(user.id);
      const refreshToken = await TokenService.generateRefreshToken(user.id);
      retVal = {user, accessToken, refreshToken};
    }
    return retVal;
  }

  async function logoutUser(refreshToken) {
    return await TokenService.deleteRefreshToken(refreshToken);
  }

  async function getAccessToken(refreshToken) {
    let retVal;
    const validToken = await TokenService.verifyRefreshToken(refreshToken);
    if (validToken) {
      retVal = TokenService.generateAccessToken(validToken.userId);
    }
    return retVal;
  }

  async function verifyAccessToken(accessToken) {
    let retVal;
    const validToken = TokenService.verifyAccessToken(accessToken);
    if (validToken && validToken.userId) {
      const user = await UserService.getUserById(validToken.userId);
      if (user) {
        retVal = user;
      }
    }
    return retVal;
  }

  return Object.freeze({
    registerUser,
    loginUser,
    logoutUser,
    getAccessToken,
    verifyAccessToken,
  });
}
