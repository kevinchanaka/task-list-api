const createError = require('http-errors');
const express = require('express');
const cors = require('cors');
const cookieParser = require('cookie-parser');
const logger = require('morgan');
const makeRoutes = require('./routes');
const {HEALTH_ENDPOINT, TASKS_ENDPOINT} = require('../config');

function makeApp({TaskController}) {
  const app = express();
  app.use(cors()); // adding cors for testing only
  app.use(logger('dev'));
  app.use(express.json());
  app.use(express.urlencoded({extended: false}));
  app.use(cookieParser());

  // configuring routes
  const {TasksRouter, HealthRouter} = makeRoutes({TaskController});
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

module.exports = makeApp;
