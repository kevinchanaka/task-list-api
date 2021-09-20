import {NODE_ENV} from '../config';
import knex from 'knex';
import {knexConfig} from '../../knexfile';
import {makeTaskModel} from './TaskModel';

const config = knexConfig[NODE_ENV];
export const database = knex(config);

export const TaskModel = makeTaskModel({database});
export {makeTaskModel};
