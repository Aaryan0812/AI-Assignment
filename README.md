🚀 AI Agentic Pipeline using LangGraph, LangChain, Qdrant & Streamlit

This project demonstrates a complete agentic AI pipeline that uses LangGraph, LangChain, Qdrant, RAG, LLM evaluation, and a Streamlit UI.
It performs two main tasks:

Fetch real-time weather data using the OpenWeatherMap API

Answer questions from a PDF document using Retrieval-Augmented Generation (RAG)

The pipeline intelligently routes user queries using a LangGraph decision node.

📌 Features
✅ 1. Agentic Workflow using LangGraph

The system uses LangGraph to orchestrate decision-making and API calls:

A router node determines whether a query is weather-related or PDF-related.

Weather queries call the OpenWeatherMap API.

PDF queries trigger RAG retrieval and summarization.

✅ 2. Weather Data Fetching

Real-time weather information is obtained via OpenWeatherMap API.

Handles temperature, humidity, wind, conditions, etc.

✅ 3. PDF Question-Answering via RAG

The system extracts text from the PDF.

Generates embeddings using an embedding model.

Stores them in Qdrant Vector DB.

Retrieves top relevant chunks for answering queries.

✅ 4. LLM-Powered Processing (LangChain)

LangChain handles:

Prompt templates

LLM invocation

Summarization

Response generation

✅ 5. LangSmith Evaluation

All LLM calls are logged and evaluated using LangSmith.

Useful for debugging, traceability, and performance metrics.

✅ 6. Streamlit Chat UI

A clean chat interface allows:

Uploading PDF

Asking questions

Viewing real-time responses

Observing RAG retrieval behavior

✅ 7. Comprehensive Test Cases

Modular test suite covering:

Weather API handlers

PDF ingestion and chunking

Embedding generation

Vector DB retrieval logic

LLM pipeline correctness

🧱 Architecture Overview
           ┌────────────────────────────┐
           │         Streamlit UI        │
           └──────────────┬─────────────┘
                          ▼
                ┌──────────────────┐
                │    LangGraph      │
                │   (Routing Node)  │
                └──────┬───────────┘
  ┌─────────────────────┼─────────────────────┐
  ▼                     ▼                     ▼
Weather API Node   PDF-RAG Node        Error Handler
(OpenWeatherMap)   (Qdrant, LLM)
  │                     │
  ▼                     ▼
Processed Weather   LLM-Enhanced Answers
Summary             from PDF Content

📁 Project Structure
📦 project/
├── src/
│   ├── graph/
│   │   ├── router.py
│   │   ├── weather_node.py
│   │   ├── rag_node.py
│   │   └── graph_builder.py
│   ├── llm/
│   │   ├── prompts.py
│   │   ├── llm_client.py
│   ├── rag/
│   │   ├── pdf_loader.py
│   │   ├── embeddings.py
│   │   ├── vector_store.py
│   └── tests/
│       ├── test_weather.py
│       ├── test_rag.py
│       ├── test_llm.py
├── app.py (Streamlit)
├── README.md
├── requirements.txt
└── .env

⚙️ Installation
1️⃣ Clone Repo
git clone <repo-url>
cd project

2️⃣ Install Dependencies
pip install -r requirements.txt

3️⃣ Environment Variables (.env)
OPENWEATHER_API_KEY=your_key
QDRANT_URL=http://localhost:6333
LANGCHAIN_API_KEY=your_key

4️⃣ Run Streamlit App
streamlit run app.py

🧪 Running Tests
pytest -v


Tests cover:

Weather API logic

RAG retrieval

Embedding pipeline

LLM correctness

🎯 Usage Guide

Start the Streamlit UI

Upload a PDF file

Ask any question:

“What is the summary of section 3?”

“What is the weather in London?”

LangGraph will route internally:

Weather → API

PDF → RAG

Answer will appear in the chat interface

🔮 Future Enhancements

Add multi-PDF RAG

Add chat memory and conversation logs

Support multiple external API tools

Add agent retrievers with tool reasoning traces

🏁 Conclusion

This project showcases a full agentic AI application using LangGraph, LangChain, Qdrant, and LangSmith — wrapped in a simple Streamlit UI.

Perfect for demonstrating:

Tool calling

RAG

Routing logic

LLM evaluation

Real-time API integration