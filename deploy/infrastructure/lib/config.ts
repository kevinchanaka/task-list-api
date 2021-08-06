const environment = 'production' || process.env.NODE_ENV;

export const ENV = {account: '436501147244', region: 'ap-southeast-2'};
export const SOURCE_REPO_NAME = 'task-list-api';
export const SOURCE_REPO_OWNER = 'kevinchanaka';

export let CODESTAR_CONNECTION_ARN: string;
export let SOURCE_REPO_BRANCH: string;
export let DATABASE_NAME: string;

if (environment == 'production') {
  CODESTAR_CONNECTION_ARN = 'arn:aws:codestar-connections:ap-southeast-2:' +
    '436501147244:connection/0e367578-3062-48ba-9a9a-b1ce675b7720';
  SOURCE_REPO_BRANCH = 'main';
  DATABASE_NAME = 'tasklist';
}
