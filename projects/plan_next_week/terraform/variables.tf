variable "function_name" {
  description = "The name of the lambda function"
  type        = string
}

variable "notion_task_database_id" {
  description = "The id of the Notion database for tasks"
  type        = string
}

variable "googlecalendar_agenda_ids" {
  description = "The ids of the Google Calendar agendas to integrate"
  type        = map(string)
}

variable "googlecalendar_work_agenda_id" {
  description = "The id of the Google Calendar work agenda"
  type        = string
}

variable "googlecalendar_personal_agenda_id" {
  description = "The id of the Google Calendar personal agenda"
  type        = string
}
