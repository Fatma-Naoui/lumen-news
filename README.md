# 📰 LumenNews AI

An intelligent news platform combining Retrieval-Augmented Generation (RAG), multi-agent fake news detection, semantic search, personalized recommendations, speech interaction, and explainable AI.

It leverages Large Language Models, vector databases, and multi-agent reasoning to deliver trustworthy and interactive news experiences.

# 🚀 Features

## 📰 News Aggregation
- RSS feed scraping from multiple sources
- Article extraction and cleaning
- Automatic summarization
- Translation (English → French, English → Arabic)

## 🤖 AI Chatbot (RAG)
A Retrieval-Augmented Generation system for querying news.

- Hybrid retrieval (BM25 + MiniLM embeddings)
- Source-grounded responses
- Multi-turn conversation memory
- Model: groq/llama-3.3-70b-versatile
- Speech-to-text: Whisper Large V3
- Text-to-speech: gTTS

## ⚖️ Multi-Agent Fake News Detection (CrewAI)

A debate-based verification system using adversarial reasoning.

### 🛡 Defender Agent
- Model: groq/llama-3.1-8b-instant
- Supports article credibility
- Retrieves supporting evidence via web search
- Builds factual arguments

### ⚔️ Opposer Agent
- Model: groq/llama-3.1-8b-instant
- Challenges credibility
- Finds contradictory evidence
- Detects misinformation and inconsistencies

### 👨‍⚖️ Judge Agent
- Model: groq/llama-3.3-70b-versatile
- Evaluates both agents
- Scores reasoning quality
- Produces final verdict

### 🌐 Web Search Tool
- Powered by Serper API
- Provides real-time Google results (titles, snippets, URLs)
- Grounds reasoning in external evidence

## 🔍 Semantic Search
- Model: sentence-transformers/all-MiniLM-L6-v2
- Stored using PostgreSQL + pgvector
- Used for:
  - Similar articles
  - RAG retrieval
  - Recommendation engine

## 📝 Summarization
- Model: facebook/bart-large-cnn
- Generates concise article summaries

## 🌍 Translation
- Helsinki-NLP/opus-mt-en-fr
- Helsinki-NLP/opus-mt-en-ar

## 😊 Sentiment Analysis
- Model: mrm8488/distilroberta-finetuned-financial-news-sentiment-analysis
- Stack: Hugging Face Transformers, spaCy, SHAP
- Outputs:
  - sentiment label
  - confidence score
  - SHAP feature importance

## 🎯 Recommendation Engine
A hybrid ranking system using:

- 50% semantic similarity
- 30% preferred domain match
- 10% recency
- 10% sentiment

User modeling:
- Uses stored embeddings or builds from reading history
- Article embeddings stored in pgvector
- Fallback embedding generation when missing

Mental state filtering:
- Filters low-sentiment content for stressed users

Limitation:
- Sentiment is not always stored → defaults to neutral (0.5)

# 🧠 System Architecture

RSS Feeds → Scraping → Cleaning → Summarization → Translation → Embedding (MiniLM) → PostgreSQL (pgvector)

Then:
- Chatbot (RAG)
- Recommendation Engine
- Fake News Debate System

# ⚖️ Multi-Agent Flow

Article → Defender Agent ↔ Opposer Agent → Web Search (Serper API) → Judge Agent → Final Verdict

# 🧪 Models & Libraries

LLMs:
- Llama 3.3 70B (Chatbot, Judge)
- Llama 3.1 8B (Agents)

NLP:
- MiniLM (Embeddings)
- BART CNN (Summarization)
- RoBERTa financial sentiment model
- Whisper Large V3 (Speech-to-text)
- Helsinki-NLP (Translation)

Frameworks:
- LangChain
- CrewAI
- Hugging Face Transformers
- SHAP
- spaCy

Infrastructure:
- Django / DRF
- PostgreSQL + pgvector

# 👩‍💻 Project Goal

LumenNews AI combines:
- RAG intelligence
- Multi-agent reasoning
- Semantic search
- Personalization
- Speech interaction
- Explainable AI

to build a trustworthy and interactive news ecosystem.
