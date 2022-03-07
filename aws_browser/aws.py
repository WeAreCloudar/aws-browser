import dataclasses
import json
from typing import Optional

import boto3
import requests

from .constants import ISSUER


def get_console_url(session: boto3.Session) -> str:
    token = get_signin_token(session)
    return get_signin_url(session, token)


def get_signin_token(session: boto3.Session) -> str:
    credentials = session.get_credentials().get_frozen_credentials()
    if not credentials.token:
        # We assume we're using SSO or AssumeRole, these work out of the box
        raise NotImplementedError("We only support credentials from SSO or STS")

    parameters = {
        "Action": "getSigninToken",
        # If the SessionDuration parameter is missing, then the session defaults to the duration of the sts credentials
        # 'SessionDuration': '',
        "Session": json.dumps(
            {
                "sessionId": credentials.access_key,
                "sessionKey": credentials.secret_key,
                "sessionToken": credentials.token,
            }
        ),
    }
    # Returns a JSON document with a single element named SigninToken.
    response = requests.get(f"https://{_signin_endpoint(session)}/federation", params=parameters)
    return response.json()["SigninToken"]


def get_signin_url(session: boto3.Session, signin_token: str) -> str:
    parameters = {
        "Action": "login",
        "Issuer": ISSUER,
        "Destination": f"https://{_console_endpoint(session)}/",
        "SigninToken": signin_token,
    }
    return requests.Request(url=f"https://{_signin_endpoint(session)}/federation", params=parameters).prepare().url


def get_normalized_caller_identifier(session: boto3.session) -> str:
    sts = session.client("sts")
    arn = Arn(sts.get_caller_identity()["Arn"])

    if arn.service == "iam" and arn.resource_type == "user":
        return f"{arn.account_id}/{arn.resource_id}"
    elif arn.service == "sts" and arn.resource_type == "assumed-role":
        role_name = arn.resource_id.split("/")[0]  # name/session
        return f"{arn.account_id}/{role_name}"


def _get_session() -> boto3.Session:
    return boto3.Session()


def _signin_endpoint(session: boto3.Session) -> str:
    region = session.region_name
    if region and region.startswith("us-gov"):
        return f"{region}.signin.amazonaws-us-gov.com"
    if region and region != "us-east-1":
        return f"{region}.signin.aws.amazon.com"
    return "signin.aws.amazon.com"


def _console_endpoint(session: boto3.Session) -> str:
    region = session.region_name
    if region and region.startswith("us-gov"):
        return f"{region}.console.amazonaws-us-gov.com"
    if region and region != "us-east-1":
        return f"{region}.console.aws.amazon.com"
    return "console.aws.amazon.com"


@dataclasses.dataclass
class Arn:
    "arn:aws:sts::123456789012:assumed-role/my-role-name/my-role-session-name"
    partition: str
    service: str
    region: Optional[str]
    account_id: Optional[str]
    resource_type: str
    resource_id: str

    def __init__(self, arn: str):
        parts = arn.split(":")
        self.partition = parts[1]
        self.service = parts[2]
        self.region = parts[3] if parts[3] != "" else None
        self.account_id = parts[4] if parts[4] != "" else None

        if len(parts) == 7:
            # arn:partition:service:region:account-id:resource-type:resource-id
            self.resource_type = parts[5]
            self.resource_id = parts[6]
        elif len(parts) == 6:
            # arn:partition:service:region:account-id:resource-type/resource-id
            resource_parts = parts[5].split("/", 1)
            self.resource_type = resource_parts[0]
            self.resource_id = resource_parts[1]
