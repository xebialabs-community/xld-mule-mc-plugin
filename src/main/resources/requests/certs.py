#!/usr/bin/env python
#
# THIS CODE AND INFORMATION ARE PROVIDED "AS IS" WITHOUT WARRANTY OF ANY KIND, EITHER EXPRESSED OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE IMPLIED WARRANTIES OF MERCHANTABILITY AND/OR FITNESS
# FOR A PARTICULAR PURPOSE. THIS CODE AND INFORMATION ARE NOT SUPPORTED BY XEBIALABS.
#

# -*- coding: utf-8 -*-

"""
certs.py
~~~~~~~~

This module returns the preferred default CA certificate bundle.

If you are packaging Requests, e.g., for a Linux distribution or a managed
environment, you can change the definition of where() to return a separately
packaged CA bundle.
"""
import os.path

try:
    from certifi import where
except ImportError:
    def where():
        """Return the preferred certificate bundle."""
        # vendored bundle inside Requests
        return os.path.join(os.path.dirname(__file__), 'cacert.pem')

if __name__ == '__main__':
    print(where())
