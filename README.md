# props-resource

`props-resource` is a sort of a [Concourse](https://concourse-ci.org/) resource. We say `sort of` because it does not really store the resource data/information outside of the Concourse installation itself as is the standard for Concourse resources. Instead it provides the ability to store properties of a given job as an `output` of the job by implementing the `out` script for resources and storing information as `metadata` which will then be stored with the job history in the Concourse system.

The `in` and `check` scripts have been implemented but don't do anything meaningful.

## Use

## Requirements

The `props-resource` is written in [Python](https://www.python.org/) so working on it takes an editor of some sort and a `python3` installation. For building you also need [Docker](https://www.docker.com/) because that is how custom resources are provided to Concourse.

Tests are run as part of the creation of the `docker` images by running
``` bash
docker build -t [image:tag] .
```
in the base directory of the project. Assuming the test all succeed a new image will be built. In case of test failures the build is aborted.
