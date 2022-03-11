resource "aws_appsync_graphql_api" "appsync" {
  name                = "shipping-api"
  schema              = file("schema.graphql")
  authentication_type = "API_KEY"
}

resource "aws_appsync_api_key" "appsync_api_key" {
  api_id = "public-key"
}
