import os
from aws_cdk import Duration, Stack, aws_sqs as sqs, aws_s3 as s3, aws_lambda as lambda_
from aws_cdk.aws_lambda_event_sources import S3EventSource
from constructs import Construct


class FileServiceStack(Stack):
    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        log_bucket = s3.Bucket(
            self, "logBucket", bucket_name=os.getenv("LOG_BUCKET", "slobby-log-bucket")
        )
        source_bucket = s3.Bucket(
            self,
            "sourceBucket",
            bucket_name=os.getenv("SOURCE_BUCKET", "slobby-source-bucket"),
            server_access_logs_bucket=log_bucket,
            server_access_logs_prefix="file-log/",
        )
        file_handler = lambda_.Function(
            self,
            "fileHandler",
            runtime=lambda_.Runtime.PYTHON_3_9,
            handler="index.process",
            code=lambda_.Code.from_asset(
                os.path.join(os.path.dirname(__file__), "handler")
            ),
            environment={
                "SQS_FILE_INFO": os.getenv("SQS_FILE_INFO", "file-info-queue")
            },
        )
        self.files_info_queue = sqs.Queue(
            self,
            "filesInfoQueue",
            queue_name=os.getenv("SQS_FILE_INFO", "file-info-queue"),
            max_message_size_bytes=1024,
            retention_period=Duration.seconds(360),
            receive_message_wait_time=Duration.seconds(20),
            visibility_timeout=Duration.seconds(360),
        )
        source_bucket.grant_read(file_handler)
        self.files_info_queue.grant_send_messages(file_handler)
        file_handler.add_event_source(
            S3EventSource(
                source_bucket,
                events=[s3.EventType.OBJECT_CREATED],
                filters=[
                    s3.NotificationKeyFilter(
                        prefix=f"{os.getenv('SOURCE_INPUT_FOLDER', 'input')}/",
                        suffix=".txt",
                    )
                ],
            )
        )
        file_handler.add_event_source(
            S3EventSource(
                source_bucket,
                events=[s3.EventType.OBJECT_CREATED],
                filters=[
                    s3.NotificationKeyFilter(
                        prefix=f"{os.getenv('SOURCE_INPUT_FOLDER', 'input')}/",
                        suffix=".csv",
                    )
                ],
            )
        )
