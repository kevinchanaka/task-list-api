import {NAME_LENGTH, DESCRIPTION_LENGTH, UUID_LENGTH} from '../src/config';

export function up(knex) {
  return knex.schema.createTable('tasks', function(table) {
    table.string('id', UUID_LENGTH);
    table.string('name', NAME_LENGTH);
    table.string('description', DESCRIPTION_LENGTH);
  });
}

export function down(knex) {
  return knex.schema.dropTableIfExists('tasks');
}
