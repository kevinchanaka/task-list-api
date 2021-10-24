/* generates JWTs for user authorization */
import jwt from 'jsonwebtoken';
import {
  ACCESS_TOKEN_SECRET,
  REFRESH_TOKEN_SECRET,
  REFRESH_TOKEN_EXPIRY_DAYS,
  ACCESS_TOKEN_EXPIRY,
} from '../config';

export function makeTokenService({TokenModel}) {
  return Object.freeze({
    generateAccessToken,
    generateRefreshToken,
    deleteRefreshToken,
    verifyAccessToken,
    verifyRefreshToken,
  });

  function generateAccessToken(userId) {
    return jwt.sign({userId: userId},
        ACCESS_TOKEN_SECRET, {expiresIn: ACCESS_TOKEN_EXPIRY});
  }

  async function generateRefreshToken(userId) {
    const expiry = Math.floor(Date.now() / 1000) +
      (60 * 60 * 24 * REFRESH_TOKEN_EXPIRY_DAYS);
    const token = jwt.sign({
      data: {userId: userId},
      exp: expiry,
    }, REFRESH_TOKEN_SECRET);
    await TokenModel.insert({
      token: token,
      expiry: expiry,
    });
    return token;
  }

  async function deleteRefreshToken(token) {
    try {
      const validToken = jwt.verify(token, REFRESH_TOKEN_SECRET);
      if (validToken) {
        return await TokenModel.removeByField({
          token: token,
        });
      }
    } catch (error) {
      return undefined;
    }


    return await TokenModel.removeByField({
      token: token,
    });
  }

  function verifyAccessToken(token) {
    try {
      return jwt.verify(token, ACCESS_TOKEN_SECRET);
    } catch (error) {
      return undefined;
    }
  }

  async function verifyRefreshToken(token) {
    // Token is valid if it can be decrypted, and if it exists in DB
    try {
      const validToken = jwt.verify(token, REFRESH_TOKEN_SECRET);
      if (await TokenModel.findByField({token: token})) {
        return validToken;
      }
    } catch (error) {
      return undefined;
    }
  }
}
