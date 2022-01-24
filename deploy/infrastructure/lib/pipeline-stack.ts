import * as cdk from 'aws-cdk-lib';
import {aws_codebuild as codebuild} from 'aws-cdk-lib';
import {aws_codepipeline as codepipeline} from 'aws-cdk-lib';
import {aws_iam as iam} from 'aws-cdk-lib';
import {aws_codepipeline_actions as codepipelineActions} from 'aws-cdk-lib';
import {aws_ec2 as ec2} from 'aws-cdk-lib';
import {aws_ecr as ecr} from 'aws-cdk-lib';
import {CODESTAR_CONNECTION_ARN, SOURCE_REPO_OWNER,
  SOURCE_REPO_NAME, SOURCE_REPO_BRANCH} from '../lib/config';

interface PipelineStackProps extends cdk.StackProps {
  vpc: ec2.IVpc,
  dbAdminCredentials: string,
  deployVariables: {[key: string]: codebuild.BuildEnvironmentVariable},
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
          buildSpec: codebuild.BuildSpec.fromSourceFilename(
              'deploy/config/buildspec.yaml'),
          environment: {
            privileged: true,
          },
          environmentVariables: {
            ECR_REPOSITORY_URI: {
              type: codebuild.BuildEnvironmentVariableType.PLAINTEXT,
              value: ecrRepository.repositoryUri,
            },
            ECR_REGISTRY: {
              type: codebuild.BuildEnvironmentVariableType.PLAINTEXT,
              value: ecrRepository.repositoryUri.split('/')[0],
            },
            ECR_REPOSITORY: {
              type: codebuild.BuildEnvironmentVariableType.PLAINTEXT,
              value: ecrRepository.repositoryUri.split('/')[1],
            },
          },
        });

    ecrBuildProject.addToRolePolicy(ecrAccessPolicy);

    const eksDeployProject = new codebuild.PipelineProject(
        this, 'EKSDeployProject', {
          buildSpec: codebuild.BuildSpec.fromSourceFilename(
              'deploy/config/buildspec-deploy.yaml'),
          vpc: props.vpc,
          environmentVariables: {
            ECR_REPOSITORY_URI: {
              type: codebuild.BuildEnvironmentVariableType.PLAINTEXT,
              value: ecrRepository.repositoryUri,
            },
            DATABASE_ADMIN_CREDENTIALS: {
              type: codebuild.BuildEnvironmentVariableType.SECRETS_MANAGER,
              value: props.dbAdminCredentials,
            },
            ...props.deployVariables,
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
      crossAccountKeys: false,
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
