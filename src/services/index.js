import {
  TaskModel,
  UserModel,
  TokenModel,
} from '../models';
import {makeTaskService} from './TaskService';
import {makeUserService} from './UserService';
import {makeTokenService} from './TokenService';

export const TaskService = makeTaskService({TaskModel});
export {makeTaskService};

export const UserService = makeUserService({UserModel});
export {makeUserService};

export const TokenService = makeTokenService({TokenModel});
export {makeTokenService};
