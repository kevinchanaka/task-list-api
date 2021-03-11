const {NAME_LENGTH, DESCRIPTION_LENGTH, UUID_LENGTH} = require('../config');
const Joi = require('joi');
const {v4: uuidv4} = require('uuid');

const task = Joi.object({
  id: Joi.string()
      .max(UUID_LENGTH)
      .default(() => uuidv4()),
  name: Joi.string()
      .required()
      .max(NAME_LENGTH),
  description: Joi.string()
      .required()
      .max(DESCRIPTION_LENGTH),
});

module.exports = task;
