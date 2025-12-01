data "azurerm_client_config" "current" {}

resource "azurerm_resource_group" "this" {
  name     = "${var.base_name}-rg"
  location = var.location
}

resource "azurerm_key_vault" "this" {
  name                = "${var.base_name}-kv"
  location            = azurerm_resource_group.this.location
  resource_group_name = azurerm_resource_group.this.name
  tenant_id           = data.azurerm_client_config.current.tenant_id

  sku_name                 = "standard"
  purge_protection_enabled = true
}

resource "azurerm_key_vault_access_policy" "this" {
  key_vault_id = azurerm_key_vault.this.id
  tenant_id    = data.azurerm_client_config.current.tenant_id
  object_id    = data.azurerm_client_config.current.object_id

  key_permissions = [
    "Create",
    "Get",
    "Delete",
    "Purge",
    "GetRotationPolicy",
  ]
}

resource "azurerm_storage_account" "this" {
  name                     = "${var.base_name}sa"
  location                 = azurerm_resource_group.this.location
  resource_group_name      = azurerm_resource_group.this.name
  account_tier             = "Standard"
  account_replication_type = "LRS"
}

resource "azurerm_ai_services" "this" {
  name                = "${var.base_name}aiservices"
  location            = azurerm_resource_group.this.location
  resource_group_name = azurerm_resource_group.this.name
  sku_name            = "S0"
}

resource "azurerm_ai_foundry" "this" {
  name                = "${var.base_name}aifoundry"
  location            = azurerm_ai_services.this.location
  resource_group_name = azurerm_resource_group.this.name
  storage_account_id  = azurerm_storage_account.this.id
  key_vault_id        = azurerm_key_vault.this.id
  identity {
    type = "SystemAssigned"
  }
}

resource "azurerm_ai_foundry_project" "this" {
  name               = "${var.base_name}aifoundryproject"
  location           = azurerm_ai_foundry.this.location
  ai_services_hub_id = azurerm_ai_foundry.this.id
}
