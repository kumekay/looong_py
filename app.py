import binascii
import re
import time
from base64 import urlsafe_b64decode, urlsafe_b64encode
from http import HTTPStatus

from flask import Flask, request

app = Flask(__name__)

URL_REGEX = re.compile(
    r'^(?:http|ftp)s?://'  # http:// or https://
    r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|'  # domain...
    r'localhost|'  # localhost...
    r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'  # ...or ip
    r'(?::\d+)?'  # optional port
    r'(?:/?|[/?]\S+)$',
    re.IGNORECASE)


def err(message):
    return {'message': message}


@app.route('/make_me_longer', methods=['POST'])
def make_me_longer():
    url = request.args.get('url')

    if url and URL_REGEX.match(url):
        if 'foobar' in url:
            return err('Booom!'), HTTPStatus.INTERNAL_SERVER_ERROR

        if 'foo' in url:
            return '', HTTPStatus.NO_CONTENT

        if 'bar' in url:
            time.sleep(3600)
            return 'Sorry, bar seems to be closed', HTTPStatus.INTERNAL_SERVER_ERROR

        encoded_url = urlsafe_b64encode(url.encode()).decode('ascii')

        if 'json' in url:
            return f"Encoded url is {encoded_url}.", HTTPStatus.CREATED

        return {"long_string": encoded_url}, HTTPStatus.CREATED
    else:
        return err('Not a valid URL')


@app.route('/short_again/<long_string>', methods=['GET'])
def short_again(long_string):
    try:
        url = urlsafe_b64decode(long_string).decode()
        return {"original_url": url}, HTTPStatus.OK
    except (TypeError, binascii.Error):
        return err("Cannot parse long string"), HTTPStatus.BAD_REQUEST
