#
# THIS CODE AND INFORMATION ARE PROVIDED "AS IS" WITHOUT WARRANTY OF ANY KIND, EITHER EXPRESSED OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE IMPLIED WARRANTIES OF MERCHANTABILITY AND/OR FITNESS
# FOR A PARTICULAR PURPOSE. THIS CODE AND INFORMATION ARE NOT SUPPORTED BY XEBIALABS.
#


import time
import json

from http.http_connection import HttpConnection
from http.http_entity_builder import HttpEntityBuilder
from http.http_request import HttpRequest



class MMCClient(object):
    def __init__(self, url, username, password):
        self._url = url
        if url.endswith('/'):
            self._url = url[:-1]
        self._http_connection = HttpConnection(url, username, password)
        self._request = HttpRequest(self._http_connection, username, password)

    @staticmethod
    def create_client_from_deployed(deployed):
        mmc = deployed.container.mmc
        return MMCClient(mmc.url, mmc.username, mmc.password)

    def upload_to_repository(self, app_name, version, file_name, file_path):
        parts = {'name': HttpEntityBuilder.create_string_body(app_name), 'version': HttpEntityBuilder.create_string_body(version), 'file': HttpEntityBuilder.create_file_body(file_path) }
        r = self._request.post_without_headers("/api/repository", HttpEntityBuilder.create_multipart_entity(parts))
        if not r.isSuccessful and r.status != 201:
            raise Exception("Failed to upload [%s]. Server return %s.\n%s" % (file_path, r.status, r.response))
        print "Received response after upload [%s].\n" % r.response
        return json.loads(r.response)

    def delete_deployment_by_id(self, deployment_id):
        r = self._request.delete("/api/deployments/%s" % deployment_id, contentType = 'application/json')
        if not r.isSuccessful():
            raise Exception("Failed to delete [%s]. Server return %s.\n%s" % (deployment_id, r.status, r.response))

    def get_deployment_id_by_name(self, name):
        r = self._request.get("/api/deployments", contentType = 'application/json')
        deployments = json.loads(r.response)['data']
        for d in deployments:
            if d['name'] == name:
                return d['id']
        return None

    def get_deployment_by_id(self, deployment_id):
        r = self._request.get("/api/deployments/%s" % deployment_id, contentType = 'application/json')
        if not r.isSuccessful():
            raise Exception("Failed to get deployment [%s]. Server return %s.\n%s" % (deployment_id, r.status, r.response))
        return json.loads(r.response)

    def delete_deployment(self, name):
        deployment_id = self.get_deployment_id_by_name(name)
        if deployment_id:
            self.delete_deployment_by_id(deployment_id)

    def get_application_version_id(self, name, version):
        r = self._request.get("/api/repository", contentType = 'application/json')
        if not r.isSuccessful():
            raise Exception("Failed to get application version [%s]-[%s]. Server return %s.\n%s\n" % (name, version, r.status, r.response))
        applications = json.loads(r.response)['data']
        for a in applications:
            if a['name'] == name:
                for v in a['versions']:
                    if v['name'] == version:
                        return v['id']
        return None

    def get_server_groups(self):
        r = self._request.get("/api/serverGroups", contentType = 'application/json')
        return json.loads(r.response)['data']

    def get_server_group_id(self, server_group):
        for g in self.get_server_groups():
            if g['name'] == server_group:
                return g['id']
        raise Exception("No sever group found having the name %s " % server_group)

    def get_servers_for_group(self, server_group):
        r = self._request.get("/api/servers", contentType = 'application/json')
        server_ids = set()
        servers = json.loads(r.response)['data']
        for s in servers:
            for g in s['groups']:
                if server_group == g['name']:
                    server_ids.add(s['id'])
        return [str(i) for i in server_ids]

    def get_clusters(self):
        r = self._request.get("/api/clusters", contentType = 'application/json')
        return json.loads(r.response)['data']

    def get_clusters_by_name(self, cluster_name):
        cluster_ids = set()
        for c in self.get_clusters():
            if cluster_name == c['name']:
                cluster_ids.add(c['id'])
        return [str(i) for i in cluster_ids]

    def delete_application_by_id(self, application_version_id):
        r = self._request.get("api/repository/%s" % application_version_id, contentType = 'application/json')
        if not r.isSuccessful():
            raise Exception("Failed to delete application [%s]. Server return %s.\n%s" % (application_version_id, r.status, r.response))

    def delete_application(self, application_name, version):
        application_version_id = self.get_application_version_id(application_name, version)
        if application_version_id:
            self.delete_application_by_id(application_version_id)

    def _create_deployment(self, name, cluster_ids, server_ids, version_id):
        # delete existing deployment before creating new one
        self.delete_deployment(name)
        req = {'name': name, 'clusters': cluster_ids, 'servers': server_ids, 'applications': [version_id]}
        r = self._request.post("/api/deployments", HttpEntityBuilder.create_string_entity(json.dumps(req)), contentType = 'application/json')
        if not r.isSuccessful():
            raise Exception("Failed to create deployment. Server return %s.\n%s" % (r.status, r.response))
        return json.loads(r.response)['id']

    def create_cluster_deployment(self, cluster_name, deployment_name, version_id):
        cluster_ids = self.get_clusters_by_name(cluster_name)
        if len(cluster_ids) == 0:
            raise Exception("No cluster found with name : [%s] " % cluster_name)
        return self._create_deployment(deployment_name, cluster_ids, [], version_id)

    def create_server_group_deployment(self, server_group, deployment_name, version_id):
        servers_ids = self.get_servers_for_group(server_group)
        if len(servers_ids) == 0:
            raise Exception("No server found into group : %s " % server_group)
        return self._create_deployment(deployment_name, [], servers_ids, version_id)

    def deploy_deployment_by_id(self, deployment_id):
        r = self._request.post("/api/deployments/%s/deploy" % deployment_id,HttpEntityBuilder.create_string_entity(''), contentType = 'application/json')
        if not r.isSuccessful():
            raise Exception("Failed to deploy [%s]. Server return %s.\n%s" % (deployment_id, r.status, r.response))

    def redeploy_deployment_by_id(self, deployment_id):
        r = self._request.post("/api/deployments/%s/redeploy" % deployment_id,HttpEntityBuilder.create_string_entity(''),  contentType = 'application/json')
        if not r.isSuccessful():
            raise Exception("Failed to redeploy [%s]. Server return %s.\n%s" % (deployment_id, r.status, r.response))

    def wait_for_deployment(self, deployment_id):
        status = "Unknown"
        deployment = None
        while status != "FAILED" and status != "DEPLOYED":
            deployment = self.get_deployment_by_id(deployment_id)
            status = deployment["status"]
            time.sleep(5)
        return status == "DEPLOYED", deployment


