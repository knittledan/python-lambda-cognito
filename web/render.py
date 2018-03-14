from jinja2 import Environment, PackageLoader, select_autoescape


def env() -> Environment:
    return Environment(
        loader=PackageLoader('web', 'asset'),
        autoescape=select_autoescape(['html', 'xml']))


def index():
    html = env().get_template('index.html')
    return html.render()