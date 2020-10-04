import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from flaskr import create_app
from models import setup_db, Question, Category


class TriviaTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_path = "postgresql://postgres:password@localhost:5432/trivia_test"
        setup_db(self.app, self.database_path)

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()
    
    def tearDown(self):
        """Executed after reach test"""
        pass

    """
    TODO
    Write at least one test for each test for successful operation and for expected errors.
    """
    def test_get_categories(self):
        res = self.client().get('/categories')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertIsNotNone(data['categories'])
        

    def test_get_categories_error(self):
        res = self.client().get('/categories/100')
        data = json.loads(res.data)
        self.assertEqual(data['success'], False)
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['message'], 'resource not found')
    
    def test_get_questions(self):
        res = self.client().get('/questions')
        data = json.loads(res.data)
        self.assertEqual(data['success'], True)
        self.assertEqual(res.status_code, 200)
        self.assertIsNotNone(data['questions'])
        self.assertIsNotNone(data['total_questions'])
        self.assertIsNotNone(data['categories'])

    def test_get_questions_error(self):
        res = self.client().get('/questions?page=100')
        data = json.loads(res.data)
        self.assertEqual(data['success'], False)
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['message'], 'resource not found')

    def test_delete_question(self):
        question = Question(question='example question', answer='example answer', difficulty=1, category=1)
        question.insert()
        id = question.id
        res = self.client().delete(f'/questions/{id}')
        data = json.loads(res.data)
        question = Question.query.filter(Question.id == question.id).one_or_none()
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['deleted'], id)
        self.assertEqual(question, None)

    def test_delete_question_error(self):
        res = self.client().delete('/questions/100')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'resource not found')

    def test_new_question(self):
        question = {
            'question': 'example question',
            'answer': 'example  answer',
            'difficulty': 1,
            'category': 1
        }
        res = self.client().post('/questions', json=question)
        last_entry = Question.query.order_by(-Question.id).first()
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertEqual(last_entry.id,data['created'])

    def test_new_question_error(self):
        question = {
            'question': 'example question',
            'answer': 'example answer',
            'category': "example false category"
        }
        res = self.client().post('/questions', json=question)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 422)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "unprocessable entity")

    
    def test_search_questions(self):
        example_search_term = {'searchTerm': 'america'}
        res = self.client().post('/questions/search', json=example_search_term)
        data = json.loads(res.data)
        self.assertIsNotNone(data['questions'])
        self.assertIsNotNone(data['total_questions'])
        self.assertEqual(data['success'], True)
        self.assertEqual(res.status_code, 200)
        
        

    def test_search_questions_error(self):
        example_search_term = {'searchTerm': None}
        res = self.client().post('/questions/search', json=example_search_term)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data["message"], "resource not found")
        self.assertEqual(data["success"], False)

    def test_get_questions_per_category(self):
        res = self.client().get('/categories/3/questions')
        data = json.loads(res.data)
        self.assertIsNotNone(data['current_category'])
        self.assertIsNotNone(data['questions'])
        self.assertIsNotNone(data['total_questions'])
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_get_questions_per_category_error(self):
        res = self.client().get('/categories/false_entry/questions')
        data = json.loads(res.data)
        self.assertEqual(data["success"], False)
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data["message"], "resource not found")

    def test_play_quiz(self):
        quiz_details = {'quiz_category': {'type': 'Science', 'id': 1},'previous_questions': []}
        res = self.client().post('/quizzes', json=quiz_details)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_404_play_quiz(self):
        quiz_details = {'previous_questions': []}
        res = self.client().post('/quizzes', json=quiz_details)
        data = json.loads(res.data)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "unprocessable entity")
        self.assertEqual(res.status_code, 422)
        
        
        
        
    


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()