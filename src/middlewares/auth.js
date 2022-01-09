import {TokenService, UserService} from '../services';
const UNAUTHORIZED = {message: 'Unauthorized'};
const INVALID_TOKEN = {message: 'Invalid token'};

export async function authenticateToken(req, res, next) {
  if (!req.cookies.accessToken) {
    res.status(401).json(UNAUTHORIZED);
    return;
  }
  const accessToken = req.cookies.accessToken;
  const validToken = TokenService.verifyAccessToken(accessToken);
  if (validToken && validToken.userId) {
    req.user = await UserService.getUserById(validToken.userId);
    if (req.user) {
      next();
      return;
    }
  }
  res.status(401).json(INVALID_TOKEN);
}
