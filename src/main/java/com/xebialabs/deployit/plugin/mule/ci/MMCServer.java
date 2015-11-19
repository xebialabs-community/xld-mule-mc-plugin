/**
 * THIS CODE AND INFORMATION ARE PROVIDED "AS IS" WITHOUT WARRANTY OF ANY KIND, EITHER EXPRESSED OR
 * IMPLIED, INCLUDING BUT NOT LIMITED TO THE IMPLIED WARRANTIES OF MERCHANTABILITY AND/OR FITNESS
 * FOR A PARTICULAR PURPOSE. THIS CODE AND INFORMATION ARE NOT SUPPORTED BY XEBIALABS.
 */
package com.xebialabs.deployit.plugin.mule.ci;

import java.util.HashMap;
import java.util.Map;

import com.xebialabs.deployit.plugin.api.inspection.Inspect;
import com.xebialabs.deployit.plugin.api.inspection.InspectionContext;
import com.xebialabs.deployit.plugin.api.inspection.InspectionProperty;
import com.xebialabs.deployit.plugin.api.udm.Metadata;
import com.xebialabs.deployit.plugin.api.udm.Property;
import com.xebialabs.deployit.plugin.api.udm.base.BaseContainer;
import com.xebialabs.deployit.plugin.mule.step.JythonInspectionStep;

@Metadata(root = Metadata.ConfigurationItemRoot.INFRASTRUCTURE, description = "Mule Management Console", inspectable = true)
public class MMCServer extends BaseContainer {

    @Property(description = "Url to the MMC server. Example http://localhost:8080/mmc-3.6.1" )
    @InspectionProperty
    private String url;

    @Property
    @InspectionProperty
    private String username;

    @Property(password = true)
    @InspectionProperty
    private String password;

    @Property(hidden = true, defaultValue = "mule/inspect_mmc.py")
    private String inspectionScript;

    @Inspect
    public void inspectContainer(InspectionContext ctx) {
        Map<String, Object> scriptContext = new HashMap<>();
        scriptContext.put("thisCi", this);
        JythonInspectionStep step = new JythonInspectionStep(inspectionScript, scriptContext, "Inspect " + this);
        ctx.addStep(step);
    }

    public String getUrl() {
        return url;
    }

    public void setUrl(final String url) {
        this.url = url;
    }

    public String getUsername() {
        return username;
    }

    public void setUsername(final String username) {
        this.username = username;
    }

    public String getPassword() {
        return password;
    }

    public void setPassword(final String password) {
        this.password = password;
    }

    public String getInspectionScript() {
        return inspectionScript;
    }

    public void setInspectionScript(final String inspectionScript) {
        this.inspectionScript = inspectionScript;
    }
}
