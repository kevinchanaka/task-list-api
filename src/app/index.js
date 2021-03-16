const {TaskController} = require('../controllers');
const makeApp = require('./app');

const app = makeApp({TaskController});

module.exports = {app, makeApp};
