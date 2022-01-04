import os
from aws_cdk import (
    Stack,
    aws_sns as sns,
    aws_sqs as sqs,
    aws_lambda as lambda_,
    aws_sns_subscriptions as sns_subscriptions,
)
from constructs import Construct
from aws_cdk.aws_lambda_event_sources import SqsEventSource
from .email_subscibers import email_subscribers


class SqsServiceStack(Stack):
    def __init__(
        self, scope: Construct, construct_id: str, files_info_queue: sqs.Queue, **kwargs
    ) -> None:
        super().__init__(scope, construct_id, **kwargs)
        file_topic = sns.Topic(
            self,
            "fileInfoTopic",
            display_name="File loaded info",
            topic_name=os.getenv("SNS_FILE_INFO", "service-sns-topic"),
        )
        for email, filter in email_subscribers.items():
            file_topic.add_subscription(
                sns_subscriptions.EmailSubscription(email, filter_policy=filter)
            )

        file_handler = lambda_.Function(
            self,
            "sqsHandler",
            runtime=lambda_.Runtime.PYTHON_3_9,
            handler="index.process",
            code=lambda_.Code.from_asset(
                os.path.join(os.path.dirname(__file__), "handler")
            ),
            environment={"SNS_FILE_INFO_TOPIC_ARN": file_topic.topic_arn},
        )

        file_topic.grant_publish(file_handler)
        file_handler.add_event_source(SqsEventSource(files_info_queue, batch_size=5))
