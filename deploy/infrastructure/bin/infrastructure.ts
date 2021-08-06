#!/usr/bin/env node
import 'source-map-support/register';
import * as cdk from '@aws-cdk/core';
import {DatabaseStack} from '../lib/database-stack';
import {PipelineStack} from '../lib/pipeline-stack';
import {VpcStack} from '../lib/vpc-stack';
import {ENV} from '../lib/config';

const app = new cdk.App();
const env = ENV;

const vpcStack = new VpcStack(app, 'VpcStack', {env: env});

const databaseStack = new DatabaseStack(app, 'DatabaseStack', {
  env: env,
  vpc: vpcStack.vpc,
});

new PipelineStack(app, 'PipelineStack', {
  env: env,
  vpc: vpcStack.vpc,
  databasePasswordSecret: databaseStack.databaseAdminPassword,
});
