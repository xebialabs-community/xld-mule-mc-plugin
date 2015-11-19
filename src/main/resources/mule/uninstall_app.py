#
# THIS CODE AND INFORMATION ARE PROVIDED "AS IS" WITHOUT WARRANTY OF ANY KIND, EITHER EXPRESSED OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE IMPLIED WARRANTIES OF MERCHANTABILITY AND/OR FITNESS
# FOR A PARTICULAR PURPOSE. THIS CODE AND INFORMATION ARE NOT SUPPORTED BY XEBIALABS.
#

from mule.mmc_client import MMCClient

deployed = previousDeployed
client = MMCClient.create_client_from_deployed(deployed)

app_name = deployed.applicationName
deployment_name = "%s-%s" % (app_name, deployed.container.name.lower())
print "Uninstalling deployment [%s]." % deployment_name
client.delete_deployment(deployment_name)
print "Done"
