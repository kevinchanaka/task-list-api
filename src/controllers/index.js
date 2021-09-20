import {makeTaskController} from './TaskController';
import {TaskService} from '../services';

export const TaskController = makeTaskController({TaskService});
export {makeTaskController};
