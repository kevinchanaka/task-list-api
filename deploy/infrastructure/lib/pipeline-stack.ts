import * as cdk from '@aws-cdk/core';
import * as codebuild from '@aws-cdk/aws-codebuild';
import * as codepipeline from '@aws-cdk/aws-codepipeline';
import * as iam from '@aws-cdk/aws-iam';
import * as codepipelineActions from '@aws-cdk/aws-codepipeline-actions';
import * as ec2 from '@aws-cdk/aws-ec2';
import * as ecr from '@aws-cdk/aws-ecr';
import {CODESTAR_CONNECTION_ARN, SOURCE_REPO_OWNER,
  SOURCE_REPO_NAME, SOURCE_REPO_BRANCH} from '../lib/config';

interface PipelineStackProps extends cdk.StackProps {
  vpc: ec2.IVpc,
  databasePasswordSecret: string,
}

export class PipelineStack extends cdk.Stack {
  constructor(scope: cdk.App, id: string, props: PipelineStackProps) {
    super(scope, id, props);

    const ecrAccessPolicy = new iam.PolicyStatement({
      effect: iam.Effect.ALLOW,
      resources: ['*'],
      actions: [
        'ecr:GetAuthorizationToken',
        'ecr:GetDownloadUrlForLayer',
        'ecr:BatchCheckLayerAvailability',
        'ecr:BatchGetImage',
        'ecr:BatchDeleteImage',
        'ecr:PutImage',
        'ecr:UploadLayerPart',
      ],
    });

    const ecrRepository = new ecr.Repository(this, 'ECRRepository', {});

    const ecrBuildProject = new codebuild.PipelineProject(
        this, 'ECRBuildProject', {
          buildSpec: codebuild.BuildSpec.fromSourceFilename('buildspec.yaml'),
          environmentVariables: {
            ECR_REPOSITORY_URI: {
              type: codebuild.BuildEnvironmentVariableType.PLAINTEXT,
              value: ecrRepository.repositoryUri,
            },
          },
        });

    ecrBuildProject.addToRolePolicy(ecrAccessPolicy);

    const eksDeployProject = new codebuild.PipelineProject(
        this, 'EKSDeployProject', {
          buildSpec: codebuild.BuildSpec.fromSourceFilename(
              'buildspec-deploy.yaml'),
          vpc: props.vpc,
          environmentVariables: {
            DATABASE_ADMIN_PASSWORD: {
              type: codebuild.BuildEnvironmentVariableType.SECRETS_MANAGER,
              value: props.databasePasswordSecret,
            },
          },
        });

    const sourceAction = new codepipelineActions.
        CodeStarConnectionsSourceAction({
          actionName: 'Source',
          connectionArn: CODESTAR_CONNECTION_ARN,
          output: new codepipeline.Artifact('SourceArtifact'),
          owner: SOURCE_REPO_OWNER,
          repo: SOURCE_REPO_NAME,
          branch: SOURCE_REPO_BRANCH,
        });

    const buildAction = new codepipelineActions.CodeBuildAction({
      actionName: 'Build',
      input: new codepipeline.Artifact('SourceArtifact'),
      project: ecrBuildProject,
    });

    const deployAction = new codepipelineActions.CodeBuildAction({
      actionName: 'Deploy',
      input: new codepipeline.Artifact('SourceArtifact'),
      project: eksDeployProject,
    });

    new codepipeline.Pipeline(this, 'Pipeline', {
      stages: [
        {
          stageName: 'Source',
          actions: [sourceAction],
        },
        {
          stageName: 'Build',
          actions: [buildAction],
        },
        {
          stageName: 'Deploy',
          actions: [deployAction],
        },
      ],
    });
  }
}
