const Joi = require('joi');

const task = Joi.object({
  id: Joi.number(),
  name: Joi.string().max(30),
  description: Joi.string().max(120),
});

module.exports = task;
