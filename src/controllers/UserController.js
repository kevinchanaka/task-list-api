import {userSchema, userLoginSchema} from '../validations/user';
const INVALID_USER = {message: 'Invalid user'};
const INVALID_TOKEN = {message: 'Invalid token'};
const INCORRECT_CREDS = {message: 'Incorrect username or password'};
const ALREADY_EXISTS = {message: 'User already exists'};
const LOGOUT_SUCCESS = {message: 'Logout successful'};
const ADDED = {message: 'User registered'};

// TODO: Feel like there is too much business logic here
// would rather move this logic to another service if possible (AuthService)
// TODO: move data validation to middleware

export function makeUserController({UserService, TokenService}) {
  return Object.freeze({
    registerUser,
    loginUser,
    getAccessToken,
    logoutUser,
  });

  async function registerUser(httpRequest) {
    let retVal;
    const {error} = userSchema.validate(httpRequest.body);
    if (error) {
      retVal = {statusCode: 400, body: INVALID_USER};
    } else {
      const user = await UserService.createUser(httpRequest.body);
      if (user) {
        retVal = {statusCode: 200, body: {user: user, ...ADDED}};
      } else {
        retVal = {statusCode: 400, body: ALREADY_EXISTS};
      }
    }
    return retVal;
  }

  async function loginUser(httpRequest) {
    const {error} = userLoginSchema.validate(httpRequest.body);
    if (error) {
      return {statusCode: 400, body: INVALID_USER};
    }
    const validUser = await UserService.validateUserCreds({
      email: httpRequest.body.email,
      password: httpRequest.body.password,
    });
    if (validUser) {
      // valid user, generate and return token
      const accessToken = TokenService.generateAccessToken(validUser.id);
      const refreshToken = await TokenService.
          generateRefreshToken(validUser.id);
      return {
        statusCode: 200,
        body: {
          user: {
            ...validUser,
          },
        },
        cookies: [
          {
            name: 'accessToken',
            value: accessToken.token,
            options: {
              httpOnly: true,
              expires: new Date(accessToken.expiry * 1000),
            },
          },
          {
            name: 'refreshToken',
            value: refreshToken.token,
            options: {
              httpOnly: true,
              expires: new Date(refreshToken.expiry * 1000),
            },
          },
        ],
      };
    }
    return {statusCode: 400, body: INCORRECT_CREDS};
  }

  async function getAccessToken(httpRequest) {
    const refreshToken = httpRequest.cookies.refreshToken;
    if (refreshToken) {
      const validToken = await TokenService.verifyRefreshToken(refreshToken);
      if (validToken) {
        const accessToken = TokenService.generateAccessToken(validToken.userId);
        return {
          statusCode: 200,
          body: {},
          cookies: [
            {
              name: 'accessToken',
              value: accessToken.token,
              options: {
                httpOnly: true,
                expires: new Date(accessToken.expiry * 1000),
              },
            },
          ],
        };
      }
    }
    return {statusCode: 400, body: INVALID_TOKEN};
  }

  async function logoutUser(httpRequest) {
    let retVal = {statusCode: 200, body: LOGOUT_SUCCESS};
    const refreshToken = httpRequest.cookies.refreshToken;
    if (refreshToken) {
      const deleted = await TokenService.deleteRefreshToken(refreshToken);
      if (deleted) {
        retVal = {
          statusCode: 200,
          body: LOGOUT_SUCCESS,
          clearCookies: [
            {
              name: 'accessToken',
              options: {
                httpOnly: true,
              },
            },
            {
              name: 'refreshToken',
              options: {
                httpOnly: true,
              },
            },
          ],
        };
      }
    }
    return retVal;
  }
}
