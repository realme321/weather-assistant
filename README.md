# 🌦️ Weather Assistant

A full-stack AI-powered weather assistant built using **Python, LangChain, LangGraph, Google Gemini, OpenWeather API, and Flask**.

The application understands natural-language weather queries and uses AI agent tool-calling to determine the user's location when required and fetch the corresponding weather information.

---

## 🚀 Features

- 🌤️ Get current weather information for any city
- 📍 Automatically detect the user's approximate location when no city is provided
- 🤖 AI-powered natural language interaction using Google Gemini
- 🔧 LangChain tools for weather and location retrieval
- 🔄 LangGraph-based agent workflow
- 💾 SQLite checkpointing for maintaining conversation state
- 🌐 Flask web interface
- 🔐 Environment variables used for API key management
- 📱 Simple and responsive chat interface

---

## 🛠️ Tech Stack

### Backend
- Python
- Flask
- LangChain
- LangGraph
- Google Gemini
- SQLite

### APIs
- OpenWeather API
- IPinfo API

### Frontend
- HTML
- CSS
- Jinja2

---

## 🏗️ Project Architecture

```text
User
  │
  ▼
Flask Web Application
  │
  ▼
LangChain / LangGraph Agent
  │
  ├── User provides city
  │       │
  │       ▼
  │   get_weather()
  │       │
  │       ▼
  │   OpenWeather API
  │
  └── User does not provide city
          │
          ▼
      get_location()
          │
          ▼
       IPinfo API
          │
          ▼
      get_weather()
          │
          ▼
    OpenWeather API
          │
          ▼
     Weather Response
