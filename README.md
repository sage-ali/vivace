# Vivace Integration API

## Overview

The Vivace Integration API enhances user queries with relevant information retrieved from a knowledge base using Retrieval-Augmented Generation (RAG). This project uses FastAPI for the API and Google Generative AI for generating responses.

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
- pypdf

## Setup

1.  Clone the repository:

    ```bash
    git clone <repository_url>
    cd vivace_integration
    ```
2.  Create a virtual environment:

    ```bash
    python3 -m venv venv
    source venv/bin/activate
    ```
3.  Install dependencies:

    ```bash
    pip install -r requirements.txt
    ```
4.  Set up environment variables:

    *   Create a `.env` file in the root directory.
    *   Add the following environment variables:

        ```
        GOOGLE_API_KEY=<your_google_api_key>
        BASE_URL=<your_base_url>
        ```

## Usage

### API Endpoints

-   **GET /healthcheck**: Checks if the server is active.
-   **POST /api/vivace**: Modifies the message based on the content of the input message.

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
      "default": "https://aws.amazon.com/what-is/retrieval-augmented_generation/"
    }
  ],
  "message": "Tell me about RAG."
}
```

### Running Tests

To run the tests, use the following command:

```bash
pytest vivace_integration/tests
```

## Deployment

### Docker Hub

1. Build the Docker image:

    ```bash
    docker build -t <your_dockerhub_username>/vivace:<tag> .
    ```

2. Log in to Docker Hub:

    ```bash
    docker login -u <your_dockerhub_username> -p <your_dockerhub_password>
    ```

3. Push the Docker image to Docker Hub:

    ```bash
    docker push <your_dockerhub_username>/vivace:<tag>
    ```

### Render

1. Create a Render account and log in.
2. Create a new web service on Render.
3. Connect your Docker repository to Render.
4. Configure the following setting:

    *   **Environment Variables:** Add the `GOOGLE_API_KEY` and `BASE_URL` environment variables.

5. Set up Render to pull the latest Docker image from Docker Hub:

    *   Go to the Render dashboard and select your service.
    *   Under the "Deploy" tab, set the Docker image to pull from Docker Hub:
        ```
        docker.io/<your_dockerhub_username>/vivace:<tag>
        ```

    *   The `cd.yml` file is configured to automatically push the latest Docker image to Docker Hub and trigger a deployment on Render.

6. Deploy the service.

## Testing the Integration on Telex.im

1. **Add the Integration:**
    - Go to the Telex.im App page.
    - Add a new integration using the integration JSON found at the `/integration_setting` endpoint of your deployed service.

2. **Configure the Integration:**
    - In the integration settings, add the URL to the knowledge base. The URL can be a webpage or a link to download a PDF.

3. **Send a Query:**
    - Send a query to the channel where you have configured the integration.
    - The integration will process the query and provide a response using Retrieval-Augmented Generation (RAG).

### Example

- Add `https://docs.telex.im/docs/intro, https://docs.telex.im/docs/Integrations/intro` to the knowledge base url settings.
- Go to test channel and ask `What is telex and what are telex integrations?`

## Contributing

Contributions are welcome! Please open an issue or submit a pull request for any changes.

## License

This project is licensed under the MIT License.
