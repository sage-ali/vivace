# Vivace Integration API

## Overview

The Vivace Integration API enhances user queries with relevant information retrieved from a knowledge base using Retrieval-Augmented Generation (RAG). This project uses FastAPI for the API, FAISS for vector database management, and Google Generative AI for generating responses.

## Features

- Faster Access to Information
- Improved Collaboration
- Reduced Knowledge Silos
- Increased Efficiency
- Enhanced Onboarding
- Better Incident Response
- Streamlined Troubleshooting
- Augments user queries with relevant context from a knowledge base
- Uses Retrieval-Augmented Generation (RAG) for enhanced responses
- Improves collaboration and information access for DevOps and Software teams

## Requirements

- Python 3.10+
- FastAPI
- Sentence Transformers
- Langchain Community
- Google Generative AI
- Uvicorn
- Python-dotenv

## Setup


## Usage

### API Endpoints


- **GET /healthcheck**: Checks if the server is active.
- **POST /api/vivace**: Modifies the message based on the content of the input message.

### Example Request

To modify a message, send a POST request to `/api/vivace` with the following JSON payload:

```json
{
  "channel_id": "0192dd70-cdf1-7e15-8776-4fee4a78405e",
  "settings": [
    {
      "label": "Knowledge Base URL(separate multiple sources with commas)",
      "type": "text",
      "required": true,
      "default": "https://aws.amazon.com/what-is/retrieval-augmented-generation/"
    }
  ],
  "message": "Tell me about RAG."
}
```

### Running Tests

To run the tests, use the following command:

```bash
pytest
```

## Contributing

Contributions are welcome! Please open an issue or submit a pull request for any changes.

## License

This project is licensed under the MIT License.
