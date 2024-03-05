# Reference parameter store of api_key
data "aws_ssm_parameter" "notion_api_key" {
  name = "/notion/api_key"
}

resource "aws_sns_topic" "autofill_urgent_project_lambda_error_topic" {
  name = "autofill_urgent_project_lambda_error_topic"
}

resource "aws_sns_topic_subscription" "autofill_urgent_project_lambda_error_topic_subscription" {
  topic_arn = aws_sns_topic.autofill_urgent_project_lambda_error_topic.arn
  protocol  = "email"
  endpoint  = "alexandre.osada.dev@gmail.com"
}

# Create the Lambda function
resource "aws_lambda_function" "autofill_urgent_project_lambda" {
  function_name = "autofill_urgent_project_lambda"
  role          = aws_iam_role.autofill_urgent_project_lambda_role.arn
  handler       = "omnilife_framework_automations.autofill_urgent_project_lambda.lambda_function.lambda_handler"
  runtime       = "python3.11"
  timeout       = 10
  memory_size   = 128
  publish       = true
  filename      = "../dist/autofill_urgent_project.zip"
  source_code_hash = filebase64sha256("../dist/autofill_urgent_project.zip")
  environment {
    variables = {
      NOTION_DATABASE_ID = "6be0dff3c0ea4c9a9fdec4f665a22a7a"
      NOTION_API_KEY  = data.aws_ssm_parameter.notion_api_key.value
    }
  }
}

resource "aws_lambda_function_event_invoke_config" "autofill_urgent_project_lambda_event_invoke_config" {
  function_name = aws_lambda_function.autofill_urgent_project_lambda.function_name

  destination_config {
    on_failure {
      destination = aws_sns_topic.autofill_urgent_project_lambda_error_topic.arn
    }
  }
}

# Create the IAM role
resource "aws_iam_role" "autofill_urgent_project_lambda_role" {
  name = "autofill_urgent_project_lambda_role"
  assume_role_policy = jsonencode({
    Version = "2012-10-17",
    Statement = [
      {
        Action = "sts:AssumeRole",
        Effect = "Allow",
        Principal = {
          Service = "lambda.amazonaws.com"
        }
      }
    ]
  })
}

# Attach the lambda policy to publish to SNS topic
resource "aws_iam_role_policy" "lambda_sns_publish" {
  name   = "lambda_sns_publish"
  role   = aws_iam_role.autofill_urgent_project_lambda_role.id
  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Action   = "sns:Publish"
        Effect   = "Allow"
        Resource = aws_sns_topic.autofill_urgent_project_lambda_error_topic.arn
      },
    ]
  })
}

# Attach the AWSLambdaBasicExecutionRole policy to the IAM role to log to cloudwatch
resource "aws_iam_role_policy_attachment" "lambda_logs" {
  role       = aws_iam_role.autofill_urgent_project_lambda_role.name
  policy_arn = "arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole"
}

# Create the CloudWatch Event Rule
resource "aws_cloudwatch_event_rule" "autofill_urgent_project_schedule" {
  name        = "autofill_urgent_project_schedule"
  description = "Schedule for running the autofill_urgent_project_lambda"
  schedule_expression = "cron(0 4 * * ? *)"
}

# Create the CloudWatch Event Target
resource "aws_cloudwatch_event_target" "autofill_urgent_project_target" {
  rule      = aws_cloudwatch_event_rule.autofill_urgent_project_schedule.name
  target_id = aws_lambda_function.autofill_urgent_project_lambda.function_name
  arn       = aws_lambda_function.autofill_urgent_project_lambda.arn
}

# Permission to allow CloudWatch to invoke the Lambda function
resource "aws_lambda_permission" "allow_cloudwatch" {
  statement_id  = "AllowExecutionFromCloudWatch"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.autofill_urgent_project_lambda.function_name
  principal     = "events.amazonaws.com"
  source_arn    = aws_cloudwatch_event_rule.autofill_urgent_project_schedule.arn
}