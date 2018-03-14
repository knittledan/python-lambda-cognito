
def callback_url(event: dict) -> str:
    headers  = event.get('headers', {})
    protocol = headers.get('X-Forwarded-Proto', '')
    host     = headers.get('Host', '')

    request_context = event.get('requestContext', {})
    url_path = request_context.get('path', '')
    return f"{protocol}://{host}{url_path}"


def authorization_token(event: dict) -> str:
    headers  = event.get('headers', {})
    return headers.get('Authorization', '')[len('bearer '):]
