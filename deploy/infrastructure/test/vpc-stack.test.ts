import {expect as expectCDK, matchTemplate, MatchStyle} from '@aws-cdk/assert';
import * as cdk from '@aws-cdk/core';
import {VpcStack} from '../lib/vpc-stack';
import {ENV} from '../lib/config';

// Sample test case below
test('Empty Stack', () => {
  const app = new cdk.App();
  // WHEN
  const stack = new VpcStack(app, 'MyTestStack', {env: ENV});
  // THEN
  expectCDK(stack).to(matchTemplate({
    'Resources': {},
  }, MatchStyle.EXACT));
});
