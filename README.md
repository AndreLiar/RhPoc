# HR Assistant AI

An intelligent HR document assistant that uses Azure services and OpenAI API to provide conversational access to HR policies and documents. Upload PDF documents, ask questions, and get accurate answers with source citations.

## 🏗️ System Architecture

The system uses **OpenAI API** as the primary AI provider with **Azure services** for:

- **Azure Cognitive Search** - Document indexing and semantic search
- **Azure Document Intelligence** - PDF text extraction and processing  
- **Azure Blob Storage** - Document storage
- **Azure OpenAI** - Backup/optional AI provider (quota limited)

## 🚀 Quick Start

### Prerequisites

1. **Azure Account** - Free tier account with active subscription
2. **OpenAI API Key** - Get from [OpenAI Platform](https://platform.openai.com/api-keys)
3. **Python 3.11+** - For running the applications
4. **Azure CLI** - For managing Azure resources ([Install Guide](https://docs.microsoft.com/en-us/cli/azure/install-azure-cli))

### 1. Clone the Repository

```bash
git clone <repository-url>
cd Poc
```

### 2. Set Up Azure Services

Login to Azure and create the required services:

```bash
# Login to Azure
az login

# Create resource group
az group create --name rg-hr-assistant --location "West Europe"

# Create Azure Cognitive Search (Free tier)
az search service create --name search-hr-assistant --resource-group rg-hr-assistant --location "West Europe" --sku free

# Create Storage Account
STORAGE_NAME="sthrassistant$(date +%s | tail -c 6)"
az storage account create --name $STORAGE_NAME --resource-group rg-hr-assistant --location "East US" --sku Standard_LRS

# Create Document Intelligence (Free tier)
az cognitiveservices account create --name docintel-hr-assistant --resource-group rg-hr-assistant --location "East US" --kind FormRecognizer --sku F0

# Optional: Create Azure OpenAI (if available in your region)
az cognitiveservices account create --name openai-hr-assistant --resource-group rg-hr-assistant --location "East US" --kind OpenAI --sku S0
```

### 3. Get Service Keys and Endpoints

Extract the connection details for your services:

```bash
# Get Search service endpoint and key
az search admin-key show --service-name search-hr-assistant --resource-group rg-hr-assistant
az search service show --name search-hr-assistant --resource-group rg-hr-assistant --query "searchServiceEndpoint"

# Get Storage connection string
az storage account show-connection-string --name $STORAGE_NAME --resource-group rg-hr-assistant

# Get Document Intelligence endpoint and key
az cognitiveservices account show --name docintel-hr-assistant --resource-group rg-hr-assistant --query "properties.endpoint"
az cognitiveservices account keys list --name docintel-hr-assistant --resource-group rg-hr-assistant
```

### 4. Configure Environment Variables

#### Backend Configuration

Create `backend/.env` with your service details:

```bash
# FastAPI metadata
APP_NAME=HR Assistant Backend
APP_VERSION=1.0.0
ENVIRONMENT=dev
LOG_LEVEL=INFO

# OpenAI API (Primary AI Provider)
OPENAI_API_KEY=your_openai_api_key_here
OPENAI_CHAT_MODEL=gpt-4o-mini
OPENAI_EMBEDDING_MODEL=text-embedding-ada-002

# Azure Cognitive Search
AZURE_SEARCH_ENDPOINT=https://search-hr-assistant.search.windows.net
AZURE_SEARCH_API_KEY=your_search_api_key_here
AZURE_SEARCH_INDEX_NAME=hr-documents

# Azure Blob Storage
AZURE_BLOB_CONNECTION_STRING=your_storage_connection_string_here
AZURE_STORAGE_CONTAINER=hr-documents

# Azure Document Intelligence
AZURE_FORMRECOG_ENDPOINT=https://eastus.api.cognitive.microsoft.com/
AZURE_FORMRECOG_API_KEY=your_document_intelligence_key_here

# Azure OpenAI (Optional - if you have quota)
AZURE_OPENAI_ENDPOINT=your_azure_openai_endpoint_here
AZURE_OPENAI_API_KEY=your_azure_openai_key_here
AZURE_OPENAI_CHAT_DEPLOYMENT=gpt-4o
AZURE_OPENAI_EMBEDDING_DEPLOYMENT=text-embedding-3-large
AZURE_OPENAI_API_VERSION=2024-02-15-preview
```

#### Frontend Configuration

Create `frontend/streamlit/.env`:

```bash
BACKEND_URL=http://localhost:8000/api/v1/hr/query
BACKEND_UPLOAD_URL=http://localhost:8000/api/v1/hr/upload
```

### 5. Install Dependencies and Run

#### Install Backend Dependencies

```bash
cd backend
pip install -r requirements.txt
```

#### Install Frontend Dependencies

```bash
cd frontend/streamlit
pip install -r requirements.txt
```

#### Start the Applications

**Terminal 1 - Backend:**
```bash
cd backend
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

**Terminal 2 - Frontend:**
```bash
cd frontend/streamlit
streamlit run app.py
```

### 6. Access the Application

1. Open your browser to `http://localhost:8501`
2. Upload HR policy PDFs using the sidebar
3. Ask questions in the chat interface
4. View source citations for answers

## 💡 Usage

1. **Upload Documents**: Use the sidebar to upload HR policy PDFs
2. **Ask Questions**: Type HR-related questions in the chat
3. **View Sources**: Check the sidebar for document citations
4. **Get Answers**: Receive AI-powered responses with source references

## 💰 Cost Considerations

### Azure Services (Free Tier)
- **Cognitive Search**: 50MB storage, 3 search units
- **Blob Storage**: 5GB storage, 20,000 operations/month
- **Document Intelligence**: 500 pages/month
- **Azure OpenAI**: Limited quota (if available)

### OpenAI API Costs
- **GPT-4o-mini**: ~$0.15 per 1M input tokens, ~$0.60 per 1M output tokens
- **Text Embeddings**: ~$0.10 per 1M tokens
- **Estimated**: $5-20/month for moderate usage

## 🔧 Troubleshooting

### Common Issues

1. **Azure Service Unavailable**: Some regions may not have all services available
2. **Quota Exceeded**: Free tier limits may be reached
3. **API Key Issues**: Ensure all keys are correctly copied and formatted

### Getting Help

- Check the `docs/` folder for detailed setup instructions
- Review `docs/troubleshooting-guide.md` for specific issues
- Verify environment variables are correctly set

## 📁 Project Structure

```
Poc/
├── backend/                 # FastAPI backend
│   ├── app/
│   │   ├── routers/        # API endpoints
│   │   ├── langgraph/      # Conversation flow
│   │   ├── azure/          # Azure integrations
│   │   └── ingestion/      # Document processing
│   └── requirements.txt
├── frontend/               # Streamlit frontend
│   └── streamlit/
│       ├── components/     # UI components
│       ├── app.py         # Main app
│       └── requirements.txt
└── docs/                   # Documentation
    ├── setup-instructions.md
    ├── troubleshooting-guide.md
    └── azure-setup-commands.md
```

## 🔐 Security Notes

- Never commit API keys to version control
- Use environment variables for all sensitive data
- Rotate keys regularly for production use
- Monitor usage to avoid unexpected costs
- Review Azure security best practices

## 📚 Documentation

For detailed setup instructions, see the `docs/` folder:
- [Complete Setup Guide](docs/setup-instructions.md)
- [Environment Configuration](docs/environment-configuration.md)
- [Azure Commands](docs/azure-setup-commands.md)
- [Troubleshooting](docs/troubleshooting-guide.md)

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.# RhPoc
