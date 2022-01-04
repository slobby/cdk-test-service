import aws_cdk as core
import aws_cdk.assertions as assertions

from file_service.file_service_stack import CdkTestServiceStack

# example tests. To run these tests, uncomment this file along with the example
# resource in cdk_test_service/cdk_test_service_stack.py
def test_sqs_queue_created():
    app = core.App()
    stack = CdkTestServiceStack(app, "cdk-test-service")
    template = assertions.Template.from_stack(stack)
