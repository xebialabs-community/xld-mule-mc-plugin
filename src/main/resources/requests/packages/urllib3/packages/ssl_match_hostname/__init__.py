#
# THIS CODE AND INFORMATION ARE PROVIDED "AS IS" WITHOUT WARRANTY OF ANY KIND, EITHER EXPRESSED OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE IMPLIED WARRANTIES OF MERCHANTABILITY AND/OR FITNESS
# FOR A PARTICULAR PURPOSE. THIS CODE AND INFORMATION ARE NOT SUPPORTED BY XEBIALABS.
#

try:
    # Python 3.2+
    from ssl import CertificateError, match_hostname
except ImportError:
    try:
        # Backport of the function from a pypi module
        from backports.ssl_match_hostname import CertificateError, match_hostname
    except ImportError:
        # Our vendored copy
        from ._implementation import CertificateError, match_hostname

# Not needed, but documenting what we provide.
__all__ = ('CertificateError', 'match_hostname')
