import os


class EnvironmentConfig:
    """
    Default config is for aws sandbox account
    """
    service_name = 'client'

    # AWS
    aws_key = ''
    aws_secret = ''
    region = 'us-west-2'
    cognito_region = 'us-west-2'
    cognito_pool_id = ""
    cognito_client_id = ""
    cognito_secret    = ""
    # Delivery Service Queues
    bucket_name = ''

    def __init__(self):

        # Vroll status worker Variables
        self.service_name = os.environ.get('SERVICE_NAME', self.service_name)

        # AWS
        self.aws_key = os.environ.get('ENV_AWS_KEY', self.aws_key)
        self.aws_secret = os.environ.get('ENV_AWS_SECRET_KEY', self.aws_secret)
        self.region = os.environ.get('ENV_AWS_REGION', self.region)

