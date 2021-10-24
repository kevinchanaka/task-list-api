import {makeMockModel} from './MockModel';
import {makeTaskService} from '../../src/services';
import {makeUserService} from '../../src/services/UserService';
import {makeTokenService} from '../../src/services/TokenService';

export const TaskModel = makeMockModel();
export const TaskService = makeTaskService({TaskModel});

export const TokenModel = makeMockModel();
export const TokenService = makeTokenService({TokenModel});

export const UserModel = makeMockModel();
export const UserService = makeUserService({UserModel});
