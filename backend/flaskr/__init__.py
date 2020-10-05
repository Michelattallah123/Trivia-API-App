import os
from flask import Flask, request, abort, jsonify, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random

from models import setup_db, Question, Category

QUESTIONS_PER_PAGE = 10


def paginate_questions(request, selection):
    page = request.args.get('page', 1, type=int)
    start = (page - 1) * QUESTIONS_PER_PAGE
    end = start + QUESTIONS_PER_PAGE

    questions = [question.format() for question in selection]
    current_questions = questions[start:end]

    return current_questions


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    setup_db(app)
    '''
  
  '''
    cors = CORS(app, resources={r"/api/*": {"origins": "*"}})
    '''
  
  '''
    @app.after_request
    def after_request(response):
        response.headers.add(
            'Access-Control-Allow-Headers',
            'Content-Type, Authorization')
        response.headers.add(
            'Access-Control-Allow-Methods',
            'GET, POST, PATCH, DELETE, OPTIONS')
        return response
    '''
  
  '''
    @app.route('/categories')
    def retrieve_categories():
        categories = Category.query.order_by(Category.id).all()
        if categories is None:
            abort(404)
        return jsonify({'success': True, 'categories': {
                       category.id: category.type for category in categories}})

    '''
  
  '''
    @app.route('/questions', methods=['GET'])
    def retrieve_questions():
        questions = Question.query.order_by(Question.id).all()
        categories = Category.query.order_by(Category.id).all()
        current_questions = paginate_questions(request, questions)
        print(current_questions)
        if len(current_questions) == 0:
            abort(404)
        return jsonify({
            'success': True,
            'questions': current_questions,
            'total_questions': len(questions),
            'categories': {category.id: category.type for category in categories},
            'current_category': [question['category'] for question in current_questions]
        })
    '''
  
  '''
    @app.route('/questions/<int:question_id>', methods=['DELETE'])
    def delete_question(question_id):
        question = Question.query.filter(
            Question.id == question_id).one_or_none()
        categories = Category.query.order_by(Category.id).all()
        if question is None:
            abort(404)
        try:
            question.delete()
            questions = Question.query.order_by(Question.id).all()
            current_questions = paginate_questions(request, questions)

            return jsonify({
                'success': True,
                'questions': current_questions,
                'total_questions': len(Question.query.all()),
                'categories': [category.type for category in categories],
                'deleted': question.id
            })
        except BaseException:
            error(422)

    '''
  
  '''
    @app.route('/questions', methods=['POST'])
    def create_question():
        body = request.get_json()
        question = body.get('question', None)
        answer = body.get('answer', None)
        category = body.get('category', None)
        difficulty = body.get('difficulty', None)

        try:
            new_question = Question(
                question=question,
                answer=answer,
                category=category,
                difficulty=difficulty)
            new_question.insert()

            return jsonify({
                'success': True,
                'created': new_question.id
            })

        except BaseException:
            abort(422)

    '''
  
  '''
    @app.route('/questions/search', methods=['POST'])
    def search_questions():
        body = request.get_json()
        search_term = body.get('searchTerm', None)
        if search_term is not None:
            try:

                questions = Question.query.filter(
                    Question.question.ilike(
                        '%' + search_term + '%')).all()
                current_questions = paginate_questions(request, questions)
                categories = Category.query.order_by(Category.id).all()

                return jsonify({
                    'success': True,
                    'questions': current_questions,
                    'total_questions': len(questions),
                })
            except BaseException:
                abort(404)
        else:
            abort(404)

    '''
  
  '''
    @app.route('/categories/<int:id>/questions')
    def filter_by_category(id):
        try:
            questions = Question.query.filter(
                Question.category == str(id)).all()
            current_questions = paginate_questions(request, questions)

            return jsonify({
                'success': True,
                'questions': current_questions,
                'total_questions': len(current_questions),
                'current_category': id
            })
        except BaseException:
            abort(404)

    '''
  
  '''
    @app.route('/quizzes', methods=['POST'])
    def play_quiz():
        try:
            body = request.get_json()
            previous_questions = body.get('previous_questions', None)
            quiz_category = body.get('quiz_category', None)
            if int(quiz_category['id']) == 0:
                questions = Question.query.filter(
                    Question.id.notin_(previous_questions)).all()
            else:
                questions = Question.query.filter(
                    Question.category == quiz_category['id']).filter(
                    Question.id.notin_(previous_questions)).all()
            if len(questions) == 0:
                current_question = None
            else:
                current_question = random.choice(questions).format()

            return jsonify({
                'success': True,
                'question': current_question
            })
        except BaseException:
            abort(422)
    '''
  
  '''
    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            "success": False,
            "error": 404,
            "message": "resource not found"
        }), 404

    @app.errorhandler(422)
    def unprocessable_entity(error):
        return jsonify({
            "success": False,
            "error": 422,
            "message": "unprocessable entity"
        }), 422

    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({
            "success": False,
            "error": 400,
            "message": "bad request"
        }), 400

    @app.errorhandler(500)
    def internal_server_error(error):
        return jsonify({
            "success": False,
            "error": 500,
            "message": "internal_server_error"
        }), 500

    return app
