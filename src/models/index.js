import {NODE_ENV} from '../config';
import knex from 'knex';
import knexConfig from '../../knexfile';
import {makeTaskModel} from './TaskModel';
import {makeUserModel} from './UserModel';
import {makeTokenModel} from './TokenModel';

const config = knexConfig[NODE_ENV];
export const database = knex(config);

export const TaskModel = makeTaskModel({database});
export {makeTaskModel};

export const UserModel = makeUserModel({database});
export {makeUserModel};

export const TokenModel = makeTokenModel({database});
export {makeTokenModel};
