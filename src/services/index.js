import {TaskModel} from '../db';
import {makeTaskService} from './TaskService';

export const TaskService = makeTaskService({TaskModel});
export {makeTaskService};
