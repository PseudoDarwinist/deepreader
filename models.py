from datetime import datetime
from app import db


class Article(db.Model):
    __tablename__ = 'articles'
    
    id = db.Column(db.Integer, primary_key=True)
    url = db.Column(db.String(2048), nullable=False)
    title = db.Column(db.String(500), nullable=False)
    source = db.Column(db.String(200))
    summary = db.Column(db.Text)
    reading_time = db.Column(db.Integer)
    difficulty = db.Column(db.String(50))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    concepts = db.relationship('Concept', backref='article', lazy=True, cascade='all, delete-orphan')
    quizzes = db.relationship('Quiz', backref='article', lazy=True, cascade='all, delete-orphan')
    eli5_explanations = db.relationship('Eli5Explanation', backref='article', lazy=True, cascade='all, delete-orphan')


class Concept(db.Model):
    __tablename__ = 'concepts'
    
    id = db.Column(db.Integer, primary_key=True)
    article_id = db.Column(db.Integer, db.ForeignKey('articles.id'), nullable=False)
    name = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    complexity = db.Column(db.String(50))
    analogy = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


class Eli5Explanation(db.Model):
    __tablename__ = 'eli5_explanations'
    
    id = db.Column(db.Integer, primary_key=True)
    article_id = db.Column(db.Integer, db.ForeignKey('articles.id'), nullable=False)
    concept_name = db.Column(db.String(200), nullable=False)
    simple_explanation = db.Column(db.Text)
    analogy = db.Column(db.Text)
    real_world_example = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


class Quiz(db.Model):
    __tablename__ = 'quizzes'
    
    id = db.Column(db.Integer, primary_key=True)
    article_id = db.Column(db.Integer, db.ForeignKey('articles.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    questions = db.relationship('QuizQuestion', backref='quiz', lazy=True, cascade='all, delete-orphan')


class QuizQuestion(db.Model):
    __tablename__ = 'quiz_questions'
    
    id = db.Column(db.Integer, primary_key=True)
    quiz_id = db.Column(db.Integer, db.ForeignKey('quizzes.id'), nullable=False)
    question = db.Column(db.Text, nullable=False)
    question_type = db.Column(db.String(50))
    correct_answer = db.Column(db.Text)
    options = db.Column(db.Text)
    explanation = db.Column(db.Text)
    difficulty = db.Column(db.String(50))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
