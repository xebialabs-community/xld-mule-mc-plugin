#
# THIS CODE AND INFORMATION ARE PROVIDED "AS IS" WITHOUT WARRANTY OF ANY KIND, EITHER EXPRESSED OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE IMPLIED WARRANTIES OF MERCHANTABILITY AND/OR FITNESS
# FOR A PARTICULAR PURPOSE. THIS CODE AND INFORMATION ARE NOT SUPPORTED BY XEBIALABS.
#

from mule.mmc_client import MMCClient

client = MMCClient.create_client_from_deployed(deployed)

version = deployed.deployable.checksum
app_name = deployed.applicationName
print "Checking if version [%s] for application [%s] exists in MMC repository." % (app_name, version)
application_version_id = client.get_application_version_id(app_name, version)

if application_version_id is None:
    print "Version does not exist in repository. Uploading file [%s]." % deployed.file.name
    result = client.upload_to_repository(app_name, version, deployed.file.name, deployed.file.path)
    application_version_id = result["versionId"]
    print "Successfully uploaded."
else:
    print "Version already uploaded to repository."

deployment_name = "%s-%s" % (app_name, deployed.container.name.lower())
print "Preparing deployment [%s] to [%s] for application version id [%s]." % (deployment_name, deployed.container.name, application_version_id)
if str(deployed.container.type) == "mule.ServerGroup":
    deployment_id = client.create_server_group_deployment(deployed.container.name, deployment_name, application_version_id)
else:
    deployment_id = client.create_cluster_deployment(deployed.container.name, deployment_name, application_version_id)

print "Deployment prepared. Will execute deployment."
client.deploy_deployment_by_id(deployment_id)
print "Done."
