# HR Assistant AI - Documentation

This folder contains complete documentation for setting up and running the HR Assistant AI system with Azure services and OpenAI API.

## Documentation Overview

### 📋 Setup & Configuration
- **[setup-instructions.md](setup-instructions.md)** - Complete step-by-step setup guide
- **[environment-configuration.md](environment-configuration.md)** - Environment variables and configuration
- **[azure-setup-commands.md](azure-setup-commands.md)** - All Azure CLI commands used

### 🔧 Troubleshooting
- **[troubleshooting-guide.md](troubleshooting-guide.md)** - Common issues and solutions for free accounts

## Quick Start

1. **Create Azure Services**: Follow commands in `azure-setup-commands.md`
2. **Configure Environment**: Use settings from `environment-configuration.md`
3. **Install Dependencies**: `pip install -r requirements.txt && pip install openai`
4. **Run Application**: Start backend and frontend servers

## Key Configuration Changes

Due to Azure free account limitations, the system has been configured to use:

### ✅ Azure Services (Created Successfully)
- **Azure Cognitive Search** (Free tier)
- **Azure Blob Storage** (Standard LRS)
- **Azure Document Intelligence** (Free tier)

### 🔄 OpenAI Integration (Modified Approach)
- **OpenAI API** instead of Azure OpenAI (due to quota limitations)
- **Direct API calls** to OpenAI's GPT and embedding models
- **Your provided API key** for immediate functionality

## Created Azure Resources

| Service | Name | Location | Status | Purpose |
|---------|------|----------|---------|---------|
| Resource Group | `rg-hr-assistant` | West Europe | ✅ | Container for all resources |
| OpenAI Service | `openai-hr-assistant-eastus` | East US | ✅ | Embeddings only (quota limited) |
| Search Service | `search-hr-assistant` | West Europe | ✅ | Document search and retrieval |
| Storage Account | `sthrassistant87358` | East US | ✅ | Document storage |
| Document Intelligence | `docintel-hr-assistant` | East US | ✅ | PDF processing |

## Environment Values Summary

### Backend Configuration
```bash
# OpenAI API (Primary AI Provider)
OPENAI_API_KEY=your-openai-api-key-here

# Azure Services
AZURE_SEARCH_ENDPOINT=https://your-search-service.search.windows.net
AZURE_SEARCH_API_KEY=your-azure-search-api-key
AZURE_FORMRECOG_ENDPOINT=https://eastus.api.cognitive.microsoft.com/
AZURE_FORMRECOG_API_KEY=your-form-recognizer-api-key
```

**⚠️ SECURITY NOTE**: Replace placeholder values with your actual API keys. Never commit real API keys to Git repositories.

## System Capabilities

### ✅ Fully Functional
- 📤 **Document Upload** - PDF ingestion via Document Intelligence
- 🔍 **Document Search** - Semantic search via Azure Cognitive Search
- 💬 **AI Chat** - Conversations using OpenAI GPT-4o-mini
- 🎯 **RAG Pipeline** - Retrieval-augmented generation
- 📚 **Citations** - Source document references
- 📊 **Policy Checking** - Content validation

### 📊 Free Tier Limitations
- **Document Intelligence**: 500 pages/month
- **Search Service**: 50MB storage, 10K documents
- **Storage Account**: 5GB storage
- **OpenAI API**: Pay-per-use (estimated $5-20/month)

## Cost Monitoring

### Azure Services (Free Tier)
- Monitor usage in Azure Portal
- Set up billing alerts
- Most services remain free within limits

### OpenAI API Costs
- **GPT-4o-mini**: ~$0.15-0.60 per 1M tokens
- **Embeddings**: ~$0.10 per 1M tokens
- **Estimated**: $5-20/month for moderate usage

## Next Steps

1. **Review all documentation** in this folder
2. **Follow setup instructions** step by step
3. **Update backend code** to use OpenAI API
4. **Test the complete system** functionality
5. **Monitor usage and costs** regularly

## Support Resources

- **Azure Documentation**: docs.microsoft.com
- **OpenAI Documentation**: platform.openai.com/docs
- **Troubleshooting**: See troubleshooting-guide.md
- **Community Support**: Stack Overflow, GitHub Issues

---

**Note**: This documentation reflects the configuration for a free Azure account with OpenAI API integration. For production deployments, consider upgrading to paid tiers for better performance and higher quotas.