import logging
import os
from http import HTTPStatus
from urllib.parse import unquote_plus
import json

import boto3

from libs.responses import success_response, error_response

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

sns_client = boto3.client("sns")
sns_arn = os.getenv("SNS_FILE_INFO_TOPIC_ARN")


def process(event, context):
    for record in event["Records"]:
        try:
            message = record["body"]
            size = json.loads(message)["Size"]
            response = sns_client.publish(
                TopicArn=sns_arn,
                Message=message,
                MessageAttributes={
                    "size": {
                        "DataType": "Number",
                        "StringValue": str(size),
                    }
                },
            )
            logger.info(
                f"Send message [{message}] to sns [{sns_arn}] with id={response.get('MessageId')}"
            )
            return success_response(HTTPStatus.OK, "Info message sended")
        except Exception as e:
            logger.exception("Sending message failed!")
            return error_response(HTTPStatus.INTERNAL_SERVER_ERROR, type(e))
