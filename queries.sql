/* TODO: convert to migrations */

CREATE TABLE users (
  id UUID PRIMARY KEY,
  email VARCHAR(255),
  passwordHash VARCHAR(255)
);

CREATE TABLE refreshtokens (
  token VARCHAR(255) PRIMARY KEY,
  userId UUID,
  expiry BIGINT,
  CONSTRAINT fkRefreshTokenUserId FOREIGN KEY (userId) REFERENCES users(id)
);

CREATE TABLE tasks (
  id UUID PRIMARY KEY,
  name VARCHAR(255),
  description VARCHAR(255),
  completed BOOLEAN,
  createdAt BIGINT,
  updatedAt BIGINT,
  userId UUID,
  CONSTRAINT fkUsersUserId FOREIGN KEY (userId) REFERENCES users(id) 
);

CREATE TABLE labels (
  id UUID PRIMARY KEY,
  name VARCHAR(255),
  colour VARCHAR(7),
  createdAt BIGINT,
  updatedAt BIGINT,
  userId UUID,
  CONSTRAINT fkUsersUserId FOREIGN KEY (userId) references users(id)
);

CREATE TABLE tasks_labels_map (
  id BIGSERIAL PRIMARY KEY,
  taskId UUID,
  labelId UUID,
  CONSTRAINT fkTasksTaskId FOREIGN KEY (taskId) REFERENCES tasks(id),
  CONSTRAINT fkLabelsLabelId FOREIGN KEY (labelId) REFERENCES labels(id)
);

/* Useful Postgres queries */

SELECT * from tasks;
SELECT * from users;
SELECT * from refreshtokens;
SELECT * from tasks_labels_map;
