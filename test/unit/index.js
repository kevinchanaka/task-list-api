import {makeMockModel} from './MockModel';
import {makeTaskService} from '../../src/services';
import {makeTaskController} from '../../src/controllers';

export const TaskModel = makeMockModel();
export const TaskService = makeTaskService({TaskModel});
export const TaskController = makeTaskController({TaskService});
