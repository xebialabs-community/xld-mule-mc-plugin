#
# THIS CODE AND INFORMATION ARE PROVIDED "AS IS" WITHOUT WARRANTY OF ANY KIND, EITHER EXPRESSED OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE IMPLIED WARRANTIES OF MERCHANTABILITY AND/OR FITNESS
# FOR A PARTICULAR PURPOSE. THIS CODE AND INFORMATION ARE NOT SUPPORTED BY XEBIALABS.
#

from java.io import File

from org.apache.http.entity import StringEntity
from org.apache.http.entity.mime import MultipartEntityBuilder
from org.apache.http.entity.mime.content import StringBody, FileBody

class HttpEntityBuilder(object):

    @staticmethod
    def create_string_entity(body):
        return StringEntity(body)

    @staticmethod
    def create_multipart_entity(parts):
        entity_builder = MultipartEntityBuilder.create()
        for key, value in parts.iteritems():
            entity_builder.addPart(key,value)
        return entity_builder.build()

    @staticmethod
    def create_string_body(value):
        return StringBody(value)

    @staticmethod
    def create_file_body(file_name):
        return FileBody(File(file_name))