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

resource "aws_sns_topic" "dead_letter_topic" {
  name = "${local.service_name}_dead_letter_topic"
}

resource "aws_sqs_queue" "dead_letter_queue" {
  name                          = "${local.service_name}_dead_letter_queue"
  output_arn_ssm_parameter_name = "/${var.project}/${local.service_name}/dead-letter-sqs-topic/arn"
  fifo_queue                    = var.fifo_queue
  message_retention_seconds     = var.retention_time
}

resource "aws_sns_topic_subscription" "channel_to_queue" {
  endpoint  = aws_sqs_queue.dead_letter_queue.arn
  protocol  = "sqs"
  topic_arn = aws_sns_topic.dead_letter_topic.arn
}

resource "aws_sqs_queue_policy" "sns_sqs_policy" {
  queue_url = aws_sqs_queue.dead_letter_queue.id

  policy = <<POLICY
{
  "Version": "2012-10-17",
  "Id": "sqspolicy",
  "Statement": [
    {
      "Sid": "First",
      "Effect": "Allow",
      "Principal": "*",
      "Action": "sqs:SendMessage",
      "Resource": "${aws_sqs_queue.dead_letter_queue.arn}",
      "Condition": {
        "ArnEquals": {
          "aws:SourceArn": "${aws_sns_topic.dead_letter_topic.arn}"
        }
      }
    }
  ]
}
POLICY
}
