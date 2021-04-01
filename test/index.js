// setting up chai and other required libraries

const chai = require('chai');
const expect = chai.expect;
const chaiSubset = require('chai-subset');
chai.use(chaiSubset);

module.exports = {expect};
