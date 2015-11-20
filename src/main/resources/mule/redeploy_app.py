#
# THIS CODE AND INFORMATION ARE PROVIDED "AS IS" WITHOUT WARRANTY OF ANY KIND, EITHER EXPRESSED OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE IMPLIED WARRANTIES OF MERCHANTABILITY AND/OR FITNESS
# FOR A PARTICULAR PURPOSE. THIS CODE AND INFORMATION ARE NOT SUPPORTED BY XEBIALABS.
#

from mule.mmc_client import MMCClient

client = MMCClient.create_client_from_deployed(deployed)

app_name = deployed.applicationName
deployment_name = "%s-%s" % (app_name, deployed.container.name.lower())
print "Redploying deployment [%s]." % deployment_name
deployment_id = client.get_deployment_id_by_name(deployment_name)
client.redeploy_deployment_by_id(deployment_id)
print "Done"
