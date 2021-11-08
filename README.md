# Budget Tracker API

## Deployment Process
The following process is used to deploy code into production:
* Create a branch from main.
* Make your desired modifications to the branch.
* Raise a pull request into main.
* A status check named "build-deploy" will appear.
  * If the status check passes, then your PR will merge automatically. Your code is now deployed in production.
  * If the status check fails, then click "details" to see what the problem is. 
    * The job will re-run automatically if you add a new commit to the PR.
    * You may also re-run manually as needed.

## Continuous Deployment Pipeline

When a pull request is raised, the GitHub workflow called "prod-pipeline" is triggered. (This workflow is defined in .github/workflows/prod-pipeline.yml.)

* Dependencies are installed on the workflow server.
* Unit tests run (see tests/unit/unit_tests.py). 
* A Docker image is built and uploaded to Amazon ECR using an AWS SAM template (as defined in sam_template.yaml).
* The image is deployed to the QA environment, which is a Lambda function exposed by an API Gateway endpoint. 
* Acceptance tests run against the QA instance (see tests/acceptance/acceptance_tests.py)
* The image is deployed to the production environment, which is a Lambda function exposed by an API Gateway endpoint.

If any of the above steps fail, the remaining steps are not executed and a failing status check is reported to the pull request that the workflow is building from.
