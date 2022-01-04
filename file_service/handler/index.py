import logging
import os
from typing import Union
from urllib.parse import unquote_plus
import json

import boto3

# from libs.responses import success_json_response, error_json_response

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

s3 = boto3.resource("s3")
QUEUE = os.getenv("SQS_FILE_INFO") or "file-info-queue"
sqs = boto3.resource("sqs")
file_info_queue = sqs.get_queue_by_name(QueueName=QUEUE)


def extract_info(bucket, key) -> Union[None, str]:
    info = None
    try:
        obj = s3.Object(bucket, key)
        iterator = obj.get()["Body"].iter_lines()
        info = next(iterator, "").decode("utf-8")
    except Exception as e:
        logger.error(f"Handling object [{key}] in backet [{bucket}] failed!")
    return info


def process(event, context):
    for record in event["Records"]:
        try:
            bucket = record["s3"]["bucket"]["name"]
            key = unquote_plus(record["s3"]["object"]["key"])
            size = record["s3"]["object"]["size"]
            info = extract_info(bucket, key)
            if info is not None:
                message = {"Bucket": bucket, "File": key, "Size": size, "Info": info}
                response = file_info_queue.send_message(MessageBody=json.dumps(message))
                logger.info(
                    f"Send message [{message}] to sqs [{file_info_queue.url}] with id={response.get('MessageId')}"
                )

        except Exception as e:
            logger.exception("Handling object failed!")
