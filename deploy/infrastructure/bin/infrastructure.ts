#!/usr/bin/env node
import * as cdk from 'aws-cdk-lib';
import {DatabaseStack} from '../lib/database-stack';
import {PipelineStack} from '../lib/pipeline-stack';
import {AppStack} from '../lib/app-stack';
import {ENV} from '../lib/config';

const app = new cdk.App();
const env = ENV;

const appStack = new AppStack(app, 'AppStack', {env: env});

const databaseStack = new DatabaseStack(app, 'DatabaseStack', {env: env});

new PipelineStack(app, 'PipelineStack', {
  env: env,
  vpc: databaseStack.vpc,
  dbAdminCredentials: databaseStack.dbAdminCredentials,
  deployVariables: appStack.deployVariables,
});
