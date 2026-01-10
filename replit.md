# DEEP READER

## Overview
A full-stack web application that transforms technical articles into deep learning experiences using the Feynman Technique. The app uses AI to analyze articles, extract key concepts, generate simple explanations, and create quizzes to test understanding.

## Project Structure
- `main.py` - Main Flask application entry point
- `app.py` - Flask app factory and database configuration
- `models.py` - SQLAlchemy database models (Article, Concept, Quiz, etc.)
- `routes.py` - API endpoints for article analysis, quizzes, and feedback
- `ai_service.py` - OpenAI integration for content analysis and generation
- `index.html` - Frontend single-page application

## Tech Stack
- **Backend**: Python/Flask with SQLAlchemy ORM
- **Database**: PostgreSQL
- **AI**: OpenAI GPT (via Replit AI Integrations)
- **Frontend**: Vanilla JavaScript SPA

## Features
- Fetch and analyze any web article URL
- AI-powered extraction of key concepts
- ELI5 (Explain Like I'm 5) explanations
- Interactive quizzes to test understanding  
- Feynman Technique teaching feedback

## API Endpoints
- `POST /api/analyze` - Analyze a URL and generate learning content
- `GET /api/articles` - List all analyzed articles
- `GET /api/articles/<id>` - Get specific article details
- `POST /api/feynman-feedback` - Get AI feedback on user explanations

## Running the App
Development server:
```bash
python main.py
```

## Deployment
Configured for Gunicorn WSGI server:
```bash
gunicorn --bind=0.0.0.0:5000 --reuse-port main:app
```
