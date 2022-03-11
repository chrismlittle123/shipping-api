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

module "data_ingestion" {
  aws_account_id = var.aws_account_id
  aws_region     = var.aws_region
  project        = var.project
  service_name   = "data-ingestion"
  source         = "./data_ingestion"
}

module "graphql_api" {
  aws_account_id = var.aws_account_id
  aws_region     = var.aws_region
  source         = "./graphql_api"
}
