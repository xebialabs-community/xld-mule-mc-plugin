#
# THIS CODE AND INFORMATION ARE PROVIDED "AS IS" WITHOUT WARRANTY OF ANY KIND, EITHER EXPRESSED OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE IMPLIED WARRANTIES OF MERCHANTABILITY AND/OR FITNESS
# FOR A PARTICULAR PURPOSE. THIS CODE AND INFORMATION ARE NOT SUPPORTED BY XEBIALABS.
#

class HttpConnection:
    def __init__(self, url, username = None, password = None, proxyHost = None, proxyPort = None):
        self.username = username
        self.password = password
        self.url = url
        self.proxyHost = proxyHost
        self.proxyPort = proxyPort

    def getUrl(self):
        return self.url

    def getProxyHost(self):
        return self.proxyHost

    def getProxyPort(self):
        return self.proxyPort

    def getUsername(self):
        return self.username

    def getPassword(self):
        return self.password