variable "region" {
  description = "AWS region"
  type        = string
  default     = "eu-north-1"
}

variable "project_name" {
  description = "Prefix and name"
  type        = string
  default     = "testdemo"
}

variable "profile_name" {
  description = "AWS profile name"
  type        = string
  default     = "tutorial-user"
}
