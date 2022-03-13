# IAM Roles

resource "aws_iam_role" "lambda_iam" {
  force_detach_policies = true
  name                  = "${var.service_name}-lambda-role"
  assume_role_policy    = data.aws_iam_policy_document.assume_role_lambda.json
  path                  = "/${var.project}/${var.service_name}/"
}

resource "aws_iam_policy" "inline_policy" {
  name   = "${var.project}-${var.service_name}-policy"
  policy = data.aws_iam_policy_document.lambda_policy.json
}

resource "aws_iam_role_policy_attachment" "lambda_iam_to_policy_attachment" {
  policy_arn = aws_iam_policy.inline_policy.arn
  role       = aws_iam_role.lambda_iam.name
}


# Dead Letter Queues
resource "aws_sns_topic" "dead_letter_topic" {
  name = "${var.service_name}_dead_letter_topic"
}

resource "aws_sqs_queue" "dead_letter_queue" {
  name                      = "${var.service_name}_dead_letter_queue"
  fifo_queue                = var.fifo_queue
  message_retention_seconds = var.retention_time
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
