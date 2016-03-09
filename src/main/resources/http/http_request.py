#
# THIS CODE AND INFORMATION ARE PROVIDED "AS IS" WITHOUT WARRANTY OF ANY KIND, EITHER EXPRESSED OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE IMPLIED WARRANTIES OF MERCHANTABILITY AND/OR FITNESS
# FOR A PARTICULAR PURPOSE. THIS CODE AND INFORMATION ARE NOT SUPPORTED BY XEBIALABS.
#

import re
import urllib

from java.lang import String

from org.apache.commons.codec.binary import Base64
from org.apache.http import HttpHost
from org.apache.http.client.config import RequestConfig
from org.apache.http.client.methods import HttpGet, HttpPost, HttpPut, HttpDelete
from org.apache.http.util import EntityUtils
from org.apache.http.impl.client import HttpClients

from http.http_response import HttpResponse


class HttpRequest:
    def __init__(self, params, username = None, password = None):
        """
        Builds an HttpRequest

        :param params: an HttpConnection
        :param username: the username
            (optional, it will override the credentials defined on the HttpConnection object)
        :param password: an password
            (optional, it will override the credentials defined on the HttpConnection object)
        """
        self.params = params
        self.username = username
        self.password = password

    def do_request(self, **options):
        """
        Performs an HTTP Request

        :param options: A keyword arguments object with the following properties :
            method: the HTTP method : 'GET', 'PUT', 'POST', 'DELETE'
                (optional: GET will be used if empty)
            context: the context url
                (optional: the url on HttpConnection will be used if empty)
            body: the body of the HTTP request for PUT & POST calls
                (optional: an empty body will be used if empty)
            contentType: the content type to use
                (optional, no content type will be used if empty)
            headers: a dictionary of headers key/values
                (optional, no headers will be used if empty)
        :return: an HttpResponse instance
        """
        request = self.build_request(
            options.get('method', 'GET'),
            options.get('context', ''),
            options.get('entity', ''),
            options.get('contentType', None),
            options.get('headers', None))
        return self.execute_request(request)

    def do_request_without_headers(self, **options):
        """
        Performs an HTTP Request

        :param options: A keyword arguments object with the following properties :
            method: the HTTP method : 'GET', 'PUT', 'POST', 'DELETE'
                (optional: GET will be used if empty)
            context: the context url
                (optional: the url on HttpConnection will be used if empty)
            body: the body of the HTTP request for PUT & POST calls
                (optional: an empty body will be used if empty)
            contentType: the content type to use
                (optional, no content type will be used if empty)
            headers: a dictionary of headers key/values
                (optional, no headers will be used if empty)
        :return: an HttpResponse instance
        """
        request = self.build_request_without_headers(
            options.get('method', 'GET'),
            options.get('context', ''),
            options.get('entity', ''))
        return self.execute_request(request)


    def get(self, context, **options):
        """
        Performs an Http GET Request

        :param context: the context url
        :param options: the options keyword argument described in do_request()
        :return: an HttpResponse instance
        """
        options['method'] = 'GET'
        options['context'] = context
        return self.do_request(**options)


    def put(self, context, entity, **options):
        """
        Performs an Http PUT Request

        :param context: the context url
        :param body: the body of the HTTP request
        :param options: the options keyword argument described in do_request()
        :return: an HttpResponse instance
        """
        options['method'] = 'PUT'
        options['context'] = context
        options['entity'] = entity
        return self.do_request(**options)


    def post(self, context, entity, **options):
        """
        Performs an Http POST Request

        :param context: the context url
        :param body: the body of the HTTP request
        :param options: the options keyword argument described in do_request()
        :return: an HttpResponse instance
        """
        options['method'] = 'POST'
        options['context'] = context
        options['entity'] = entity
        return self.do_request(**options)

    def post_without_headers(self, context, entity, **options):
        """
        Performs an Http POST Request

        :param context: the context url
        :param body: the body of the HTTP request
        :param options: the options keyword argument described in do_request()
        :return: an HttpResponse instance
        """
        options['method'] = 'POST'
        options['context'] = context
        options['entity'] = entity
        return self.do_request_without_headers(**options)


    def delete(self, context, **options):
        """
        Performs an Http DELETE Request

        :param context: the context url
        :param options: the options keyword argument described in do_request()
        :return: an HttpResponse instance
        """
        options['method'] = 'DELETE'
        options['context'] = context
        return self.do_request(**options)


    def build_request(self, method, context, entity, contentType, headers):
        url = self.quote(self.create_path(self.params.getUrl(), context))

        method = method.upper()

        if method == 'GET':
            request = HttpGet(url)
        elif method == 'POST':
            request = HttpPost(url)
            request.setEntity(entity)
        elif method == 'PUT':
            request = HttpPut(url)
            request.setEntity(entity)
        elif method == 'DELETE':
            request = HttpDelete(url)
        else:
            raise Exception('Unsupported method: ' + method)

        request.addHeader('Content-Type', contentType)
        request.addHeader('Accept', contentType)
        self.set_credentials(request)
        self.set_proxy(request)
        self.setHeaders(request, headers)

        return request

    def build_request_without_headers(self, method, context, entity):
        url = self.quote(self.create_path(self.params.getUrl(), context))

        method = method.upper()

        if method == 'GET':
            request = HttpGet(url)
        elif method == 'POST':
            request = HttpPost(url)
            request.setEntity(entity)
        elif method == 'PUT':
            request = HttpPut(url)
            request.setEntity(entity)
        elif method == 'DELETE':
            request = HttpDelete(url)
        else:
            raise Exception('Unsupported method: ' + method)

        self.set_credentials(request)
        self.set_proxy(request)

        return request


    def create_path(self, url, context):
        url = re.sub('/*$', '', url)
        if context is None:
            return url
        elif context.startswith('/'):
            return url + context
        else:
            return url + '/' + context

    def quote(self, url):
        return urllib.quote(url, ':/?&=%')


    def set_credentials(self, request):
        if self.username:
            username = self.username
            password = self.password
        elif self.params.getUsername():
            username = self.params.getUsername()
            password = self.params.getPassword()
        else:
            return

        encoding = Base64.encodeBase64String(String(username + ':' + password).getBytes())
        request.addHeader('Authorization', 'Basic ' + encoding)


    def set_proxy(self, request):
        if not self.params.getProxyHost():
            return

        proxy = HttpHost(self.params.getProxyHost(), int(self.params.getProxyPort()))
        config = RequestConfig.custom().setProxy(proxy).build()
        request.setConfig(config)


    def setHeaders(self, request, headers):
        if headers:
            for key in headers:
                request.setHeader(key, headers[key])


    def execute_request(self, request):
        client = None
        response = None
        try:
            client = HttpClients.createDefault()
            response = client.execute(request)
            status = response.getStatusLine().getStatusCode()
            entity = response.getEntity()
            result = EntityUtils.toString(entity, "UTF-8") if entity else None
            headers = response.getAllHeaders()
            EntityUtils.consume(entity)

            return HttpResponse(status, result, headers)
        finally:
            if response:
                response.close()
            if client:
                client.close()