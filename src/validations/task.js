import {NAME_LENGTH, DEFAULT_LENGTH} from '../config';
import Joi from 'joi';

export const taskSchema = Joi.object({
  name: Joi.string()
      .required()
      .max(NAME_LENGTH),
  description: Joi.string()
      .required()
      .allow('')
      .max(DEFAULT_LENGTH),
});
