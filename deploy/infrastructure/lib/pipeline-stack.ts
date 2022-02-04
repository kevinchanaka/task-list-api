import * as cdk from 'aws-cdk-lib';
import {aws_codebuild as codebuild} from 'aws-cdk-lib';
import {aws_codepipeline as codepipeline} from 'aws-cdk-lib';
import {aws_iam as iam} from 'aws-cdk-lib';
import {aws_codepipeline_actions as codepipelineActions} from 'aws-cdk-lib';
import {aws_ec2 as ec2} from 'aws-cdk-lib';
import {aws_ecr as ecr} from 'aws-cdk-lib';
import {CODESTAR_CONNECTION_ARN, EKS_CLUSTER_ARN, SOURCE_REPO_OWNER,
  SOURCE_REPO_NAME, SOURCE_REPO_BRANCH} from '../lib/config';

interface PipelineStackProps extends cdk.StackProps {
  vpc: ec2.IVpc,
  deployVariables: {[key: string]: codebuild.BuildEnvironmentVariable},
}

export class PipelineStack extends cdk.Stack {
  constructor(scope: cdk.App, id: string, props: PipelineStackProps) {
    super(scope, id, props);

    const ecrRepository = new ecr.Repository(this, 'ECRRepository', {
      repositoryName: 'task-list-api',
    });

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
        'ecr:InitiateLayerUpload',
        'ecr:UploadLayerPart',
        'ecr:CompleteLayerUpload',
      ],
    });

    const ecrBuildProject = new codebuild.PipelineProject(
        this, 'TaskListApiBuild', {
          buildSpec: codebuild.BuildSpec.fromSourceFilename(
              'deploy/config/buildspec.yaml'),
          environment: {
            privileged: true,
            buildImage: codebuild.LinuxBuildImage.STANDARD_5_0,
            computeType: codebuild.ComputeType.SMALL,
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

    const eksDeployPolicy = new iam.PolicyStatement({
      effect: iam.Effect.ALLOW,
      resources: [EKS_CLUSTER_ARN],
      actions: [
        'eks:DescribeCluster',
      ],
    });

    const eksDeployProject = new codebuild.PipelineProject(
        this, 'TaskListApiDeploy', {
          buildSpec: codebuild.BuildSpec.fromSourceFilename(
              'deploy/config/buildspec-deploy.yaml'),
          vpc: props.vpc,
          environment: {
            buildImage: codebuild.LinuxBuildImage.STANDARD_5_0,
            computeType: codebuild.ComputeType.SMALL,
          },
          environmentVariables: {
            ECR_REPOSITORY_URI: {
              type: codebuild.BuildEnvironmentVariableType.PLAINTEXT,
              value: ecrRepository.repositoryUri,
            },
            ...props.deployVariables,
          },
        });

    eksDeployProject.addToRolePolicy(eksDeployPolicy);

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

    new codepipeline.Pipeline(this, 'TaskListApiPipeline', {
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
