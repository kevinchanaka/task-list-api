import {Router} from 'express';
import {TaskController} from '../controllers';
import {expressCallback} from '../helpers/express-callback';

export const TasksRouter = new Router();
export const HealthRouter = new Router();

TasksRouter.get('/', expressCallback(TaskController.getTasks));
TasksRouter.get('/:id', expressCallback(TaskController.getTask));
TasksRouter.post('/', expressCallback(TaskController.postTask));
TasksRouter.delete('/:id', expressCallback(TaskController.deleteTask));
TasksRouter.put('/:id', expressCallback(TaskController.putTask));

HealthRouter.get('/', (req, res) => {
  res.json({message: 'API is running'});
});

