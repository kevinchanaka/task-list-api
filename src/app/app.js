import createError from 'http-errors';
import express from 'express';
import cors from 'cors';
import cookieParser from 'cookie-parser';
import logger from 'morgan';
import {makeRoutes} from './routes';
import {HEALTH_ENDPOINT, TASKS_ENDPOINT} from '../config';

export function makeApp(controllers) {
  const app = express();
  app.use(cors()); // adding cors for testing only
  app.use(logger('dev'));
  app.use(express.json());
  app.use(express.urlencoded({extended: false}));
  app.use(cookieParser());

  // configuring routes
  const {TasksRouter, HealthRouter} = makeRoutes(controllers);
  app.use(HEALTH_ENDPOINT, HealthRouter);
  app.use(TASKS_ENDPOINT, TasksRouter);

  // catch 404 and forward to error handler
  app.use(function(req, res, next) {
    next(createError(404));
  });

  // error handler
  app.use(function(err, req, res, next) {
    res.status(err.status || 500);
    res.json({
      message: err.message,
    });
  });

  return app;
}
