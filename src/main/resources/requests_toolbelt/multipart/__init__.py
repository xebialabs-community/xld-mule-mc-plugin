#
# THIS CODE AND INFORMATION ARE PROVIDED "AS IS" WITHOUT WARRANTY OF ANY KIND, EITHER EXPRESSED OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE IMPLIED WARRANTIES OF MERCHANTABILITY AND/OR FITNESS
# FOR A PARTICULAR PURPOSE. THIS CODE AND INFORMATION ARE NOT SUPPORTED BY XEBIALABS.
#

"""
requests_toolbelt.multipart
===========================

See http://toolbelt.rtfd.org/ for documentation

:copyright: (c) 2014 by Ian Cordasco and Cory Benfield
:license: Apache v2.0, see LICENSE for more details
"""

from .encoder import MultipartEncoder, MultipartEncoderMonitor
from .decoder import MultipartDecoder
from .decoder import ImproperBodyPartContentException
from .decoder import NonMultipartContentTypeException

__title__ = 'requests-toolbelt'
__authors__ = 'Ian Cordasco, Cory Benfield'
__license__ = 'Apache v2.0'
__copyright__ = 'Copyright 2014 Ian Cordasco, Cory Benfield'

__all__ = [
    'MultipartEncoder',
    'MultipartEncoderMonitor',
    'MultipartDecoder',
    'ImproperBodyPartContentException',
    'NonMultipartContentTypeException',
    '__title__',
    '__authors__',
    '__license__',
    '__copyright__',
]
