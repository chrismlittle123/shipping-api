# shipping-api

An API which lets you access the EU-MRV public CO2 emission report: https://mrv.emsa.europa.eu/#public/emission-report

# Requirements

- Python 3.9
- Pipenv. Run `brew install pipenv` or `pip3 install pipenv`
- Node and NPM. Run `brew install node` with homebrew if you are developing on a Mac, or alternatively download from here: https://nodejs.org/en/download/
- Yarn. Run `npm install --global yarn`
- Pre-commit. Run `pip install pre-commit` or `brew install pre-commit`
- Run `pre-commit install --hook-type pre-push` in the root directory, this hook will run tests before pushing to remote
- Run `pre-commit install --hook-type pre-commit` in the root directory, this hook will check and format code on each commit
- AWS bucket set up for terraform.tfstate file (see backend-config.tfvars file)
- DynamoDB table called terraform-lock with partition key LockID

Installing dependencies:

- `yarn install`
- `yarn run install-python-deps`

Run tests:

- `yarn test`

# Invoke Lambda Locally

Ensure you are logged into the AWS CLI and run:

`pipenv run serverless invoke local --function <lambda_name> --path <json_file>`

# Deploy Serverless

Run the following comman:

`pipenv run serverless deploy`
