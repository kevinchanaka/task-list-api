import {Router} from 'express';
import {authenticateToken} from '../middlewares/auth';
import {TaskController, UserController} from '../controllers';
import {expressCallback} from '../helpers/express-callback';

export const TasksRouter = new Router();
export const HealthRouter = new Router();
export const UsersRouter = new Router();

TasksRouter.get('/', authenticateToken,
    expressCallback(TaskController.getTasks));
TasksRouter.get('/:id', authenticateToken,
    expressCallback(TaskController.getTask));
TasksRouter.post('/', authenticateToken,
    expressCallback(TaskController.postTask));
TasksRouter.delete('/:id', authenticateToken,
    expressCallback(TaskController.deleteTask));
TasksRouter.put('/:id', authenticateToken,
    expressCallback(TaskController.putTask));

UsersRouter.post('/register', expressCallback(UserController.registerUser));
UsersRouter.post('/login', expressCallback(UserController.loginUser));
UsersRouter.post('/token', expressCallback(UserController.getAccessToken));
UsersRouter.post('/logout', expressCallback(UserController.logoutUser));

HealthRouter.get('/', (req, res) => {
  res.json({message: 'API is running'});
});

