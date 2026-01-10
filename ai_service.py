import os
import json
import requests
from bs4 import BeautifulSoup
from openai import OpenAI
from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_exception

AI_INTEGRATIONS_OPENAI_API_KEY = os.environ.get("AI_INTEGRATIONS_OPENAI_API_KEY")
AI_INTEGRATIONS_OPENAI_BASE_URL = os.environ.get("AI_INTEGRATIONS_OPENAI_BASE_URL")

openai = OpenAI(
    api_key=AI_INTEGRATIONS_OPENAI_API_KEY,
    base_url=AI_INTEGRATIONS_OPENAI_BASE_URL
)

def is_rate_limit_error(exception):
    error_msg = str(exception)
    return (
        "429" in error_msg
        or "RATELIMIT_EXCEEDED" in error_msg
        or "quota" in error_msg.lower()
        or "rate limit" in error_msg.lower()
        or (hasattr(exception, "status_code") and exception.status_code == 429)
    )


def fetch_article_content(url):
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        response = requests.get(url, headers=headers, timeout=15)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.text, 'html.parser')
        
        for script in soup(["script", "style", "nav", "footer", "aside"]):
            script.decompose()
        
        title = ""
        if soup.title:
            title = soup.title.string or ""
        elif soup.find('h1'):
            title = soup.find('h1').get_text(strip=True)
        
        article = soup.find('article') or soup.find('main') or soup.find('body')
        if article:
            paragraphs = article.find_all(['p', 'h1', 'h2', 'h3', 'h4', 'li'])
            content = '\n'.join([p.get_text(strip=True) for p in paragraphs if p.get_text(strip=True)])
        else:
            content = soup.get_text(separator='\n', strip=True)
        
        content = content[:15000]
        
        return {
            'title': title,
            'content': content,
            'url': url
        }
    except Exception as e:
        return {'error': str(e), 'url': url}


@retry(
    stop=stop_after_attempt(5),
    wait=wait_exponential(multiplier=1, min=2, max=60),
    retry=retry_if_exception(is_rate_limit_error),
    reraise=True
)
def generate_article_analysis(content, title):
    # the newest OpenAI model is "gpt-5" which was released August 7, 2025.
    # do not change this unless explicitly requested by the user
    response = openai.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "system",
                "content": """You are an expert educator who analyzes technical articles and creates learning materials using the Feynman Technique. 
                
Analyze the article and return a JSON object with the following structure:
{
    "title": "Article title",
    "summary": "A clear, comprehensive summary of the article (2-3 paragraphs)",
    "difficulty": "beginner" | "intermediate" | "advanced",
    "reading_time": <estimated minutes as integer>,
    "source": "Source/publication name if identifiable",
    "key_concepts": [
        {
            "name": "Concept name",
            "description": "Brief description",
            "complexity": "low" | "medium" | "high",
            "analogy": "A simple real-world analogy"
        }
    ],
    "eli5_explanations": [
        {
            "concept_name": "Concept name",
            "simple_explanation": "Explanation a 5-year-old could understand",
            "analogy": "A relatable everyday analogy",
            "real_world_example": "A concrete real-world example"
        }
    ],
    "quiz_questions": [
        {
            "question": "The question text",
            "type": "multiple_choice" | "true_false" | "open_ended",
            "options": ["Option A", "Option B", "Option C", "Option D"],
            "correct_answer": "The correct answer",
            "explanation": "Why this answer is correct",
            "difficulty": "easy" | "medium" | "hard"
        }
    ]
}

Generate 3-5 key concepts, 2-3 ELI5 explanations for the most complex concepts, and 5-7 quiz questions of varying difficulty."""
            },
            {
                "role": "user",
                "content": f"Analyze this article titled '{title}':\n\n{content}"
            }
        ],
        response_format={"type": "json_object"},
        max_tokens=4096
    )
    
    result = response.choices[0].message.content
    return json.loads(result)


@retry(
    stop=stop_after_attempt(5),
    wait=wait_exponential(multiplier=1, min=2, max=60),
    retry=retry_if_exception(is_rate_limit_error),
    reraise=True
)
def generate_feynman_feedback(user_explanation, concept_name, original_description):
    # Using gpt-4o-mini for efficient feedback generation
    response = openai.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "system",
                "content": """You are a supportive learning coach using the Feynman Technique. 
                
Evaluate the user's explanation of a concept and provide constructive feedback.

Return a JSON object:
{
    "understanding_score": <1-100>,
    "feedback": "Detailed constructive feedback",
    "gaps": ["List of knowledge gaps identified"],
    "suggestions": ["Specific suggestions to improve understanding"],
    "strengths": ["What they explained well"],
    "revised_explanation": "A model explanation they can learn from"
}"""
            },
            {
                "role": "user",
                "content": f"""The user is trying to explain the concept "{concept_name}".

Original concept description: {original_description}

User's explanation: {user_explanation}

Evaluate their understanding and provide feedback."""
            }
        ],
        response_format={"type": "json_object"},
        max_tokens=2048
    )
    
    result = response.choices[0].message.content
    return json.loads(result)
