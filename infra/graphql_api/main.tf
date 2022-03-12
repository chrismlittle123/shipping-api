data "local_file" "schema" {
  filename = "${path.module}/schema.graphql"
}

# IAM roles

resource "aws_iam_role" "shipping_datasource_role" {
  name               = "shipping_datasource_role_dev"
  assume_role_policy = data.aws_iam_policy_document.shipping_data_datasource_policy_assume_role.json
}

resource "aws_iam_role_policy" "shipping_api_datasource_role_policy" {
  name   = "shipping_api_datasource_policy"
  policy = data.aws_iam_policy_document.shipping_data_datasource_policy.json
  role   = aws_iam_role.shipping_datasource_role.id
}
resource "aws_iam_role" "logging_role" {
  name               = "purchasing_api_logging_role"
  assume_role_policy = data.aws_iam_policy_document.shipping_api_logging_policy_assume_role.json
}
resource "aws_iam_role_policy_attachment" "purchasing_api_logging_policy" {
  policy_arn = "arn:aws:iam::aws:policy/service-role/AWSAppSyncPushToCloudWatchLogs"
  role       = aws_iam_role.logging_role.name
}

# AppSync GraphQL API
resource "aws_appsync_graphql_api" "appsync" {
  name                = "shipping-api"
  schema              = data.local_file.schema.content
  authentication_type = "API_KEY"

  log_config {
    cloudwatch_logs_role_arn = aws_iam_role.logging_role.arn
    field_log_level          = "ERROR"
  }
}

resource "aws_appsync_api_key" "appsync_api_key" {
  api_id = aws_appsync_graphql_api.appsync.id
}

## GetVesselData Query

# Resolvers
data "local_file" "get_vessel_data_request_mapping" {
  filename = "${path.module}/resolvers/getVesselData/request-mapping-template.vm"
}

data "local_file" "get_vessel_data_response_mapping" {
  filename = "${path.module}/resolvers/getVesselData/response-mapping-template.vm"
}

# Data source

resource "aws_appsync_datasource" "shipping_data" {
  api_id           = aws_appsync_api_key.appsync_api_key.api_id
  name             = "shipping_data"
  service_role_arn = aws_iam_role.shipping_datasource_role.arn
  type             = "AMAZON_DYNAMODB"

  dynamodb_config {
    table_name = "shipping-data"
  }
}

# Functions
resource "aws_appsync_function" "getVesselData_function" {
  api_id                    = aws_appsync_api_key.appsync_api_key.api_id
  data_source               = aws_appsync_datasource.shipping_data.name
  name                      = "getVesselData_function"
  request_mapping_template  = data.local_file.get_vessel_data_request_mapping.content
  response_mapping_template = data.local_file.get_vessel_data_response_mapping.content
}

data "template_file" "getVesselData_before_mapping" {
  template = file("${path.module}/resolvers/all-resolvers-before-mapping-template.vm.tpl")
  vars = {
    section_name = "getVesselData"
  }
}
