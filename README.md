# Prompt : Website-AI-Assistant

This project provides a REST API built with FastAPI to create and query chatbots. These chatbots can be trained using content scraped from websites and uploaded documents (PDF and TXT). The chatbots use vector databases to efficiently answer questions based on the ingested data, leveraging the power of Large Language Models (LLMs) via OpenAI.

## Features

- **Bot Creation**:
  - Create a chatbot by providing a website URL. The application will crawl the website, extract text content, and use it to train the bot.
  - Upload local files (PDF and TXT formats) to train your chatbot with specific documents.
  - Supports combining website crawling and file uploads for comprehensive bot training.
- **Intelligent Querying**:
  - Query your chatbot with natural language questions.
  - Provides context-aware answers based on the information learned from the website and documents.
- **Vector Database**:
  - Utilizes ChromaDB for efficient storage and retrieval of document embeddings, enabling fast and relevant query responses.
- **Web Crawling**:
  - Employs `crawl4ai` for robust website crawling, handling various website structures and content types.
  - Extracts text content from web pages and PDFs hosted on websites.
  - Basic header and footer removal from crawled website content to improve data quality.
- **Document Loading and Chunking**:
  - Supports loading PDF and TXT documents.
  - Offers different document chunking strategies (`semantic`, `recursive`, `markdown`, `auto`) to optimize information retrieval.
- **OpenAI Integration**:
  - Leverages OpenAI's powerful models (specifically `gpt-4o` in the code) to formulate intelligent answers based on retrieved document chunks.
- **API Endpoints**:
  - `/create_bot/`: Endpoint to create a new chatbot with a website URL and/or document uploads.
  - `/query_bot/`: Endpoint to query an existing chatbot with a specific question.
- **CORS Support**:
  - Implements CORS middleware to allow cross-origin requests, making the API accessible from web browsers.
- **Caching**:
  - Implements caching for vector databases using `lru_cache` to improve performance and reduce loading times for frequently accessed bots.
- **Logging**:
  - Includes comprehensive logging for debugging and monitoring the application's behavior.

## Installation

### Prerequisites

- **Python 3.8+**
- **pip** (Python package installer)
- **OpenAI API Key**: You will need an OpenAI API key to use the LLM features. [Get your API key here](https://www.google.com/url?sa=E&source=gmail&q=https://platform.openai.com/api-keys).
- **Ngrok Account** (Optional): If you want to expose the API publicly using Ngrok. [Sign up for Ngrok](https://www.google.com/url?sa=E&source=gmail&q=https://ngrok.com/).

### Steps

1.  **Clone the repository:**

    ```bash
    git clone https://github.com/visha1Sagar/No-Code-Website-AI-Assistant.git
    cd No-Code-Website-AI-Assistant
    ```

2.  **Create a virtual environment (recommended):**

    ```bash
    python -m venv venv
    source venv/bin/activate  # On Linux/macOS
    venv\Scripts\activate  # On Windows
    ```

3.  **Install dependencies:**

    ```bash
    pip install -r requirements.txt
    ```

4.  **Set up environment variables:**

    - Create a `.env` file in the project root directory.
    - Add your OpenAI API key to the `.env` file:
      ```env
      OPENAI_API_KEY=your_openai_api_key_here
      ```

## Usage

### Running the API

1.  **Navigate to the project directory in your terminal.**

2.  **Run the `app.py` file:**

    ```bash
    python app.py
    ```

3.  **Ngrok Public URL (Optional):**

    - The application will attempt to connect to Ngrok and output a public URL in the console (e.g., `Public ngrok URL: https://your-ngrok-url.ngrok.io`).
    - You can use this URL to access the API from anywhere.
    - **Note**: Ngrok provides a temporary public URL. For production use, consider deploying the API to a cloud platform or setting up a more permanent hosting solution.

4.  **Local API Access:**

    - The API will also be accessible locally at `http://localhost:8000`.

### API Endpoints

#### 1\. Create Bot (`/create_bot/`)

- **Method:** `POST`

- **Endpoint URL:** `/create_bot/` (or the Ngrok public URL if running with Ngrok)

- **Request Body (Form Data):**

  - `website_url`: `string` (Required) - The URL of the website to crawl for training data.
  - `files`: `List[UploadFile]` (Optional) - Files to upload for training data. Supports PDF and TXT files. Use the form-data format to upload files.

- **Example Request (using `curl`):**

  **Website URL Only:**

  ```bash
  curl -X POST \
    -F "website_url=[https://www.example.com](https://www.example.com)" \
    http://localhost:8000/create_bot/
  ```

  **Website URL and File Upload:**

  ```bash
  curl -X POST \
    -F "website_url=[https://www.example.com](https://www.example.com)" \
    -F "files=@/path/to/your/document1.pdf" \
    -F "files=@/path/to/your/document2.txt" \
    http://localhost:8000/create_bot/
  ```

- **Response (JSON):**

  ```json
  {
    "bot_id": "your_bot_id_uuid",
    "message": "Bot created and saved successfully!"
  }
  ```

  - `bot_id`: A unique ID for the newly created chatbot. Store this `bot_id` to query the bot later.
  - `message`: A success message.

- **Error Response (JSON):**

  ```json
  {
    "detail": "Bot creation failed. Check server logs for errors."
  }
  ```

  - Status Code: `500` (Internal Server Error) - Indicates bot creation failure. Check the server logs for more details on the error.

#### 2\. Query Bot (`/query_bot/`)

- **Method:** `POST`

- **Endpoint URL:** `/query_bot/` (or the Ngrok public URL if running with Ngrok)

- **Request Body (JSON):**

  ```json
  {
    "bot_id": "your_bot_id_uuid", // Replace with the bot_id from the create_bot response
    "query": "Your question here?",
    "context": "Optional context to provide to the bot. Can be empty string."
  }
  ```

  - `bot_id`: The `bot_id` of the chatbot you want to query.
  - `query`: The question you want to ask the chatbot.
  - `context`: _(Optional)_ Additional context or instructions for the chatbot to consider when answering. Can be an empty string if no context is needed.

- **Example Request (using `curl`):**

  ```bash
  curl -X POST \
    -H "Content-Type: application/json" \
    -d '{
          "bot_id": "your_bot_id_uuid",
          "query": "What is this website about?",
          "context": ""
        }' \
    http://localhost:8000/query_bot/
  ```

- **Response (JSON):**

  ```json
  {
    "answer": "The answer to your question based on the bot's knowledge."
  }
  ```

  - `answer`: The chatbot's response to your query.

- **Error Response (JSON):**

  ```json
  {
    "detail": "Bot with id 'your_bot_id_uuid' not found or could not be loaded."
  }
  ```

  - Status Code: `404` (Not Found) - Indicates that the provided `bot_id` is invalid or the bot could not be loaded.

## Directory Structure

```
.
├── app.py                      # Main FastAPI application file, API endpoints definition.
├── ask_openai.py              # Handles interactions with the OpenAI API.
├── document_loader.py         # Functions for loading documents, chunking, and vector database operations.
├── new_pdf.py                  # Web crawler using crawl4ai and PDF text extraction logic.
├── remove_header.py             # Functionality for removing headers and footers from crawled content (using OpenAI).
├── tree_from_json.py          # Converts crawled JSON output to a tree structure and extracts markdown.
├── vector_db_storage/         # Directory to store Chroma vector databases (created at runtime).
├── venv/                       # (Optional) Virtual environment directory.
├── .env                        # (Optional) Environment variables file (API keys).
├── requirements.txt            # (Optional, but should be included) Project dependencies.
└── README.md                   # This README file.
```

## Contributing

Contributions are welcome\! Please feel free to submit pull requests with bug fixes, improvements, or new features.

## Contact

Team Chateaus

```

```
