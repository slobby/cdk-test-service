#!/usr/bin/env python3

import aws_cdk as cdk

from cdk_test_service.cdk_test_service_stack import CdkTestServiceStack


app = cdk.App()
CdkTestServiceStack(app, "cdk-test-service")

app.synth()
