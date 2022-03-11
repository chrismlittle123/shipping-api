resource "aws_ssm_parameter" "iam_role_arn" {
  name      = "/${var.project}/${local.service_name}/lambda-iam-role/arn"
  type      = "String"
  value     = aws_iam_role.lambda_iam.arn
  overwrite = true
}

output "sns_topic_arn" {
  value = aws_sns_topic.dead_letter_topic.arn
}

output "sqs_topic_arn" {
  value = aws_sqs_queue.dead_letter_queue.arn
}
