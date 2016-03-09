# Preface #
 
This document describes the functionality provided by the Mule Management Console Plugin.

[![Build Status](https://travis-ci.org/xebialabs-community/xld-mule-mc-plugin.svg?branch=master)](https://travis-ci.org/xebialabs-community/xld-mule-mc-plugin)


# Overview #

The Mule Management Console plugin is an XL Deploy plugin that uses the Mulesoft [MMC Rest Api](https://docs.mulesoft.com/mule-management-console/v/3.7/rest-api-reference) to perform application deployments to [Mule](https://www.mulesoft.com/platform/mule)

# Features #

* Automatic discovery of MMC server groups and clusters.
* Deploy, update and undeploys Mule application archives.
	* Supports cluster deployments
	* Supports server group deployments
	* Automatic versioning of application
* Deploy configuration file associated with Mule application.
	* Automatic redeploy of application on configuration file change	

# Requirements #

* **XLD Server** 5.1+
* **Mule Management Console** 3.6+
		

# Installation #

Plugin can be downloaded directly from the plugin's repository on [Github](https://github.com/xebialabs-community/xld-mule-mc-plugin/releases).

Place the plugin xldp file into __&lt;xld-home&gt;/plugins__ directory.

## Compilation ##

When you want to develop / test / ... you can use a docker container available at:
[docker-mule](https://github.com/jdewinne/docker-mule)

# Setting up MMC server groups and clusters #

This plugin uses XL Deploy's discovery mechanism to connect to MMC and discover the configured server groups and clusters.  The discovered items (__mule.Cluster__, __mule.ServerGroup__) are stored under the __mule.MMCServer__ configuration item in XL Deploy's repository in the __Infrastruture__ root. The __mule.Cluster__ and __mule.ServerGroup__ containers can then be added to an environment as targets for a __mule.Application__ deployables contained in packages.

## Discovery ##

To start the discovery process, right click the __Infrastructure__ node in the XLD repository tree.  
Then select _Discover_ -> _mule_ -> _MMCServer_

The following properties are required for discovery.

| Property | Description |
| -------- | ----------- |
| url   | Url to the MMC server. Example http://localhost:8080/mmc-3.6.1 |
| username | Username of the administrative user |
| password | Password of the administrative user |


# Deploying a Mule Application #

The Mule application zip (__mule.Application__) configuration item can be defined in a deployment package. __mule.Application__ has the following required properties.

| Property | Description | 
| -------- | ----------- |
| applicationName | The name of the application name in MMC | 
         
## Installation conventions ##

The plugin uses the checksum of the Mule application zip as the version to be stored in the MMC repository. If the version does not exist in the repository, it will be automatically uploaded.  MMC deployment names are generated by appending the target server group or cluster's name to the application name.

## Configuration files ##

Configuration files that are associated with Mule applications can be deployed using the __mule.ConfigFile__ type in a deployment package.  This configuration item inherits all behaviour and properties from __file.File__

When configuration files change, but the Mule application in the deployment package has not, this plugin will automatically generate steps to redeploy the Mule application.

## Sample _deployit-manifest.xml_ ##

```xml
<?xml version="1.0" encoding="UTF-8"?>
<udm.DeploymentPackage version="1.0" application="MyMuleAppApp">
  <deployables>
    <mule.Application name="MyApp.zip" file="MyApp.zip">
      <applicationName>HelloWorld</applicationName>
    </mule.Applicaiton>
  </deployables>
</udm.DeploymentPackage>
```
