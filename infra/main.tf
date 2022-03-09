terraform {

  backend "s3" {}
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 3.27"
    }
  }

  required_version = ">= 1.1.0"
}

provider "aws" {
  profile = "chrismlittle"
  region  = "eu-west-2"
}

module "sample-lambda" {
  aws_account_id = var.aws_account_id
  aws_region     = var.aws_region
  project        = var.project
  source         = "./sample_lambda"
}
