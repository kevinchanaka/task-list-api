
exports.up = function(knex) {
  return knex.schema.createTable('tasks', function(table) {
    table.increments('id');
    table.string('name', 30);
    table.string('description', 120);
  });
};

exports.down = function(knex) {
  return knex.schema.dropTableIfExists('tasks');
};
