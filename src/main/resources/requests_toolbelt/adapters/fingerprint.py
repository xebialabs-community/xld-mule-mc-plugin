#
# THIS CODE AND INFORMATION ARE PROVIDED "AS IS" WITHOUT WARRANTY OF ANY KIND, EITHER EXPRESSED OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE IMPLIED WARRANTIES OF MERCHANTABILITY AND/OR FITNESS
# FOR A PARTICULAR PURPOSE. THIS CODE AND INFORMATION ARE NOT SUPPORTED BY XEBIALABS.
#

# -*- coding: utf-8 -*-
"""Submodule containing the implementation for the FingerprintAdapter.

This file contains an implementation of a Transport Adapter that validates
the fingerprints of SSL certificates presented upon connection.
"""
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.poolmanager import PoolManager


class FingerprintAdapter(HTTPAdapter):
    """
    A HTTPS Adapter for Python Requests that verifies certificate fingerprints,
    instead of certificate hostnames.

    Example usage:

    .. code-block:: python

        import requests
        import ssl
        from requests_toolbelt.adapters.fingerprint import FingerprintAdapter

        twitter_fingerprint = '...'
        s = requests.Session()
        s.mount(
            'https://twitter.com',
            FingerprintAdapter(twitter_fingerprint)
        )

    The fingerprint should be provided as a hexadecimal string, optionally
    containing colons.
    """

    __attrs__ = HTTPAdapter.__attrs__ + ['fingerprint']

    def __init__(self, fingerprint, **kwargs):
        self.fingerprint = fingerprint

        super(FingerprintAdapter, self).__init__(**kwargs)

    def init_poolmanager(self, connections, maxsize, block=False):
        self.poolmanager = PoolManager(num_pools=connections,
                                       maxsize=maxsize,
                                       block=block,
                                       assert_fingerprint=self.fingerprint)
