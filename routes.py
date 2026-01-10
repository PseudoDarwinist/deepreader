import json
from flask import request, jsonify
from app import db
from models import Article, Concept, Eli5Explanation, Quiz, QuizQuestion
from ai_service import fetch_article_content, generate_article_analysis, generate_feynman_feedback


def register_routes(app):
    @app.route('/api/analyze', methods=['POST'])
    def analyze_article():
        data = request.get_json()
        url = data.get('url')
        
        if not url:
            return jsonify({'error': 'URL is required'}), 400
        
        existing = Article.query.filter_by(url=url).first()
        if existing:
            return jsonify(format_article_response(existing))
        
        article_data = fetch_article_content(url)
        if 'error' in article_data:
            return jsonify({'error': f"Failed to fetch article: {article_data['error']}"}), 400
        
        try:
            analysis = generate_article_analysis(article_data['content'], article_data['title'])
        except Exception as e:
            return jsonify({'error': f'AI analysis failed: {str(e)}'}), 500
        
        article = Article(
            url=url,
            title=analysis.get('title', article_data['title']),
            source=analysis.get('source', ''),
            summary=analysis.get('summary', ''),
            reading_time=analysis.get('reading_time', 5),
            difficulty=analysis.get('difficulty', 'intermediate')
        )
        db.session.add(article)
        db.session.flush()
        
        for concept_data in analysis.get('key_concepts', []):
            concept = Concept(
                article_id=article.id,
                name=concept_data.get('name', ''),
                description=concept_data.get('description', ''),
                complexity=concept_data.get('complexity', 'medium'),
                analogy=concept_data.get('analogy', '')
            )
            db.session.add(concept)
        
        for eli5_data in analysis.get('eli5_explanations', []):
            eli5 = Eli5Explanation(
                article_id=article.id,
                concept_name=eli5_data.get('concept_name', ''),
                simple_explanation=eli5_data.get('simple_explanation', ''),
                analogy=eli5_data.get('analogy', ''),
                real_world_example=eli5_data.get('real_world_example', '')
            )
            db.session.add(eli5)
        
        quiz = Quiz(article_id=article.id)
        db.session.add(quiz)
        db.session.flush()
        
        for q_data in analysis.get('quiz_questions', []):
            question = QuizQuestion(
                quiz_id=quiz.id,
                question=q_data.get('question', ''),
                question_type=q_data.get('type', 'multiple_choice'),
                correct_answer=q_data.get('correct_answer', ''),
                options=json.dumps(q_data.get('options', [])),
                explanation=q_data.get('explanation', ''),
                difficulty=q_data.get('difficulty', 'medium')
            )
            db.session.add(question)
        
        db.session.commit()
        
        return jsonify(format_article_response(article))

    @app.route('/api/articles/<int:article_id>', methods=['GET'])
    def get_article(article_id):
        article = Article.query.get_or_404(article_id)
        return jsonify(format_article_response(article))

    @app.route('/api/articles', methods=['GET'])
    def list_articles():
        articles = Article.query.order_by(Article.created_at.desc()).limit(20).all()
        return jsonify([{
            'id': a.id,
            'title': a.title,
            'url': a.url,
            'difficulty': a.difficulty,
            'reading_time': a.reading_time,
            'created_at': a.created_at.isoformat() if a.created_at else None
        } for a in articles])

    @app.route('/api/feynman-feedback', methods=['POST'])
    def get_feynman_feedback():
        data = request.get_json()
        user_explanation = data.get('explanation')
        concept_name = data.get('concept_name')
        original_description = data.get('original_description', '')
        
        if not user_explanation or not concept_name:
            return jsonify({'error': 'explanation and concept_name are required'}), 400
        
        try:
            feedback = generate_feynman_feedback(user_explanation, concept_name, original_description)
            return jsonify(feedback)
        except Exception as e:
            return jsonify({'error': f'Feedback generation failed: {str(e)}'}), 500


def format_article_response(article):
    concepts = [{
        'id': c.id,
        'name': c.name,
        'description': c.description,
        'complexity': c.complexity,
        'analogy': c.analogy
    } for c in article.concepts]
    
    eli5_explanations = [{
        'id': e.id,
        'concept_name': e.concept_name,
        'simple_explanation': e.simple_explanation,
        'analogy': e.analogy,
        'real_world_example': e.real_world_example
    } for e in article.eli5_explanations]
    
    quizzes = []
    for quiz in article.quizzes:
        questions = [{
            'id': q.id,
            'question': q.question,
            'type': q.question_type,
            'options': json.loads(q.options) if q.options else [],
            'correct_answer': q.correct_answer,
            'explanation': q.explanation,
            'difficulty': q.difficulty
        } for q in quiz.questions]
        quizzes.append({
            'id': quiz.id,
            'questions': questions
        })
    
    return {
        'id': article.id,
        'url': article.url,
        'title': article.title,
        'source': article.source,
        'summary': article.summary,
        'reading_time': article.reading_time,
        'difficulty': article.difficulty,
        'concepts': concepts,
        'eli5_explanations': eli5_explanations,
        'quizzes': quizzes,
        'created_at': article.created_at.isoformat() if article.created_at else None
    }
