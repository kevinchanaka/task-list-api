import * as cdk from 'aws-cdk-lib';
import {aws_rds as rds} from 'aws-cdk-lib';
import {aws_ec2 as ec2} from 'aws-cdk-lib';
import {aws_secretsmanager as secretsmanager} from 'aws-cdk-lib';
import {VPC_LOOKUP_TAGS} from '../lib/config';

export class DatabaseStack extends cdk.Stack {
  public readonly dbAdminSecret: secretsmanager.ISecret;
  public readonly vpc: ec2.IVpc;

  constructor(scope: cdk.App, id: string, props: cdk.StackProps) {
    super(scope, id, props);

    this.vpc = ec2.Vpc.fromLookup(this, 'Vpc', {tags: VPC_LOOKUP_TAGS});

    const databaseSecurityGroup = new ec2.SecurityGroup(
        this, 'DatabaseSecurityGroup', {
          vpc: this.vpc,
          allowAllOutbound: true,
        });

    databaseSecurityGroup.addIngressRule(
        ec2.Peer.ipv4('192.168.0.0/16'),
        ec2.Port.tcp(3306),
    );

    const databaseInstance = new rds.DatabaseInstance(this, 'Database', {
      engine: rds.DatabaseInstanceEngine.mysql({
        version: rds.MysqlEngineVersion.VER_8_0_26,
      }),
      vpc: this.vpc,
      vpcSubnets: {
        subnetType: ec2.SubnetType.PRIVATE_WITH_NAT,
      },
      instanceType: ec2.InstanceType.of(
          ec2.InstanceClass.BURSTABLE3, ec2.InstanceSize.MICRO),
      securityGroups: [databaseSecurityGroup],
      allocatedStorage: 5,
    });

    if (databaseInstance.secret) {
      this.dbAdminSecret = databaseInstance.secret;
    }
  }
}
