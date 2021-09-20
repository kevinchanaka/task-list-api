import {NAME_LENGTH, DESCRIPTION_LENGTH, UUID_LENGTH} from '../config';
import Joi from 'joi';
import {v4 as uuidv4} from 'uuid';

export const taskSchema = Joi.object({
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
