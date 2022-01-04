#!/usr/bin/env python3
import aws_cdk as cdk
import os
from file_service.file_service_stack import FileServiceStack
from dotenv import load_dotenv
load_dotenv()


app = cdk.App()
FileServiceStack(app, "FileServiceStack",
                 env=cdk.Environment(account=os.getenv(
                     'CDK_DEPLOY_ACCOUNT', '892398644316'), region=os.getenv('CDK_DEPLOY_REGION', 'eu-west-1')),
                 )

app.synth()
