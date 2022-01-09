/* generates JWTs for user authorization */
import jwt from 'jsonwebtoken';
import dayjs from 'dayjs';
import {
  ACCESS_TOKEN_SECRET,
  REFRESH_TOKEN_SECRET,
  REFRESH_TOKEN_EXPIRY,
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
    const expiry = computeExpiryTime(ACCESS_TOKEN_EXPIRY);
    const token = jwt.sign({userId: userId},
        ACCESS_TOKEN_SECRET, {expiresIn: ACCESS_TOKEN_EXPIRY});
    return {
      token: token,
      expiry: expiry,
    };
  }

  async function generateRefreshToken(userId) {
    const expiry = computeExpiryTime(REFRESH_TOKEN_EXPIRY);
    const token = jwt.sign({userId: userId},
        REFRESH_TOKEN_SECRET, {expiresIn: REFRESH_TOKEN_EXPIRY});
    await TokenModel.insert({
      token: token,
      expiry: expiry,
    });
    return {
      token: token,
      expiry: expiry,
    };
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

  function computeExpiryTime(expiryTime) {
    // calculates token expiry time as unix timestamp
    const unit = expiryTime.slice(-1);
    const magnitude = parseInt(expiryTime.slice(0, expiryTime.length - 1));
    return dayjs().add(magnitude, unit).unix();
  }
}
