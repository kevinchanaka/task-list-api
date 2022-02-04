// Stack to create various application specific AWS resources
// TODO: Add cognito user pool here once ready

import * as cdk from 'aws-cdk-lib';
import {aws_iam as iam} from 'aws-cdk-lib';
import {aws_secretsmanager as secretsmanager} from 'aws-cdk-lib';
import {aws_codebuild as codebuild} from 'aws-cdk-lib';
import {EKS_OIDC_PROVIDER_ARN, EKS_CLUSTER_NAME,
  DATABASE_NAME, DATABASE_USER, APP_PORT} from './config';

interface AppStackProps extends cdk.StackProps {
  dbAdminSecret: secretsmanager.ISecret
}

export class AppStack extends cdk.Stack {
  public readonly deployVariables:
    {[key: string]: codebuild.BuildEnvironmentVariable}

  constructor(scope: cdk.App, id: string, props: AppStackProps) {
    super(scope, id, props);

    const accessTokenSecret = new secretsmanager.Secret(this,
        'AccessTokenSecret',
        {
          generateSecretString: {
            excludePunctuation: true,
            passwordLength: 200,
          },
        });

    const refreshTokenSecret = new secretsmanager.Secret(this,
        'RefreshTokenSecret',
        {
          generateSecretString: {
            excludePunctuation: true,
            passwordLength: 200,
          },
        });

    const databaseUserCredentials = new secretsmanager.Secret(this,
        'DatabaseUserCredentials',
        {
          generateSecretString: {
            generateStringKey: 'password',
            secretStringTemplate: JSON.stringify({username: DATABASE_USER}),
          },
        });

    const taskListApiPolicyStatement = new iam.PolicyStatement({
      actions: [
        'cognito-idp:AdminInitiateAuth',
        'cognito-idp:AdminGetUser',
      ],
      effect: iam.Effect.ALLOW,
      resources: ['*'],
    });

    const oidcProvider = iam.OpenIdConnectProvider
        .fromOpenIdConnectProviderArn(
            this, 'OidcProvider', EKS_OIDC_PROVIDER_ARN);

    const provider = EKS_OIDC_PROVIDER_ARN
        .slice(EKS_OIDC_PROVIDER_ARN.indexOf('/') + 1);

    const taskListApiRole = new iam.Role(this, 'TaskListApiRole', {
      assumedBy: new iam.OpenIdConnectPrincipal(oidcProvider, {
        StringEquals: {
          [provider + ':sub']:
              'system:serviceaccount:task-list:task-list-api',
          [provider + ':aud']: 'sts.amazonaws.com',
        },
      }),
      inlinePolicies: {
        taskListApiPolicy: new iam.PolicyDocument({
          statements: [taskListApiPolicyStatement],
        }),
      },
    });

    this.deployVariables = {
      NODE_ENV: {
        type: codebuild.BuildEnvironmentVariableType.PLAINTEXT,
        value: 'production',
      },
      PORT: {
        type: codebuild.BuildEnvironmentVariableType.PLAINTEXT,
        value: APP_PORT,
      },
      DB_ADMIN_USER: {
        type: codebuild.BuildEnvironmentVariableType.SECRETS_MANAGER,
        value: props.dbAdminSecret.secretArn + ':username',
      },
      DB_ADMIN_PASSWORD: {
        type: codebuild.BuildEnvironmentVariableType.SECRETS_MANAGER,
        value: props.dbAdminSecret.secretArn + ':password',
      },
      DB_USER: {
        type: codebuild.BuildEnvironmentVariableType.SECRETS_MANAGER,
        value: databaseUserCredentials.secretArn + ':username',
      },
      DB_PASSWORD: {
        type: codebuild.BuildEnvironmentVariableType.SECRETS_MANAGER,
        value: databaseUserCredentials.secretArn + ':password',
      },
      DB_NAME: {
        type: codebuild.BuildEnvironmentVariableType.PLAINTEXT,
        value: DATABASE_NAME,
      },
      DB_HOST: {
        type: codebuild.BuildEnvironmentVariableType.SECRETS_MANAGER,
        value: props.dbAdminSecret.secretArn + ':host',
      },
      DB_PORT: {
        type: codebuild.BuildEnvironmentVariableType.SECRETS_MANAGER,
        value: props.dbAdminSecret.secretArn + ':port',
      },
      ACCESS_TOKEN_SECRET: {
        type: codebuild.BuildEnvironmentVariableType.SECRETS_MANAGER,
        value: accessTokenSecret.secretArn,
      },
      REFRESH_TOKEN_SECRET: {
        type: codebuild.BuildEnvironmentVariableType.SECRETS_MANAGER,
        value: refreshTokenSecret.secretArn,
      },
      EKS_CLUSTER_NAME: {
        type: codebuild.BuildEnvironmentVariableType.PLAINTEXT,
        value: EKS_CLUSTER_NAME,
      },
      APP_IAM_ROLE_ARN: {
        type: codebuild.BuildEnvironmentVariableType.PLAINTEXT,
        value: taskListApiRole.roleArn,
      },
    };
  }
}
