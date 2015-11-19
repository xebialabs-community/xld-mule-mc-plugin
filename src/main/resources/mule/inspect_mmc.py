#
# THIS CODE AND INFORMATION ARE PROVIDED "AS IS" WITHOUT WARRANTY OF ANY KIND, EITHER EXPRESSED OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE IMPLIED WARRANTIES OF MERCHANTABILITY AND/OR FITNESS
# FOR A PARTICULAR PURPOSE. THIS CODE AND INFORMATION ARE NOT SUPPORTED BY XEBIALABS.
#

from mule.mmc_client import MMCClient
from com.xebialabs.deployit.plugin.api.reflect import Type

print "Starting discovery of clusters and server groups on %s " % thisCi.url

cluster_descriptor = Type.valueOf("mule.Cluster").getDescriptor()
server_group_descriptor = Type.valueOf("mule.ServerGroup").getDescriptor()

client = MMCClient(thisCi.url, thisCi.username, thisCi.password)

def discovered(ci):
    inspectionContext.discovered(ci)
    inspectionContext.inspected(ci)

print "Starting discovery of clusters"
for cluster in client.get_clusters():
    print "Found cluster %s" % cluster["name"]
    discovered(cluster_descriptor.newInstance("%s/%s" % (thisCi.id, cluster['name'])))

print "Starting discovery of server groups"
for sg in client.get_server_groups():
    print "Found server group %s" % sg["name"]
    discovered(server_group_descriptor.newInstance("%s/%s" % (thisCi.id, sg['name'])))
