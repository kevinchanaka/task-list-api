import * as cdk from '@aws-cdk/core';
import * as rds from '@aws-cdk/aws-rds';
import * as ec2 from '@aws-cdk/aws-ec2';
import {DATABASE_NAME} from '../lib/config';

interface DatabaseStackProps extends cdk.StackProps {
  vpc: ec2.IVpc
}

export class DatabaseStack extends cdk.Stack {
  public readonly databaseAdminPassword: string;

  constructor(scope: cdk.App, id: string, props: DatabaseStackProps) {
    super(scope, id, props);

    const databaseSecurityGroup = new ec2.SecurityGroup(
        this, 'DatabaseSecurityGroup', {
          vpc: props.vpc,
          allowAllOutbound: true,
        });

    databaseSecurityGroup.addIngressRule(
        ec2.Peer.ipv4('192.168.0.0/16'),
        ec2.Port.tcp(3306),
    );

    const databaseInstance = new rds.DatabaseInstance(this, 'Database', {
      engine: rds.DatabaseInstanceEngine.mysql({
        version: rds.MysqlEngineVersion.of('8.0.25', '8.0'),
      }),
      databaseName: DATABASE_NAME,
      vpc: props.vpc,
      vpcSubnets: {
        subnetType: ec2.SubnetType.PRIVATE,
      },
      instanceType: ec2.InstanceType.of(
          ec2.InstanceClass.BURSTABLE3, ec2.InstanceSize.MICRO),
      securityGroups: [databaseSecurityGroup],
      allocatedStorage: 10,
    });

    if (databaseInstance.secret) {
      this.databaseAdminPassword = databaseInstance.secret.secretArn;
    }
  }
}
