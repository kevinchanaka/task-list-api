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

/* Useful Postgres queries */

SELECT * from tasks;
SELECT * from users;
SELECT * from refreshtokens;
