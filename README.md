
# Prompt : No Code based Website Assistant

This project provides a REST API built with FastAPI to create and query chatbots. These chatbots can be trained using content scraped from websites and uploaded documents (PDF and TXT).  The chatbots use vector databases to efficiently answer questions based on the ingested data, leveraging the power of Large Language Models (LLMs) via OpenAI.  **A frontend interface is also included to interact with the API and customize the chatbot widget.**

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
  - **Frontend Interface**:
      - **Chatbot Playground**:
          - **Real-time Customization**: Visually customize the chatbot widget in real-time, including:
              - Chatbot Name and Display Name
              - Welcome and Placeholder Messages
              - Header and Assistant Text
              - AI and User Message Background Colors
              - Accent Color for Buttons and Headers
              - Chat Icon Background Color
              - Profile Image Upload
          - **Chat Preview**: Provides a live preview of the chatbot widget as you customize it.
          - **Popup Chat Window**: Allows testing the chatbot interaction in a popup chat window directly from the playground.
          - **Configuration Saving**: *(Note: While UI elements for saving are present, backend persistence for frontend configuration is not implemented in the provided code.)*
      - **Training Data Upload**:
          - **Website Link Input**:  Input field to provide a website URL for crawling and training the chatbot.
          - **File Upload**: Drag and drop area or file selector for uploading PDF and TXT documents.
          - **Uploaded Files Management**: List of uploaded files with the ability to delete individual files.
          - **Save & Train**: Button to trigger the backend bot creation process using the provided website URL and uploaded files.
          - **Embedded Script Generation**: Generates a JavaScript code snippet to embed the chatbot widget on an external website after training.
          - **Copy to Clipboard**:  Easy copy button to copy the generated embedded script.

## Installation

### Prerequisites

  - **Python 3.8+**
  - **pip** (Python package installer)
  - **Node.js and npm** (for Frontend - if you plan to run the frontend)
  - **OpenAI API Key**: You will need an OpenAI API key to use the LLM features.  [Get your API key here](https://www.google.com/url?sa=E&source=gmail&q=https://platform.openai.com/api-keys).
  - **Ngrok Account** (Optional): If you want to expose the API publicly using Ngrok. [Sign up for Ngrok](https://www.google.com/url?sa=E&source=gmail&q=https://ngrok.com/).

### Backend Setup Steps

1.  **Clone the repository:**

    ```bash
    git clone https://github.com/visha1Sagar/The-Chateaus_Prompt.git
    cd The-Chateaus_Prompt
    ```

2.  **Create a virtual environment (recommended):**

    ```bash
    python -m venv venv
    source venv/bin/activate  # On Linux/macOS
    venv\Scripts\activate  # On Windows
    ```

3.  **Install backend dependencies:**

    ```bash
    pip install -r requirements.txt
    ```

4.  **Set up backend environment variables:**

      - Create a `.env` file in the project root directory.
      - Add your OpenAI API key to the `.env` file:
        ```env
        OPENAI_API_KEY=your_openai_api_key_here
        ```

### Frontend Setup Steps

1.  **Navigate to the `prompt-frontend` directory:**

    ```bash
    cd prompt-frontend
    ```

2.  **Install frontend dependencies:**

    ```bash
    npm install # or yarn install
    ```

    *(Ensure you have Node.js and npm or yarn installed.)*

3.  **Set up frontend environment variables:**

      - In `prompt-frontend`, create a `.env.local` file.
      - Define the backend API URL:
        ```env
        NEXT_PUBLIC_BACKEND_URL=http://localhost:8000 # or your Ngrok URL, or deployed backend URL for now it has been set to running backend Ngrok url
        ```

4.  **Run the frontend development server:**

    ```bash
    npm run dev # or yarn dev
    ```

5.  **Access the frontend:**

      - The frontend application will be accessible in your browser at `http://localhost:3000` (or the port shown in the console after running `npm run dev`).

## Usage

### Running the API and Frontend

1.  **Start the backend API:** Follow the "Running the API" steps in the "Usage" section above.
2.  **Start the frontend:** Follow the "Frontend Setup Steps" above to run the frontend development server.
3.  **Access the frontend in your browser at `http://localhost:3000`.**
4.  **Train your chatbot**:
      - Navigate to the "Train" page in the frontend.
      - Choose "Website Link and File Upload".
      - Enter the website URL and upload files if desired.
      - Click "Save" to train the chatbot. You will receive a script URL and a bot ID after successful training.
5.  **Customize the Chatbot Widget**:
      - Navigate to the "Playground" page in the frontend.
      - Customize the chatbot appearance and messages using the settings panel on the left.
      - Preview the chatbot widget on the right.
6.  **Embed the Chatbot**:
      - Copy the generated "Embedded Script" from the "Train" page.
      - Paste this script into the HTML `<body>` of the website where you want to embed the chatbot widget.

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
├── .env                        # (Optional) Backend environment variables file (API keys).
├── requirements.txt            # (Optional, but should be included) Backend dependencies.
├── README.md                   # This README file.
└── prompt-frontend/            # Frontend React/Next.js application directory
    ├── app/                    # Next.js app directory
    │   ├── playground/        # Playground page components
    │   │   ├── chat.jsx        # Chat screen component for playground
    │   │   └── page.jsx        # Playground main page component
    │   ├── train/           # Training page components
    │   │   └── page.js         # Training main page component
    │   └── layout.js           # Root layout for frontend app
    ├── components/             # Reusable UI components (likely using a UI library)
    │   └── ui/               # UI primitives and components (e.g., Card, Button, Input, etc.)
    │       ├── Navbar.jsx
    │       ├── button.jsx
    │       ├── card.jsx
    │       ├── input.jsx
    │       ├── label.jsx
    │       ├── separator.jsx
    │       └── textarea.jsx
    ├── public/                 # Public assets directory (e.g., images, fonts)
    ├── .env.local              # Frontend environment variables (API URL)
    ├── package.json            # npm package file, lists frontend dependencies and scripts
    └── package-lock.json       # npm lock file
```

## Dependencies

### Backend Dependencies

  - `fastapi`
  - `uvicorn`
  - `pydantic`
  - `langchain-chroma`
  - `langchain-openai`
  - `langchain-community`
  - `langchain-text-splitters`
  - `langchain-experimental`
  - `openai`
  - `requests`
  - `python-dotenv`
  - `uuid`
  - `starlette`
  - `pyngrok`
  - `crawl4ai`
  - `fitz` (PyMuPDF)
  - `lru-cache`
  - `logging`
  - ...

### Frontend Dependencies

  - `react`
  - `react-dom`
  - `next`
  - `lucide-react` (for icons - inferred from `<X />, <UploadCloud />, etc.` imports)
  - `@/components/ui/*` (Likely a UI component library like Radix UI, Shadcn UI, or similar - needs to be verified by checking `package.json` or project documentation if available)



## Contact
Team Chateaus
