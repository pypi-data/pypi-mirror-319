## `cdk-cr-constructs`

This Construct is collect custom resource

### Example for CustomResourceGetEIP

```python
import { App, Stack, CfnOutput, Duration, aws_iam } from 'aws-cdk-lib';
import { CustomResourceGetEIP } from 'cdk-cr-constructs';
const env = {
  region: process.env.CDK_DEFAULT_REGION,
  account: process.env.CDK_DEFAULT_ACCOUNT,
};
const app = new App();
const stack = new Stack(app, 'testing-stack', { env });
const getIps = new CustomResourceGetEIP(stack, 'CustomResourceGetEIP', {
  /**
   * Discovery us-east-1 Elastic Ips.
   */
  regions: ['us-east-1'],
  /**
   * Add Company Ips.
   */
  companyIps: ['1.2.3.4'],
});
const role = new aws_iam.Role(stack, 'DemoRole', {
  assumedBy: new aws_iam.AccountRootPrincipal(),
});
/**
 * Example create an assume role, allow all action from ip address.
*/
role.addToPolicy(new aws_iam.PolicyStatement({
  effect: aws_iam.Effect.ALLOW,
  resources: ['*'],
  actions: ['*'],
  conditions: {
    IpAddress: {
      'aws:SourceIp': getIps.ipList(),
    },
  },
}));
```
