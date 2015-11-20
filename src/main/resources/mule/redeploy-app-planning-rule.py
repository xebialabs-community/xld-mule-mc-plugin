#
# THIS CODE AND INFORMATION ARE PROVIDED "AS IS" WITHOUT WARRANTY OF ANY KIND, EITHER EXPRESSED OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE IMPLIED WARRANTIES OF MERCHANTABILITY AND/OR FITNESS
# FOR A PARTICULAR PURPOSE. THIS CODE AND INFORMATION ARE NOT SUPPORTED BY XEBIALABS.
#

def should_trigger_redeploy(deltas):
    for delta in deltas.deltas:
        delta_op = str(delta.operation)
        deployed = delta.previous if delta_op == "DESTROY" else delta.deployed
        if str(deployed.type) == "mule.DeployedConfigFile" and delta_op != "NOOP":
            return True
    return False

def extract_mule_app_deltas_to_redeploy(deltas):
    redeploy_deltas = []
    for delta in deltas.deltas:
        if str(delta.operation) == "NOOP":
            redeploy_deltas.append(delta)
    return redeploy_deltas

def add_step(script, desc, deployed):
    step = steps.jython(description=desc, order=70, script=script, jython_context={"deployed": deployed})
    context.addStep(step)

if should_trigger_redeploy(deltas):
    for delta in extract_mule_app_deltas_to_redeploy(deltas):
        deployed = delta.deployed
        add_step("mule/redeploy_app.py", "Redeploy application %s on %s" % (deployed.applicationName, deployed.container.name), deployed)
        add_step("mule/check_app_status.py", "Check deployment status for %s" % deployed.applicationName, deployed)

