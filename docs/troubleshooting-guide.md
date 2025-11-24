# Troubleshooting Guide - Free Account Limitations

This guide addresses common issues when setting up the HR Assistant AI system with a free Azure account.

## Common Issues and Solutions

### 1. Azure OpenAI Quota Issues

#### Problem
```
ERROR: (InsufficientQuota) This operation require 10 new capacity in quota Tokens Per Minute (thousands) - gpt-4o, which is bigger than the current available capacity 0.
```

#### Solution
**Use OpenAI API instead of Azure OpenAI:**

1. **Update environment configuration** to use OpenAI API key
2. **Modify backend code** to use standard OpenAI client
3. **Install OpenAI Python library**: `pip install openai`

#### Code Changes Required:
```python
# Before (Azure OpenAI)
from azure.ai.openai import AzureOpenAI
client = AzureOpenAI(endpoint=endpoint, api_key=api_key, api_version=api_version)

# After (OpenAI API)
from openai import OpenAI
client = OpenAI(api_key=openai_api_key)
```

### 2. Model Deployment Failures

#### Problem
```
ERROR: (InvalidResourceProperties) The specified SKU 'Standard' for model 'gpt-4o' is not supported in this region.
```

#### Root Causes:
- Free accounts have limited model access
- Regional availability restrictions
- Quota limitations

#### Solutions:
1. **Use OpenAI API** (recommended)
2. **Request quota increase** through Azure Portal
3. **Try different regions** (East US, West US)
4. **Use free tier models** only

### 3. Search Service Quota Exceeded

#### Problem
```
ERROR: (ServiceQuotaExceeded) Creating search service would exceed quota of sku 'free' for subscription.
```

#### Solution
**Use existing search service:**
```bash
# Check existing services
az search service list --resource-group rg-hr-assistant

# Use existing service name in configuration
AZURE_SEARCH_ENDPOINT=https://existing-search-service.search.windows.net
```

### 4. Storage Account Name Conflicts

#### Problem
```
ERROR: The storage account name 'sthrassistant' is not available.
```

#### Solution
**Generate unique names:**
```bash
# Use timestamp suffix
STORAGE_NAME="sthrassistant$(date +%s | tail -c 6)"
az storage account create --name $STORAGE_NAME ...
```

### 5. Document Intelligence Free Tier Limits

#### Problem
- 500 pages per month limit
- Processing fails for large documents

#### Solutions:
1. **Monitor monthly usage** in Azure Portal
2. **Split large PDFs** into smaller files
3. **Use document preview** before full processing
4. **Implement usage tracking** in application

### 6. Connection String Issues

#### Problem
```
ERROR: There are no credentials provided in your command and environment
```

#### Solution
**Get complete connection string:**
```bash
az storage account show-connection-string \
  --name your-storage-account \
  --resource-group rg-hr-assistant \
  --query "connectionString" -o tsv
```

### 7. Search Index Creation Issues

#### Problem
- Vector search not supported in free tier
- Index creation fails

#### Solution
**Simplified index schema for free tier:**
```json
{
  "fields": [
    {"name": "id", "type": "Edm.String", "key": true},
    {"name": "content", "type": "Edm.String", "searchable": true},
    {"name": "metadata", "type": "Edm.String", "filterable": true}
  ]
}
```

### 8. Rate Limiting and Throttling

#### Problem
- API calls being throttled
- Service temporarily unavailable

#### Solutions:
1. **Implement retry logic** with exponential backoff
2. **Add delays** between API calls
3. **Monitor usage quotas** in Azure Portal
4. **Use connection pooling** for efficiency

```python
import time
import random
from tenacity import retry, stop_after_attempt, wait_exponential

@retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=4, max=10))
def api_call_with_retry():
    # Your API call here
    pass
```

## Free Tier Service Limits

### Azure Cognitive Search (Free)
- **Storage**: 50 MB
- **Documents**: 10,000 documents
- **Indexes**: 3 indexes
- **Search Units**: 3 units per service

### Azure Storage Account (Free)
- **Storage**: 5 GB blob storage
- **Transactions**: 20,000 read/write operations
- **Bandwidth**: 5 GB egress per month

### Azure Document Intelligence (Free)
- **Pages**: 500 pages per month
- **API Calls**: Rate limited
- **File Size**: 50 MB per file

### OpenAI API (Pay-per-use)
- **Rate Limits**: Vary by tier (typically 3 RPM for new accounts)
- **Token Limits**: Model-specific
- **Cost**: Pay per token used

## Monitoring and Cost Control

### 1. Monitor Azure Usage
```bash
# Check resource usage
az consumption usage list --start-date 2024-01-01 --end-date 2024-01-31

# Monitor specific service costs
az consumption usage list --metric-names "Cost" --resource-group rg-hr-assistant
```

### 2. Set Up Billing Alerts
1. Navigate to **Azure Portal > Cost Management + Billing**
2. Create **Budget** with spending limits
3. Set up **Alert Rules** for threshold notifications

### 3. Monitor OpenAI Usage
1. Check usage in **OpenAI Dashboard**
2. Set up **usage alerts**
3. Monitor **token consumption** patterns

## Performance Optimization for Free Tier

### 1. Reduce API Calls
```python
# Cache embeddings
embedding_cache = {}

def get_cached_embedding(text):
    if text in embedding_cache:
        return embedding_cache[text]
    
    embedding = get_embedding(text)
    embedding_cache[text] = embedding
    return embedding
```

### 2. Optimize Search Queries
```python
# Use simpler queries for free tier
simple_query = {
    "search": user_query,
    "top": 3,  # Limit results
    "select": "content,metadata"  # Only needed fields
}
```

### 3. Batch Operations
```python
# Process multiple documents in batches
batch_size = 5
for i in range(0, len(documents), batch_size):
    batch = documents[i:i+batch_size]
    process_batch(batch)
    time.sleep(1)  # Rate limiting
```

## Emergency Procedures

### 1. Service Outage
1. **Check Azure Status** page
2. **Switch to backup region** if configured
3. **Use local fallbacks** for critical functionality

### 2. Quota Exceeded
1. **Implement graceful degradation**
2. **Queue requests** for later processing
3. **Notify users** of temporary limitations

### 3. Cost Overrun
1. **Pause expensive operations**
2. **Review usage patterns**
3. **Implement cost controls**

## Getting Help

### Azure Support
- **Azure Portal**: Help + Support section
- **Community Forums**: Microsoft Q&A
- **Documentation**: docs.microsoft.com

### OpenAI Support
- **OpenAI Help Center**: help.openai.com
- **Community Forum**: community.openai.com
- **API Documentation**: platform.openai.com/docs

### Emergency Contacts
- **Azure Technical Support**: Available with paid plans
- **Community Support**: Stack Overflow, GitHub Issues
- **Documentation**: Comprehensive guides available