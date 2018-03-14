import boto3
from uuid import uuid4


class IdentityPool:
    def __init__(self, cognito_pool_id, cognito_client_id, region):
        self.client_id = cognito_client_id
        self.client = boto3.DEFAULT_SESSION.client("cognito-idp", region_name=region)
        self.user_pool = self.client.describe_user_pool(UserPoolId=cognito_pool_id)
        self.user_pool_client = self.client.describe_user_pool_client(UserPoolId=self.user_pool['UserPool']['Id'], ClientId=cognito_client_id)

    @property
    def redirect_urls(self):
        return self.user_pool_client['UserPoolClient']['CallbackURLs']

    @property
    def token_url(self):
        return f"https://{self.user_pool['UserPool']['Domain']}.auth.us-west-2.amazoncognito.com/oauth2/token"

    @property
    def authorize_url(self):
        query_params = '&'.join((
            f"redirect_uri={','.join(self.redirect_urls)}",
            "response_type=code",
            f"client_id={self.client_id}",
            f"state={uuid4()}",
        ))
        return f"https://{self.user_pool['UserPool']['Domain']}.auth.us-west-2.amazoncognito.com/oauth2/authorize?{query_params}"
