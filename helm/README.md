### Summary

This repo helps you to learn how to build and deploy a NodeJS app onto an OpenShift cluster using an OpenShift templates and its equivalent Helm implementation.

  *Python App Note:
  1. Run you app at 0.0.0.0:8080 port
  2. NPM_MIRROR env variable is set in way to identify its running in openshift and for the swagger UI to work with https scheme.
  3. The base image used is changed to python:latest
  4. Create the appropriate git repo secret.*

### Helm charts vs OCP template

* [Helm](https://helm.sh/) is best way to find, share, and use software built for Kubernetes. It allows describing the application structure through convenient helm-charts and managing it with simple commands.
[OCP-Template](https://docs.openshift.com/container-platform/3.5/dev_guide/templates.html) can describe a set of objects, for example services, build configurations, and deployment configurations. These can be processed to create anything you have permission to create within a project
* Templates are way more static compared to Helm charts. Helm provides values.yaml file which can be used to parameterize the entire helm chart. These values are easy to override for multiple runs using different values file or using console input.
* Helm charts can deal with many life cycle methods which templates lack.
* Helm charts can be built around a solid testing framework for making it viable for large projects.

### Prerequisites Helm
1. User has access to an Openshift Cluster 3.11 or 4. 
2. User has installed [OpenShift Client Tools](https://docs.openshift.com/enterprise/3.0/cli_reference/get_started_cli.html#installing-the-cli) and has access to the cluster via ```bash oc```.
3. First login to your OpenShift cluster via the ```oc login``` command. Make sure you have a working namespace. If not, create a new one.
4. Run below command to create the source secret in OpenShift. Generate you git passcode following [this](https://help.github.com/en/github/authenticating-to-github/creating-a-personal-access-token). This can be generated only from your personal github repo on the fork of this project.
```bash
oc create secret generic git-secret --from-literal=username=<git-username> --from-literal=password=<git-passcode/password> --type=kubernetes.io/basic-auth
```
5. Make sure [Helm client](https://github.com/helm/helm/releases) v3.x.x is installed and added to your path.

### Values file in Helm

In a Helm chart the customization happens in the values.yaml used. For each run you can use a different values file. These files will hold those fields that are made dynamic in the corresponding charts. Following table gives an overview of different values you can set in values file for both build and deploy

| Name | Description | Default |
| ------ | ------ | ------ |
| NAME_OVERRIDE  | Value that overrides release name for your created k8s resource in Openshift.| Helm run Release name  |
| NAMESPACE | Namespace in which ImageStream exists  | openshift |
| NODEJS_VERSION | Version of python used | latest |
| GIT_SECRET | Name of secret created in OpenShift to read from source repository. Check prerequisite step for details  | git-secret |
| SOURCE_REPOSITORY_URL | (REQUIRED) The URL of the repository with your application source code. Repo link of this project's fork in your personal git repo | https://github.com/binoyskumar92/covid-ticketing.git |
| SOURCE_REPOSITORY_REF | (REQUIRED) Set this to a branch name, tag or other ref of your repository if you | dev-backend-code |
| CONTEXT_DIR  | Set this to the relative path to your project if it is not in the root | nil |
| APPLICATION_DOMAIN  | The exposed hostname that will route to the Node.js service, if left  | nil |
| NPM_MIRROR | The custom NPM mirror URL | nil |
| CREATE_NEW_IMAGE_STREAM | Flag to create a new ImageStream. If IS is already created set this to false. | true |
| CREATE_NEW_IMAGE_STREAM | Flag to create a new ImageStream. If IS is already created set this to false. | true |
| DEST_IMAGE_NAME | Name of the image that needs to be pushed to ImageStream | pythonapp |
| MEMORY_LIMIT | Maximum amount of memory the container can use | 512Mi |
| SRC_IMAGE_NAME | Name of the image that needs to be pulled from ImageStream for deployment | pythonapp |

> Note: If you face any error regarding a duplicate ImageStream, set ```CREATE_NEW_IMAGE_STREAM``` to false in [/helm/nodeapp-build/values.yaml](helm/nodeapp-build/values.yaml) file
> Note: ```NODEJS_VERSION``` is actually the python version

#### How to Build  
1. Update the [values.yaml](helm/nodeapp-build/values.yaml) for Build with your required values.
2. Stay in root folder. If logged in to the OpenShift cluster via ```oc```, run the following command to create the BuildConfig and an ImageStream via Helm. This will build the application source specified by source values in [/helm/nodeapp-build/values.yaml](helm/nodeapp-build/values.yaml) and push to the ImageStream.
```bash 
helm upgrade --install <a-release-name> helm/nodeapp-build --values helm/nodeapp-build/values.yaml
```
 > Note: The release-name can be any other name.
 
 3. Run below command to make sure a build pod is running
 ```bash
 oc get pods
 ```

 #### How to Deploy
1. Update the [values.yaml](helm/nodeapp-deploy/values.yaml) for Deploy  with your required values.
2. Stay in root folder. If logged in to the OpenShift cluster via ```oc```, run the following command to create the Deployment, Route and Service via Helm. This will pull the previously built image in previous Build step. Update values in [/helm/nodeapp-deploy/values.yaml](helm/nodeapp-deploy/values.yaml) before running below command.
```bash 
helm upgrade --install <a-release-name> helm/nodeapp-deploy --values helm/nodeapp-deploy/values.yaml
```
> Note: The release-name can be any other name.

 3. Run below command to get the exposed route information and run the url in your browser when it is ready to see the NodeJS application.
 ```bash
 oc get route -l app=<used-release-name-in-previous-step>
 ```
 4. If you run into any issue always login to your cluster and check the pod logs.



