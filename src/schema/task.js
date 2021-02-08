const {NAME_LENGTH, DESCRIPTION_LENGTH} = require('../../config');
const Joi = require('joi');

const task = Joi.object({
  name: Joi.string()
      .required()
      .max(NAME_LENGTH),
  description: Joi.string()
      .required()
      .max(DESCRIPTION_LENGTH),
});

module.exports = task;
