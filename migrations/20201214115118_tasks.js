const {NAME_LENGTH, DESCRIPTION_LENGTH, UUID_LENGTH} = require('../src/config');

exports.up = function(knex) {
  return knex.schema.createTable('tasks', function(table) {
    table.string('id', UUID_LENGTH);
    table.string('name', NAME_LENGTH);
    table.string('description', DESCRIPTION_LENGTH);
  });
};

exports.down = function(knex) {
  return knex.schema.dropTableIfExists('tasks');
};
