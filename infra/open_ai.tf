resource "azurerm_cognitive_account" "open_ai" {
  name                          = format("oai-%s", local.resource_suffix_kebabcase)
  location                      = azurerm_resource_group.this.location
  resource_group_name           = azurerm_resource_group.this.name
  kind                          = "OpenAI"
  sku_name                      = "S0"
  public_network_access_enabled = true
  custom_subdomain_name         = format("oai-%s", local.resource_suffix_kebabcase)
  tags                          = local.tags
}

resource "azurerm_cognitive_deployment" "gpt_4_1" {
  name                 = "gpt-4.1"
  cognitive_account_id = azurerm_cognitive_account.open_ai.id
  model {
    format  = "OpenAI"
    name    = "gpt-4.1"
    version = "2025-04-14"
  }

  sku {
    name     = "DataZoneStandard"
    capacity = 100
  }
}

resource "azurerm_cognitive_deployment" "gpt5_model" {
  name                 = "gpt-5.0"
  cognitive_account_id = azurerm_cognitive_account.open_ai.id
  model {
    format  = "OpenAI"
    name    = "gpt-5-chat"
    version = "2025-10-03"
  }

  sku {
    name     = "GlobalStandard"
    capacity = 150
  }
}

resource "azurerm_cognitive_deployment" "router_chat_model" {
  name                 = "model-router"
  cognitive_account_id = azurerm_cognitive_account.open_ai.id
  model {
    format  = "OpenAI"
    name    = "model-router"
    version = "2025-05-19"
  }

  sku {
    name     = "GlobalStandard"
    capacity = 100
  }
}

resource "azurerm_cognitive_deployment" "embedding_model" {
  name                 = "text-embedding-3-large"
  cognitive_account_id = azurerm_cognitive_account.open_ai.id
  model {
    format  = "OpenAI"
    name    = "text-embedding-3-large"
    version = "1"
  }

  sku {
    name = "GlobalStandard"
  }
}

resource "azapi_resource" "open_ai_connection" {
  type      = "Microsoft.CognitiveServices/accounts/connections@2025-04-01-preview"
  name      = format("con-%s", azurerm_cognitive_account.open_ai.name)
  parent_id = azapi_resource.ai_services.id

  body = {
    properties = {
      category = "AzureOpenAI",
      target   = azurerm_cognitive_account.open_ai.endpoint,
      authType = "ApiKey",
      credentials = {
        key = azurerm_cognitive_account.open_ai.primary_access_key
      }
      isSharedToAll = true,
      metadata = {
        ApiType    = "Azure",
        ResourceId = azurerm_cognitive_account.open_ai.id
      }
    }
  }
  response_export_values = ["*"]
}
