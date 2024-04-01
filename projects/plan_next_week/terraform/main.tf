# Reference parameter store of api_key
data "aws_ssm_parameter" "googlecalendar_agenda_id" {
  name = "/google/calendar/agenda_id"
}

data "aws_ssm_parameter" "googlecalendar_project_id" {
  name = "/google/calendar/project_id"
}

data "aws_ssm_parameter" "googlecalendar_private_key_id" {
  name = "/google/calendar/private_key_id"
}

data "aws_ssm_parameter" "googlecalendar_private_key" {
  name = "/google/calendar/private_key"
}

data "aws_ssm_parameter" "googlecalendar_client_email" {
  name = "/google/calendar/client_email"
}

data "aws_ssm_parameter" "googlecalendar_client_id" {
  name = "/google/calendar/client_id"
}

data "aws_ssm_parameter" "googlecalendar_client_x509_cert_url" {
  name = "/google/calendar/client_x509_cert_url"
}

data "aws_ssm_parameter" "notion_api_key" {
  name = "/notion/api_key"
}

resource "aws_sns_topic" "plan_next_week_lambda_error_topic" {
  name = "plan_next_week_lambda_error_topic"
}

resource "aws_sns_topic_subscription" "plan_next_week_lambda_error_topic_subscription" {
  topic_arn = aws_sns_topic.plan_next_week_lambda_error_topic.arn
  protocol  = "email"
  endpoint  = "alexandre.osada.dev@gmail.com"
}

# Create the Lambda function
resource "aws_lambda_function" "plan_next_week_lambda" {
  function_name = var.function_name
  role          = aws_iam_role.plan_next_week_lambda_role.arn
  handler       = "omnilife_framework_automations.plan_next_week_lambda.lambda_function.lambda_handler"
  runtime       = "python3.11"
  timeout       = 90
  memory_size   = 128
  publish       = true
  filename      = "../dist/plan_next_week.zip"
  source_code_hash = filebase64sha256("../dist/plan_next_week.zip")
  environment {
    variables = {
      NOTION_DATABASE_ID = var.notion_task_database_id
      NOTION_API_KEY  = data.aws_ssm_parameter.notion_api_key.value
      GOOGLE_CALENDAR_AGENDA_ID = data.aws_ssm_parameter.googlecalendar_agenda_id.value
      GOOGLE_PROJECT_ID = data.aws_ssm_parameter.googlecalendar_project_id.value 
      GOOGLE_PRIVATE_KEY_ID = data.aws_ssm_parameter.googlecalendar_private_key_id.value
      GOOGLE_PRIVATE_KEY = data.aws_ssm_parameter.googlecalendar_private_key.value
      GOOGLE_CLIENT_EMAIL = data.aws_ssm_parameter.googlecalendar_client_email.value
      GOOGLE_CLIENT_ID = data.aws_ssm_parameter.googlecalendar_client_id.value
      GOOGLE_CLIENT_X509_CERT_URL = data.aws_ssm_parameter.googlecalendar_client_x509_cert_url.value
    }
  }
}

resource "aws_lambda_function_event_invoke_config" "plan_next_week_lambda_event_invoke_config" {
  function_name = aws_lambda_function.plan_next_week_lambda.function_name

  destination_config {
    on_failure {
      destination = aws_sns_topic.plan_next_week_lambda_error_topic.arn
    }
  }
}

# Create the IAM role
resource "aws_iam_role" "plan_next_week_lambda_role" {
  name = "plan_next_week_lambda_role"
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
  role   = aws_iam_role.plan_next_week_lambda_role.id
  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Action   = "sns:Publish"
        Effect   = "Allow"
        Resource = aws_sns_topic.plan_next_week_lambda_error_topic.arn
      },
    ]
  })
}

# Attach the AWSLambdaBasicExecutionRole policy to the IAM role to log to cloudwatch
resource "aws_iam_role_policy_attachment" "lambda_logs" {
  role       = aws_iam_role.plan_next_week_lambda_role.name
  policy_arn = "arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole"
}

# Create the CloudWatch Event Rule for work agenda
resource "aws_cloudwatch_event_rule" "plan_next_week_work_schedule" {
  name        = "plan_next_week_work_schedule"
  description = "Schedule for running the plan_next_week_lambda for work agenda"
  schedule_expression = "cron(0 4 * * ? 0)"
}

# Create the CloudWatch Event Rule for work personal
resource "aws_cloudwatch_event_rule" "plan_next_week_personal_schedule" {
  name        = "plan_next_week_personal_schedule"
  description = "Schedule for running the plan_next_week_lambda for personal agenda"
  schedule_expression = "cron(0 4 * * ? 0)"
}

# Create the CloudWatch Event Target for work agenda
resource "aws_cloudwatch_event_target" "plan_next_week_work_target" {
  rule      = aws_cloudwatch_event_rule.plan_next_week_work_schedule.name
  target_id = aws_lambda_function.plan_next_week_lambda.function_name
  arn       = aws_lambda_function.plan_next_week_lambda.arn

  input = jsonencode({
    "agenda_id": var.googlecalendar_work_agenda_id
  })
}

# Create the CloudWatch Event Target for personal agenda
resource "aws_cloudwatch_event_target" "plan_next_week_personal_target" {
  rule      = aws_cloudwatch_event_rule.plan_next_week_personal_schedule.name
  target_id = aws_lambda_function.plan_next_week_lambda.function_name
  arn       = aws_lambda_function.plan_next_week_lambda.arn

  input = jsonencode({
    "agenda_id": var.googlecalendar_personal_agenda_id
  })
}

# Permission to allow CloudWatch to invoke the Lambda function
resource "aws_lambda_permission" "allow_cloudwatch_work" {
  statement_id  = "AllowExecutionFromCloudWatch_work"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.plan_next_week_lambda.function_name
  principal     = "events.amazonaws.com"
  source_arn    = aws_cloudwatch_event_rule.plan_next_week_work_schedule.arn
}

# Permission to allow CloudWatch to invoke the Lambda function
resource "aws_lambda_permission" "allow_cloudwatch_personal" {
  statement_id  = "AllowExecutionFromCloudWatch_personal"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.plan_next_week_lambda.function_name
  principal     = "events.amazonaws.com"
  source_arn    = aws_cloudwatch_event_rule.plan_next_week_personal_schedule.arn
}
