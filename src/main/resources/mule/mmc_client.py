#
# THIS CODE AND INFORMATION ARE PROVIDED "AS IS" WITHOUT WARRANTY OF ANY KIND, EITHER EXPRESSED OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE IMPLIED WARRANTIES OF MERCHANTABILITY AND/OR FITNESS
# FOR A PARTICULAR PURPOSE. THIS CODE AND INFORMATION ARE NOT SUPPORTED BY XEBIALABS.
#


import requests
import time
from requests_toolbelt import MultipartEncoder


class MMCClient(object):
    def __init__(self, url, username, password):
        self._auth = (username, password)
        self._url = url
        if url.endswith('/'):
            self._url = url[:-1]

    @staticmethod
    def create_client_from_deployed(deployed):
        mmc = deployed.container.mmc
        return MMCClient(mmc.url, mmc.username, mmc.password)

    def upload_to_repository(self, app_name, version, file_name, file_path):
        encoder = MultipartEncoder({'name': app_name, 'version': version, 'file': (file_name, open(file_path, 'rb'), 'application/octet-stream')})
        r = requests.post("%s/api/repository" % self._url, data=encoder, headers={'Content-Type': encoder.content_type}, auth=self._auth)
        sc = r.status_code
        if sc != requests.codes.ok and sc != requests.codes.created:
            raise Exception("Failed to upload [%s]. Server return %s.\n%s" % (file_path, sc, r.text))
        return r.json()

    def delete_deployment_by_id(self, deployment_id):
        r = requests.delete("%s/api/deployments/%s" % (self._url, deployment_id), auth=self._auth)
        if r.status_code != requests.codes.ok:
            raise Exception("Failed to delete [%s]. Server return %s.\n%s" % (deployment_id, r.status_code, r.text))

    def get_deployment_id_by_name(self, name):
        r = requests.get("%s/api/deployments" % self._url, auth=self._auth)
        deployments = r.json()['data']
        for d in deployments:
            if d['name'] == name:
                return d['id']
        return None

    def get_deployment_by_id(self, deployment_id):
        r = requests.get("%s/api/deployments/%s" % (self._url, deployment_id), auth=self._auth)
        if r.status_code != requests.codes.ok:
            raise Exception("Failed to get deployment [%s]. Server return %s.\n%s" % (deployment_id, r.status_code, r.text))
        return r.json()

    def delete_deployment(self, name):
        deployment_id = self.get_deployment_id_by_name(name)
        if deployment_id:
            self.delete_deployment_by_id(deployment_id)

    def get_application_version_id(self, name, version):
        r = requests.get("%s/api/repository" % self._url, auth=self._auth)
        applications = r.json()['data']
        for a in applications:
            if a['name'] == name:
                for v in a['versions']:
                    if v['name'] == version:
                        return v['id']
        return None

    def get_server_groups(self):
        r = requests.get("%s/api/serverGroups" % self._url, auth=self._auth)
        return r.json()['data']

    def get_server_group_id(self, server_group):
        for g in self.get_server_groups():
            if g['name'] == server_group:
                return g['id']
        raise Exception("No sever group found having the name %s " % server_group)

    def get_servers_for_group(self, server_group):
        r = requests.get("%s/api/servers" % self._url, auth=self._auth)
        server_ids = set()
        servers = r.json()['data']
        for s in servers:
            for g in s['groups']:
                if server_group == g['name']:
                    server_ids.add(s['id'])
        return [str(i) for i in server_ids]

    def get_clusters(self):
        r = requests.get("%s/api/clusters" % self._url, auth=self._auth)
        return r.json()['data']

    def get_clusters_by_name(self, cluster_name):
        cluster_ids = set()
        for c in self.get_clusters():
            if cluster_name == c['name']:
                cluster_ids.add(c['id'])
        return [str(i) for i in cluster_ids]

    def delete_application_by_id(self, application_version_id):
        r = requests.get("%s/api/repository/%s" % (self._url, application_version_id), auth=self._auth)
        if r.status_code != requests.codes.ok:
            raise Exception("Failed to delete application [%s]. Server return %s.\n%s" % (application_version_id, r.status_code, r.text))

    def delete_application(self, application_name, version):
        application_version_id = self.get_application_version_id(application_name, version)
        if application_version_id:
            self.delete_application_by_id(application_version_id)

    def _create_deployment(self, name, cluster_ids, server_ids, version_id):
        # delete existing deployment before creating new one
        self.delete_deployment(name)
        req = {'name': name, 'clusters': cluster_ids, 'servers': server_ids, 'applications': [version_id]}
        r = requests.post("%s/api/deployments" % self._url, json=req, headers={'Content-Type': 'application/json'}, auth=self._auth)
        if r.status_code != requests.codes.ok:
            raise Exception("Failed to create deployment. Server return %s.\n%s" % (r.status_code, r.text))
        return r.json()['id']

    def create_cluster_deployment(self, cluster_name, deployment_name, version_id):
        cluster_ids = self.get_clusters_by_name(cluster_name)
        if len(cluster_ids) == 0:
            raise Exception("No cluster found with name : %s " + cluster_name)
        return self._create_deployment(deployment_name, cluster_ids, [], version_id)

    def create_server_group_deployment(self, server_group, deployment_name, version_id):
        servers_ids = self.get_servers_for_group(server_group)
        if len(servers_ids) == 0:
            raise Exception("No server found into group : %s " % server_group)
        return self._create_deployment(deployment_name, [], servers_ids, version_id)

    def deploy_deployment_by_id(self, deployment_id):
        r = requests.post("%s/api/deployments/%s/deploy" % (self._url, deployment_id), auth=self._auth)
        if r.status_code != requests.codes.ok:
            raise Exception("Failed to deploy [%s]. Server return %s.\n%s" % (deployment_id, r.status_code, r.text))
        status = "Unknown"
        deployment = None
        while status != "FAILED" and status != "DEPLOYED":
            deployment = self.get_deployment_by_id(deployment_id)
            status = deployment["status"]
            time.sleep(5)
        return status == "DEPLOYED", deployment


