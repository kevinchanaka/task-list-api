import {UUID_LENGTH, NAME_LENGTH,
  DEFAULT_LENGTH, HASH_LENGTH, TIMESTAMP_LENGTH} from '../src/config';

export async function up(knex) {
  await knex.schema.createTable('users', function(table) {
    table.string('id', UUID_LENGTH).primary(),
    table.string('name', NAME_LENGTH),
    table.string('email', NAME_LENGTH);
    table.string('passwordHash', HASH_LENGTH);
  });
  await knex.schema.alterTable('tasks', function(table) {
    table.string('userId', UUID_LENGTH).references('users.id');
  });
  await knex.schema.createTable('refreshTokens', function(table) {
    table.string('token', DEFAULT_LENGTH);
    table.integer('expiry', TIMESTAMP_LENGTH);
  });
}

export async function down(knex) {
  await knex.schema.alterTable('tasks', function(table) {
    table.dropForeign('userId');
  });
  await knex.schema.dropTableIfExists('refreshTokens');
  await knex.schema.dropTableIfExists('users');
}

