# terraform import azurerm_resource_group.ai_learning /subscriptions/7939cc19-6638-45a9-b3ad-a87050a55491/resourceGroups/# rg-ai-learning
resource "azurerm_resource_group" "ai_learning" {
  name     = "rg-ai-learning"
  location = "eastus"
}

# terraform import azurerm_cognitive_account.aoai_learning \
# /subscriptions/7939cc19-6638-45a9-b3ad-a87050a55491/resourceGroups/rg-ai-learning/providers/Microsoft.CognitiveServices/accounts/aoai-learning-01
resource "azurerm_cognitive_account" "aoai_learning" {
  name                = "aoai-learning-01"
  resource_group_name = azurerm_resource_group.ai_learning.name
  location             = "eastus"
  kind                = "OpenAI"
  sku_name            = "S0"
}

# terraform import azurerm_cognitive_deployment.gpt_5_mini \
#   /subscriptions/7939cc19-6638-45a9-b3ad-a87050a55491/resourceGroups/rg-ai-learning/providers/Microsoft.CognitiveServices/accounts/aoai-learning-01/deployments/gpt-5-mini
resource "azurerm_cognitive_deployment" "gpt_5_mini" {
  name                 = "gpt-5-mini"
  cognitive_account_id = azurerm_cognitive_account.aoai_learning.id

  model {
    format  = "OpenAI"
    name    = "gpt-5-mini"
    version = "2025-08-07" 
  }

  sku {
    name     = "GlobalStandard" 
    capacity = 10
  }
}



# terraform import azurerm_cognitive_deployment.gpt_chat_latest_judge \
#   /subscriptions/7939cc19-6638-45a9-b3ad-a87050a55491/resourceGroups/rg-ai-learning/providers/Microsoft.CognitiveServices/accounts/aoai-learning-01/deployments/gpt-chat-latest-judge
resource "azurerm_cognitive_deployment" "gpt_chat_latest_judge" {
  name                 = "gpt-chat-latest-judge"
  cognitive_account_id = azurerm_cognitive_account.aoai_learning.id

  model {
    format  = "OpenAI"
    name    = "gpt-chat-latest"
    version = "2026-08-06"
  }

  sku {
    name     = "GlobalStandard"
    capacity = 3
  }
}

# terraform import azurerm_search_service.ai_search \
#   /subscriptions/7939cc19-6638-45a9-b3ad-a87050a55491/resourceGroups/rg-ai-learning/providers/Microsoft.Search/searchServices/aisearch-learning-01
resource "azurerm_search_service" "ai_search" {
  name                = "aisearch-learning-01"
  resource_group_name = azurerm_resource_group.ai_learning.name
  location            = "eastus"
  authentication_failure_mode = "http401WithBearerChallenge"
  semantic_search_sku = "free"
  sku                 = "free" 
}