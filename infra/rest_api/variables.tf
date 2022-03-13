variable "aws_account_id" {
  type = string
}

variable "aws_region" {
  type = string
}

variable "project" {
  type = string
}

variable "stage_name" {
  type = string
}
variable "service_name" {
  type = string
}

variable "fifo_queue" {
  type    = bool
  default = false
}

variable "retention_time" {
  description = "Override retention time"
  type        = number
  default     = 345600
}
