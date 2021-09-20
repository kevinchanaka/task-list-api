import {Router} from 'express';

function expressCallback(controller) {
  return async (req, res) => {
    const httpRequest = {
      body: req.body,
      query: req.query,
      params: req.params,
      ip: req.ip,
      method: req.method,
      path: req.path,
      headers: {
        'Content-Type': req.get('Content-Type'),
        'Referer': req.get('referer'),
        'User-Agent': req.get('User-Agent'),
      },
    };
    try {
      const httpResponse = await controller(httpRequest);
      if (httpResponse.headers) {
        res.set(httpResponse.headers);
      }
      res.type('json');
      res.status(httpResponse.statusCode).send(httpResponse.body);
    } catch (error) {
      console.log(error);
      res.status(500).send({message: 'An unknown error occured'});
    }
  };
};

export function makeRoutes(controllers) {
  const TasksRouter = new Router();
  const HealthRouter = new Router();

  const TaskController = controllers.TaskController;

  TasksRouter.get('/', expressCallback(TaskController.getTasks));
  TasksRouter.get('/:id', expressCallback(TaskController.getTask));
  TasksRouter.post('/', expressCallback(TaskController.postTask));
  TasksRouter.delete('/:id', expressCallback(TaskController.deleteTask));
  TasksRouter.put('/:id', expressCallback(TaskController.putTask));

  HealthRouter.get('/', (req, res) => {
    res.json({message: 'API is running'});
  });

  return {TasksRouter, HealthRouter};
}
