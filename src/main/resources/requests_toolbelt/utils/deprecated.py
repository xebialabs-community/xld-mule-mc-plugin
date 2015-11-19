#
# THIS CODE AND INFORMATION ARE PROVIDED "AS IS" WITHOUT WARRANTY OF ANY KIND, EITHER EXPRESSED OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE IMPLIED WARRANTIES OF MERCHANTABILITY AND/OR FITNESS
# FOR A PARTICULAR PURPOSE. THIS CODE AND INFORMATION ARE NOT SUPPORTED BY XEBIALABS.
#

# -*- coding: utf-8 -*-
"""A collection of functions deprecated in requests.utils."""
import re

from requests import utils


def get_encodings_from_content(content):
    """Return encodings from given content string.

    .. code-block:: python

        import requests
        from requests_toolbelt.utils import deprecated

        r = requests.get(url)
        encodings = deprecated.get_encodings_from_content(r)

    :param content: bytestring to extract encodings from.
    :type content: bytes
    """
    find_charset = re.compile(
        r'<meta.*?charset=["\']*(.+?)["\'>]', flags=re.I
    ).findall

    find_pragma = re.compile(
        r'<meta.*?content=["\']*;?charset=(.+?)["\'>]', flags=re.I
    ).findall

    find_xml = re.compile(
        r'^<\?xml.*?encoding=["\']*(.+?)["\'>]'
    ).findall

    return find_charset(content) + find_pragma(content) + find_xml(content)


def get_unicode_from_response(response):
    """Return the requested content back in unicode.

    This will first attempt to retrieve the encoding from the response
    headers. If that fails, it will use
    :func:`requests_toolbelt.utils.deprecated.get_encodings_from_content`
    to determine encodings from HTML elements.

    .. code-block:: python

        import requests
        from requests_toolbelt.utils import deprecated

        r = requests.get(url)
        text = deprecated.get_unicode_from_response(r)

    :param response: Response object to get unicode content from.
    :type response: requests.models.Response
    """
    tried_encodings = set()

    # Try charset from content-type
    encoding = utils.get_encoding_from_headers(response.headers)

    if encoding:
        try:
            return str(response.content, encoding)
        except UnicodeError:
            tried_encodings.add(encoding.lower())

    encodings = get_encodings_from_content(response.content)

    for _encoding in encodings:
        _encoding = _encoding.lower()
        if _encoding in tried_encodings:
            continue
        try:
            return str(response.content, _encoding)
        except UnicodeError:
            tried_encodings.add(_encoding)

    # Fall back:
    if encoding:
        try:
            return str(response.content, encoding, errors='replace')
        except TypeError:
            pass
    return response.text