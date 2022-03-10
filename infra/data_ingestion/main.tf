locals {
  service_name = "data-ingestion"
}
resource "aws_iam_role" "lambda_iam" {
  force_detach_policies = true
  name                  = "${var.project}-lambda-role"
  assume_role_policy    = data.aws_iam_policy_document.assume_role_lambda.json
  path                  = "/${var.project}/${local.service_name}/"
}

resource "aws_iam_policy" "inline_policy" {
  name   = "${var.project}-${local.service_name}-policy"
  policy = data.aws_iam_policy_document.lambda_policy.json
}

resource "aws_iam_role_policy_attachment" "lambda_iam_to_policy_attachment" {
  policy_arn = aws_iam_policy.inline_policy.arn
  role       = aws_iam_role.lambda_iam.name
}


resource "aws_s3_bucket" "shipping_api_bucket" {
  bucket = "${var.project}-${var.aws_account_id}"
}

resource "aws_dynamodb_table" "shipping-data" {
  name           = "shipping-data"
  read_capacity  = 20
  write_capacity = 20
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

}
