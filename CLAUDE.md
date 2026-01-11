# DEEP READER

---

## MANDATORY: Intentional Compaction Protocol

**CLAUDE: You MUST read this section and follow it religiously.**

After completing ANY feature, bug fix, or significant change, perform **Intentional Compaction** by updating `ADR.md` (Architectural Decision Records):

### What to Document

For every change, capture:

1. **The Fork in the Road** - What alternatives existed? What parallel paths were available?
2. **Why This Path** - Why did you choose this approach over others? What trade-offs were accepted?
3. **How It Works** - Technical implementation details that aren't obvious from code alone
4. **The Thinking** - Your reasoning process, assumptions made, constraints considered
5. **What Was Rejected** - Approaches explicitly NOT taken and why
6. **Future Considerations** - What might need to change if requirements evolve

### When to Update

- After completing a feature
- After fixing a non-trivial bug
- After refactoring or changing existing behavior
- Before ending a conversation where significant work was done

### Format

```markdown
## [Feature/Change Name] - YYYY-MM-DD

### Context & Problem
Why was this needed?

### Decision
What approach was chosen?

### Alternatives Considered
| Option | Pros | Cons | Why Rejected |
|--------|------|------|--------------|

### Implementation Notes
How does it work technically?

### Trade-offs Accepted
What compromises were made?

### Change History
- [Date]: Initial implementation
- [Date]: Modified because...
```

**This is not optional. The "why" behind code is more valuable than the code itself. Future engineers (and future Claude sessions) depend on this context.**

---

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
