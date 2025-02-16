# 🚀 Prompt:  Unleash the Power of AI Chatbots on *Any* Website - No Code Required! 🤖

**Tired of complex chatbot integrations?**  ✨ **Prompt** ✨ revolutionizes website interaction by offering a **lightning-fast, no-code solution** to create intelligent, website-aware chatbots.  Imagine deploying a cutting-edge AI assistant on *any* website in minutes, simply by providing a URL!  This project delivers a powerful REST API built with FastAPI, seamlessly integrated with a user-friendly frontend, to empower anyone to harness the magic of Large Language Models (LLMs) and vector databases.

**Stop coding, start conversing! Welcome to the future of website engagement.**

## 🔥 Key Features - Prepare to be Amazed! 🔥

*   **Instant Bot Creation - Website to Chatbot in a Click!**:
    *   **Website Crawling Wizardry**:  Simply provide a website URL, and our intelligent system *automagically* crawls, extracts, and transforms website content into a fully functional chatbot brain! 🧠
    *   **Document Power-Up**:  Supercharge your bot with local knowledge! Upload PDFs and TXT files to infuse specific documents and expertise into your chatbot's capabilities. 📚
    *   **Hybrid Training Mastery**: Unleash the ultimate knowledge fusion! Combine website crawling and document uploads for truly comprehensive and deeply informed chatbots. 🚀

*   **Mind-Reading Intelligent Querying - Answers that Wow!**:
    *   **Natural Language Ninja**:  Users ask questions in plain English, and **Prompt** understands!  No more rigid command structures – just natural, intuitive conversation. 🗣️
    *   **Context-Aware Genius**:  Powered by advanced LLMs and vector databases, our chatbots deliver laser-focused, contextually relevant answers, drawing directly from the learned website and document data. 💡

*   **Under the Hood Magic - Cutting-Edge Tech, Zero Complexity**:
    *   **Vector Database Velocity**:  ChromaDB ensures blazing-fast information retrieval, powering instant and accurate query responses. ⚡
    *   **Web Crawling Prowess**:  `crawl4ai` tackles even the most intricate website structures, extracting valuable text content with unmatched robustness. 🕸️
    *   **OpenAI Brainpower**:  Fueled by OpenAI's state-of-the-art models (like `gpt-4o`!), **Prompt** generates insightful, human-like answers that will leave users impressed. ✨

*   **Frontend Playground - Design Your Dream Chatbot in Real-Time!**:
    *   **Visual Customization Paradise**:  Shape the perfect chatbot widget with our intuitive, real-time customization panel! Tweak everything from colors and messages to branding and appearance – all with live preview! 🎨
        *   **Brand it Boldly**: Chatbot Name, Display Name, Profile Image – make it yours!
        *   **Craft Compelling Conversations**: Welcome messages, placeholder text, header text, assistant prompts – design the perfect conversational flow.
        *   **Unleash Your Inner Designer**: AI & User message backgrounds, accent colors, icon styles –  make your chatbot visually stunning!
    *   **Chat Preview Sandbox**:  Test drive your chatbot creations instantly! Interact with a live preview directly within the playground environment. 🕹️
    *   **Embeddable Magic Script**:  Generate a single line of JavaScript code to effortlessly embed your customized chatbot onto *any* website. 🪄  **Deployment is now literally copy-paste simple!**

*   **Developer-Friendly API - Power and Flexibility for the Tech-Savvy**:
    *   **REST API Mastery**:  Clean, well-documented API endpoints (`/create_bot/`, `/query_bot/`) for seamless integration and programmatic chatbot management. 💻
    *   **CORS Enabled**:  Effortless cross-origin communication – use your chatbot anywhere on the web without restriction. 🌐

*   **Performance & Efficiency Built-In**:
    *   **Caching Champions**: `lru_cache` optimizes vector database access, ensuring lightning-fast response times even for heavily used chatbots. 🚀
    *   **Robust Logging**: Comprehensive logging provides deep insights for debugging and monitoring, ensuring smooth operation. 📊

## ✨ Innovation Highlights - Why Prompt is a Game-Changer! ✨

*   **No-Code Chatbot Creation**: Democratizes AI! Anyone, regardless of coding expertise, can build and deploy intelligent website assistants.
*   **Rapid Deployment**:  Go from zero to chatbot in *minutes*.  Train, customize, and embed with unparalleled speed.
*   **Visually Stunning Customization**:  Create chatbots that perfectly match your brand and website aesthetic with real-time visual feedback.
*   **Universal Website Compatibility**:  Embed your chatbot on *any* website with a single line of code.
*   **Combines Web Crawling & Document Learning**:  Offers unparalleled flexibility in training data sources for truly comprehensive chatbot knowledge.

## 🛠️ Installation - Get Started in Minutes! 🛠️

### Prerequisites

*   **Python 3.8+**
*   **pip** (Python package installer)
*   **Node.js and npm** (for Frontend - if you want to experience the visual playground!)
*   **OpenAI API Key**:  Unlock the power of LLMs! [Get your API key here](https://platform.openai.com/api-keys).
*   **Ngrok Account** (Optional): Share your chatbot API with the world instantly! [Sign up for Ngrok](https://ngrok.com/).

### Backend Setup Steps

1.  **Clone the repository:**

    ```bash
    git clone https://github.com/visha1Sagar/The-Chateaus_Prompt.git
    cd The-Chateaus_Prompt
    ```

2.  **Set up your virtual environment:**

    ```bash
    python -m venv venv
    source venv/bin/activate  # Linux/macOS
    venv\Scripts\activate  # Windows
    ```

3.  **Install backend dependencies:**

    ```bash
    pip install -r requirements.txt
    ```

4.  **Configure your OpenAI API Key:**

    *   Create a `.env` file in the project root.
    *   Add your API key:
        ```env
        OPENAI_API_KEY=your_openai_api_key_here
        ```

### Frontend Setup Steps - Unleash the Playground!

1.  **Navigate to the frontend:**

    ```bash
    cd prompt-frontend
    ```

2.  **Install frontend dependencies:**

    ```bash
    npm install # or yarn install
    ```

3.  **Set the backend API URL:**

    *   Create `.env.local` in `prompt-frontend`.
    *   Point to your backend:
        ```env
        NEXT_PUBLIC_BACKEND_URL=http://localhost:8000  # Local backend OR your Ngrok URL!
        ```

4.  **Launch the frontend!**

    ```bash
    npm run dev # or yarn dev
    ```

5.  **Access the Playground at `http://localhost:3000`!**

## 🚀 Usage - From Zero to Chatbot Hero! 🚀

### Running the API and Frontend - Double the Power!

1.  **Backend Blast-Off:** Start your API (see "Running the API" in the full README).
2.  **Frontend Ignition:** Launch the frontend dev server (see "Frontend Setup Steps").
3.  **Playground Access:** Open your browser to `http://localhost:3000` and enter the **Prompt Playground!**
4.  **Train Like a Pro**:
    *   "Train" page -> "Website Link and File Upload".
    *   Enter website URL, upload files.
    *   "Save" -  and BOOM! Chatbot brain is online! Get your embed script & bot ID.
5.  **Customize & Conquer**:
    *   "Playground" page - unleash your creativity!
    *   Tweak settings, preview live, perfect your chatbot's look and feel.
6.  **Embed & Engage**:
    *   "Train" page -> Copy "Embedded Script".
    *   Paste into your website's `<body>`.  **Done!** Your AI assistant is live!

## 🛠️ Tech Stack ⚙️

**Prompt** leverages a modern and robust technology stack for both backend API and frontend interface:

### Backend

*   **Framework**: **FastAPI** - A high-performance Python framework for building APIs, known for its speed and ease of use.
*   **Language**: **Python 3.8+** -  A versatile and widely-used language ideal for AI and backend development.
*   **LLM Integration**: **OpenAI API** - Utilizing powerful models like `gpt-4o` to generate intelligent and contextually relevant chatbot responses.
*   **Vector Database**: **ChromaDB** - An embedded vector database for efficient storage and similarity search of document embeddings.
*   **Web Crawling**: **crawl4ai** - A dedicated web crawling library designed for robust and effective website data extraction.
*   **Document Processing**: **PyMuPDF (fitz)** -  For efficient loading and text extraction from PDF documents.
*   **Caching**: **lru-cache** -  For in-memory caching to enhance performance and reduce latency.
*   **API Tools**:
    *   **Uvicorn** - ASGI server to run the FastAPI application.
    *   **Pydantic** - For data validation and settings management.
    *   **Requests** - For making HTTP requests.
    *   **Starlette** -  Underlying framework for FastAPI, providing core ASGI functionality.
    *   **Python-dotenv** -  For managing environment variables securely.
    *   **UUID** - For generating unique identifiers.
    *   **Pyngrok** -  (Optional) For quickly exposing the API via Ngrok tunnels.
    *   **Logging** - Python's built-in logging library for application monitoring and debugging.

### Frontend

*   **Framework**: **Next.js** - A React framework for building user interfaces, known for performance and developer experience.
*   **Language**: **JavaScript (ES6+)** / **JSX** - Modern JavaScript and JSX syntax for building dynamic UI components.
*   **UI Components**:  **Custom React Components & UI Library** -  Utilizing reusable UI components (likely from a library like Radix UI, Shadcn UI - needs verification) for a polished and consistent design. Includes components like: `Card`, `Button`, `Input`, `Textarea`, `Label`, `Separator`.
*   **Icons**: **lucide-react** -  For a consistent and beautiful icon set.
*   **Styling**: **CSS Modules / Global CSS** -  For styling components and the overall application.
*   **Environment Variables**: **dotenv (via Next.js)** -  For managing frontend environment configuration.

## 🤝 Contributing - Join the Prompt Revolution! 🤝

Contributions are eagerly welcomed!  Help us make **Prompt** even more amazing.  Pull requests, feature suggestions, bug reports – all are highly appreciated!  Let's build the future of no-code chatbots together!

## 📞 Contact

**Team Chateaus** - Let's Chat! 💬
