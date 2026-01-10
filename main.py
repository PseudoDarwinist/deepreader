from flask import send_from_directory
from app import create_app, db
from routes import register_routes

app = create_app()


@app.route('/')
def serve_index():
    return send_from_directory('.', 'index.html')


@app.after_request
def add_header(response):
    response.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate'
    response.headers['Pragma'] = 'no-cache'
    response.headers['Expires'] = '0'
    return response


with app.app_context():
    from models import Article, Concept, Eli5Explanation, Quiz, QuizQuestion
    db.create_all()

register_routes(app)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
