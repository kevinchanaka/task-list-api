const Joi = require('joi');

const task = Joi.object({
  name: Joi.string()
      .required()
      .max(30),
  description: Joi.string()
      .required()
      .max(120),
});

module.exports = task;
