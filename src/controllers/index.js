import {
  TaskService,
  AuthService,
} from '../services';

import {makeTaskController} from './TaskController';
import {makeUserController} from './UserController';

export const TaskController = makeTaskController({TaskService});
export {makeTaskController};

export const UserController = makeUserController({AuthService});
export {makeUserController};
