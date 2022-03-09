# lambda-template

A template to use for new lambda functions

# Requirements

- Python 3.9
- Pipenv. Run `brew install pipenv` or `pip3 install pipenv` if you have the misfortune of not
  developing on a mac.
- Node + NPM or Yarn. `brew install node` will get you Node and NPM
- Pre-commit, install pre-commit on your mac `pip install pre-commit` or `brew install pre-commit`
- Run `pre-commit install --hook-type pre-push` in the root directory, we will check tests before pushing to remote
- Run `pre-commit install --hook-type pre-commit` in the root directory, we check and format on commit
- AWS bucket set up for terraform.tfstate file
- DynamoDB table called terraform-lock with partition key LockID

Installing deps:

- `yarn install`
- `yarn run install-python-deps`

Run tests:

- `yarn test`

# Invoke Lambda Locally

Ensure you are logged into the AWS CLI and run:

`pipenv run serverless invoke local --function <lambda_name> --path <json_file>`
