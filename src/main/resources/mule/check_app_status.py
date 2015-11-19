#
# THIS CODE AND INFORMATION ARE PROVIDED "AS IS" WITHOUT WARRANTY OF ANY KIND, EITHER EXPRESSED OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE IMPLIED WARRANTIES OF MERCHANTABILITY AND/OR FITNESS
# FOR A PARTICULAR PURPOSE. THIS CODE AND INFORMATION ARE NOT SUPPORTED BY XEBIALABS.
#

from mule.mmc_client import MMCClient
import sys

client = MMCClient.create_client_from_deployed(deployed)

print "Check deployment status for success"
app_name = deployed.applicationName
deployment_name = "%s-%s" % (app_name, deployed.container.name.lower())

deployment_id = client.get_deployment_id_by_name(deployment_name)
success, deployment = client.wait_for_deployment(deployment_id)
if not success:
    print "Deployment [%s] failed. No additional information available.\nSee %s" % (deployment_name, deployment["href"])
    sys.exit(1)
print "Done."
