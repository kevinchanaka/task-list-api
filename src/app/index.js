import {TaskController} from '../controllers';
import {makeApp} from './app';

export const app = makeApp({TaskController});
export {makeApp};
