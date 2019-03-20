# props-resource

`props-resource` is a sort of a [Concourse](https://concourse-ci.org/) resource. We say `sort of` because it does not 
really store the resource data/information outside of the Concourse installation itself as is the standard for Concourse 
resources. Instead it provides the ability to store properties of a given job as an `output` of the job by implementing 
the `out` script for resources and storing information as `metadata` which will then be stored with the job history in 
the Concourse system.

The `in` and `check` scripts have been implemented but don't do anything meaningful.

## Use
The following description assumes that you have some familiarity with setting up `Concourse` pipelines. If not you can
find documentation at [Concourse docs](https://concourse-ci.org/docs.html).

To use this resource in a pipeline you should first declare the `resource_type` in your pipeline descriptor file:
```yaml
resource_types:
- name: properties
  type: docker-image
  source:
    repository: driepinter/props-resource
    tag: latest
```
If you decide to build the docker image yourself and put it in our own repo the `repository` property may have a different 
value. The name can be anything you want it to be but it makes sense to choose something that indicates what this does.

After this you can declare the `resource` in the same pipeline descriptor file:
```yaml
resources:
- name: random-props
  type: properties
  source:
    path: random-props/random.properties
```
The important thing to note here is the `path` which indicates where the resource will pick up the properties file to
process and put in the `metadata` of the resource `output`.

The next thing to do is to make sure that you have a `job` description that uses the resource. In the sample below we 
have a `git` resource that pulls in a git repository for the job and for the output or `put` we declare our `random-props`
properties resource that we declared earlier:
```yaml
jobs:
- name: properties-fun
  public: false
  plan:
  - get: git-cloudfoundry-spinnaker-ci
    trigger: false
  - task: Shuffle properties to out
    timeout: 10m
    file: git-cloudfoundry-spinnaker-ci/props-pipeline/tasks/properties-fun/properties-fun.yml
  - put: random-props
```
The task describes the details and looks as follows:
```yaml
platform: linux
image_resource:
  type: registry-image
  source: {repository: bash, tag: latest}
inputs:
- name: git-cloudfoundry-spinnaker-ci
outputs:
- name: random-props

run:
  path: git-cloudfoundry-spinnaker-ci/props-pipeline/tasks/properties-fun/properties-fun.sh
```
We declare the task container information and `inputs` and `outputs`. These will make sure that the resources declared
will be mounted in the task container under the names set there. These names need to match the resource names.

As part of the task the script will need to preform the task of putting the properties file in the mounted `outputs` and 
the full name of this needs to match the `path` provided in the `random-props` resource description.

Assuming all those things line up your properties resource will read the provided properties file and put the properties
in the metadata of the output resource. 

## Requirements

The `props-resource` is written in [Python](https://www.python.org/) so working on it takes an editor of some sort and 
a `python3` installation. For building you also need [Docker](https://www.docker.com/) because that is how custom 
resources are provided to Concourse.

Tests are run as part of the creation of the `docker` images by running
``` bash
docker build -t [image:tag] .
```
in the base directory of the project. Assuming the test all succeed a new image will be built. In case of test failures 
the build is aborted.
