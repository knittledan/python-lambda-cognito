import sys
import logging
import boto3


sys.path.insert(0, '.serverless/requirements')
from session.cognito import IdentityPool
from util.exceptions import NotAuthorizedException
from util.extract import callback_url, authorization_token
from config.environment_config import EnvironmentConfig
from data.s3_client import S3
from session.user import User
from config.logging_config import LoggingConfig
from web import render


log           = None  # type: logging.Logger
s3_client     = None  # type: S3
user          = None  # type: User
identity_pool = None  # type: IdentityPool
env           = EnvironmentConfig()


def setup():
    global log
    global s3_client
    global user
    global identity_pool

    print("setting up")
    LoggingConfig()
    log = logging.getLogger()
    log.info("logger set")
    log.setLevel(logging.INFO)
    log.info(f"Config: {repr(env)}")

    boto3.setup_default_session(aws_access_key_id=env.aws_key, aws_secret_access_key=env.aws_secret, region_name=env.region)
    log.info("boto session is set")

    s3_client = S3(env.bucket_name)
    log.info("s3_client is set")
    user = User(env.cognito_client_id, env.cognito_secret, env.cognito_region)
    log.info("user class set")
    identity_pool = IdentityPool(env.cognito_pool_id, env.cognito_client_id, env.cognito_region)
    log.info("identity_pool set")


def index(event, context):
    try:
        return dict(
            statusCode=200,
            body=render.index(),
            headers={'Content-Type': 'text/html; charset=utf-8'}
        )
    except Exception as e:
        return dict(
            statusCode=500,
            body=str(e)
        )


def edit(event, context):
    try:
        setup()
        print(event)
        query_params = event.get('queryStringParameters', {})
        access_token = authorization_token(event)

        if query_params and query_params.get('code') and query_params.get('state'):
            access_code  = query_params.get('code')
            access_state = query_params.get('state')
            redirect_uri = callback_url(event)
            user.start_session(identity_pool.token_url, access_code, redirect_uri, access_state)
            access_token = user.access_token
        elif access_token:
            user.verify(access_token)
        else:
            raise NotAuthorizedException

        return dict(
            statusCode=200,
            body="Fuck yeah",
            headers={"Authorization": f'Bearer {access_token}'}
        )
    except NotAuthorizedException as e:
        log.exception(e)
        return dict(
            statusCode=302,
            body="Not Authorized",
            headers={"Location": identity_pool.authorize_url}
        )
    except Exception as e:
        log.exception(e)


# event = {'body': None,
#  'headers': {'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
#              'Authorization': 'Bearer ssFBMaebIVeFcumCUUvELF1wzaNVJRQ1XA5IalKHc1498FshEe1TWyLkdM16MM3w',
#              'Accept-Encoding': 'gzip, deflate, br',
#              'Accept-Language': 'en-US,en;q=0.5',
#              'CloudFront-Forwarded-Proto': 'https',
#              'CloudFront-Is-Desktop-Viewer': 'true',
#              'CloudFront-Is-Mobile-Viewer': 'false',
#              'CloudFront-Is-SmartTV-Viewer': 'false',
#              'CloudFront-Is-Tablet-Viewer': 'false',
#              'CloudFront-Viewer-Country': 'US',
#              'Host': '0pi.us-west-2.amazonaws.com',
#              'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.13; '
#                            'rv:57.0) Gecko/20100101 Firefox/57.0',
#              'Via': '2.0 05c830b46.cloudfront.net '
#                     '(CloudFront)',
#              'X-Amz-Cf-Id': 'kYcLP2KNDxNLVqw5ub4UdM',
#              'X-Amzn-Trace-Id': 'Root=1-e63464347ab1fe0c514ae0',
#              'X-Forwarded-For': '174.65.23.114, 216.137.44.11',
#              'X-Forwarded-Port': '443',
#              'X-Forwarded-Proto': 'https',
#              'cache-control': 'no-cache',
#              'pragma': 'no-cache',
#              'upgrade-insecure-requests': '1'},
#  'httpMethod': 'GET',
#  'isBase64Encoded': False,
#  'path': '/edit',
#  'pathParameters': None,
#  'queryStringParameters': {},
#  'requestContext': {'accountId': '428',
#                     'apiId': '0eiv1z65i4',
#                     'httpMethod': 'GET',
#                     'identity': {'accessKey': None,
#                                  'accountId': None,
#                                  'caller': None,
#                                  'cognitoAuthenticationProvider': None,
#                                  'cognitoAuthenticationType': None,
#                                  'cognitoIdentityId': None,
#                                  'cognitoIdentityPoolId': None,
#                                  'sourceIp': '174.65.23.114',
#                                  'user': None,
#                                  'userAgent': 'Mozilla/5.0 (Macintosh; Intel '
#                                               'Mac OS X 10.13; rv:57.0) '
#                                               'Gecko/20100101 Firefox/57.0',
#                                  'userArn': None},
#                     'path': '/dev/edit',
#                     'protocol': 'HTTP/1.1',
#                     'requestId': 'e14210b1-2720-11e8-9df4-0d105233d7ed',
#                     'requestTime': '14/Mar/2018:00:44:40 +0000',
#                     'requestTimeEpoch': 1520988280644,
#                     'resourceId': 'glglnt',
#                     'resourcePath': '/edit',
#                     'stage': 'dev'},
#  'resource': '/edit',
#  'stageVariables': None}

# print(pprint(event))
# edit(event, None)