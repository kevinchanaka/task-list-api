import createError from 'http-errors';
import express from 'express';
import cookieParser from 'cookie-parser';
import logger from 'morgan';
import {HEALTH_ENDPOINT, TASKS_ENDPOINT,
  USERS_ENDPOINT, LOG_TYPE} from './config';
import {HealthRouter, TasksRouter, UsersRouter} from './routes';

export const app = express();

app.use(logger(LOG_TYPE));
app.use(express.json());
app.use(express.urlencoded({extended: false}));
app.use(cookieParser());

// configuring routes
app.use(HEALTH_ENDPOINT, HealthRouter);
app.use(TASKS_ENDPOINT, TasksRouter);
app.use(USERS_ENDPOINT, UsersRouter);

// catch 404 and forward to error handler
app.use(function(req, res, next) {
  next(createError(404));
});

// error handler
app.use(function(err, req, res, next) {
  const status = err.status || 500;
  res.status(status);
  if (status == 400) {
    res.json({message: 'Invalid data'});
  } else if (status == 404) {
    res.json({message: 'Not found'});
  } else {
    console.log(err.message);
    res.json({message: 'Internal error'});
  }
});
