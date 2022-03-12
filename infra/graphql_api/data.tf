data "aws_iam_policy_document" "shipping_api_access_policy" {

  statement {
    effect = "Allow"
    actions = [
      "appsync:GraphQL"
    ]
    resources = [
    "arn:aws:appsync:${var.aws_region}:${var.aws_account_id}:apis/${aws_appsync_graphql_api.appsync.id}/*"]
  }
}

data "aws_iam_policy_document" "shipping_data_datasource_policy" {

  statement {
    effect = "Allow"
    actions = [
      "dynamodb:GetItem",
      "dynamodb:BatchGetItem",
      "dynamodb:Query"
    ]
    resources = [
      "arn:aws:dynamodb:${var.aws_region}:${var.aws_account_id}:table/shipping-data",
    ]
  }
}
