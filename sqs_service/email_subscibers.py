"""Module contains sns email subscribers."""
from typing import Mapping
from aws_cdk import aws_sns as sns

#  sns email subscribers with SubscriptionFilter policies
email_subscribers: dict[str, Mapping[str, sns.SubscriptionFilter]] = {
    "aws-condition1@rambler.ru": {
        "size": sns.SubscriptionFilter.numeric_filter(less_than=100)
    },
    "aws-condition2@rambler.ru": {
        "size": sns.SubscriptionFilter.numeric_filter(greater_than_or_equal_to=100)
    },
}
