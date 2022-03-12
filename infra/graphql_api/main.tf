data "local_file" "schema" {
  filename = "${path.module}/schema.graphql"
}
resource "aws_appsync_graphql_api" "appsync" {
  name                = "shipping-api"
  schema              = data.local_file.schema.content
  authentication_type = "API_KEY"
}

resource "aws_appsync_api_key" "appsync_api_key" {
  api_id = aws_appsync_graphql_api.appsync.id
}

data "local_file" "get_vessel_data_request_mapping" {
  filename = "${path.module}/resolvers/getVesselData/request-mapping-template.vm"
}

data "local_file" "get_vessel_data_response_mapping" {
  filename = "${path.module}/resolvers/getVesselData/response-mapping-template.vm"
}

resource "aws_iam_role" "shipping_datasource_role" {
  name               = "shipping_datasource_role_dev"
  assume_role_policy = data.aws_iam_policy_document.shipping_data_datasource_policy.json
}

resource "aws_appsync_datasource" "shipping_data" {
  api_id           = aws_appsync_api_key.appsync_api_key.api_id
  name             = "shipping-data"
  service_role_arn = aws_iam_role.shipping_datasource_role.arn
  type             = "AMAZON_DYNAMODB"

  dynamodb_config {
    table_name = "shipping-data"
  }
}
resource "aws_appsync_function" "getVesselData_function" {
  api_id                    = aws_appsync_api_key.appsync_api_key.api_id
  data_source               = aws_appsync_datasource.shipping_data.name
  name                      = "getVesselData_function"
  request_mapping_template  = data.local_file.get_vessel_data_request_mapping.content
  response_mapping_template = data.local_file.get_vessel_data_response_mapping.content
}
