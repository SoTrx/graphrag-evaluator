variable "base_name" {
  description = "Base name for all resources"
  type        = string
}

variable "subscription_id" {
  type        = string
  description = "The Azure Subscription ID where the resources will be created"
}

variable "location" {
  type        = string
  default     = "eastus2"
  description = "The Azure region where the resources should be created"
}

variable "tags" {
  type        = map(any)
  description = "The custom tags for all resources"
  default     = {}
}
