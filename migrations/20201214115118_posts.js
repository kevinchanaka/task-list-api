const {NAME_LENGTH, DESCRIPTION_LENGTH} = require('../config');

exports.up = function(knex) {
  return knex.schema.createTable('tasks', function(table) {
    table.increments('id');
    table.string('name', NAME_LENGTH);
    table.string('description', DESCRIPTION_LENGTH);
  });
};

exports.down = function(knex) {
  return knex.schema.dropTableIfExists('tasks');
};
