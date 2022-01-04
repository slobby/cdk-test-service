import os
from aws_cdk import (
    # Duration,
    Stack,
    aws_sns as sns,
)
from constructs import Construct


class SqsServiceStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, files_info_queue: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)
        file_topic = sns.Topic(self,
                               "fileInfoTopic",
                               display_name="File loaded info",
                               topic_name=os.getenv(
                                   "SNS_FILE_INFO", "service-sns-topic"),
                               )
        file_topic.add_subscription()
