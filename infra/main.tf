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


# Shared resources
resource "aws_s3_bucket" "shipping_api_bucket" {
  bucket = "${var.project}-${var.aws_account_id}"
}

resource "aws_dynamodb_table" "shipping-data" {
  name           = "shipping-data"
  read_capacity  = 200
  write_capacity = 200
  hash_key       = "PK"
  range_key      = "SK"

  attribute {
    name = "PK"
    type = "S"
  }

  attribute {
    name = "SK"
    type = "S"
  }

  attribute {
    name = "imo_number"
    type = "S"
  }

  attribute {
    name = "name"
    type = "S"
  }

}


# Lambda functions
module "data_ingestion" {
  aws_account_id = var.aws_account_id
  aws_region     = var.aws_region
  project        = var.project
  stage_name     = var.stage_name
  service_name   = "data-ingestion"
  source         = "./data_ingestion"
}

module "rest_api" {
  aws_account_id = var.aws_account_id
  aws_region     = var.aws_region
  project        = var.project
  stage_name     = var.stage_name
  service_name   = "rest-api"
  source         = "./rest_api"
}
