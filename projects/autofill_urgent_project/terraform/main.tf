# Create the Lambda function
resource "aws_lambda_function" "autofill_urgent_project_lambda" {
  function_name = "autofill_urgent_project_lambda"
  role          = aws_iam_role.autofill_urgent_project_lambda_role.arn
  handler       = "omnilife_framework_automations.autofill_urgent_project_lambda.lambda_function.lambda_handler"
  runtime       = "python3.11"
  timeout       = 10
  memory_size   = 128
  publish       = true
  filename      = "../dist/autofill_urgent_project-0.1.0.zip"
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
