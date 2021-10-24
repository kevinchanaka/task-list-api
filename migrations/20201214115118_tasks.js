import {NAME_LENGTH, UUID_LENGTH, DEFAULT_LENGTH} from '../src/config';

export async function up(knex) {
  await knex.schema.createTable('tasks', function(table) {
    table.string('id', UUID_LENGTH).primary();
    table.string('name', NAME_LENGTH);
    table.string('description', DEFAULT_LENGTH);
  });
}

export async function down(knex) {
  await knex.schema.dropTableIfExists('tasks');
}
