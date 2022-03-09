resource "aws_ssm_parameter" "iam_role_arn" {
  name      = "/${var.project}/${local.service_name}/lambda-iam-role/arn"
  type      = "String"
  value     = aws_iam_role.lambda_iam.arn
  overwrite = true
}
