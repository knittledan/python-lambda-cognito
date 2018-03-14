

def asset(event, context):
    path = event['pathParameters']
    asset_file = path.get('asset_file')
    with open(f"web/asset/{asset_file}", 'r') as _file:
        body = _file.read()

    content_type = {
        "css": "text/css",
        "js": "application/javascript",
        "svg": "image/svg+xml",
        "html": "'text/html; charset=utf-8'}"
    }
    content_type = content_type[asset_file.split(".")[-1]]
    return dict(
        statusCode=200,
        body=body,
        headers={'Content-Type': content_type}
    )