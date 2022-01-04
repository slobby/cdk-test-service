#!/usr/bin/env python3
import os
import aws_cdk as cdk
from dotenv import load_dotenv

load_dotenv()

from file_service.file_service_stack import FileServiceStack
from sqs_service.sqs_service_stack import SqsServiceStack

print(os.getenv("CDK_DEFAULT_ACCOUNT"))
print(os.getenv("CDK_DEFAULT_REGION"))

app = cdk.App()
file_service_stack = FileServiceStack(
    app,
    "FileServiceStack",
    env=cdk.Environment(
        account=os.getenv("CDK_DEPLOY_ACCOUNT", "892398644316"),
        region=os.getenv("CDK_DEPLOY_REGION", "eu-west-1"),
    ),
)
SqsServiceStack(
    app,
    "SqsServiceStack",
    files_info_queue=file_service_stack.files_info_queue,
    env=cdk.Environment(
        account=os.getenv("CDK_DEFAULT_ACCOUNT"), region=os.getenv("CDK_DEFAULT_REGION")
    ),
)

app.synth()
