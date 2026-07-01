import json
import unittest
from service import app
from service.models import db, Account

class TestAccountService(unittest.TestCase):

    def setUp(self):
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
        app.config['WTF_CSRF_ENABLED'] = False
        app.config['SERVER_NAME'] = 'localhost'
        self.app = app.test_client()
        with app.app_context():
            db.create_all()

    def tearDown(self):
        with app.app_context():
            db.session.remove()
            db.drop_all()

    def _create_account(self, name="John Doe"):
        data = {"name": name, "email": "john@example.com", "address": "123 Main St", "phone_number": "555-1234"}
        return self.app.post('/accounts', json=data, content_type='application/json')

    def test_health(self):
        resp = self.app.get('/health')
        self.assertEqual(resp.status_code, 200)
        data = json.loads(resp.data)
        self.assertEqual(data['status'], 'OK')

    def test_index(self):
        resp = self.app.get('/')
        self.assertEqual(resp.status_code, 200)

    def test_create_account(self):
        resp = self._create_account()
        self.assertEqual(resp.status_code, 201)
        data = json.loads(resp.data)
        self.assertEqual(data['name'], 'John Doe')

    def test_create_account_no_data(self):
        resp = self.app.post('/accounts', json={}, content_type='application/json')
        self.assertEqual(resp.status_code, 400)

    def test_create_account_no_name(self):
        resp = self.app.post('/accounts', json={"email": "test@test.com"}, content_type='application/json')
        self.assertEqual(resp.status_code, 400)

    def test_list_accounts(self):
        self._create_account("Alice")
        self._create_account("Bob")
        resp = self.app.get('/accounts')
        self.assertEqual(resp.status_code, 200)
        data = json.loads(resp.data)
        self.assertEqual(len(data), 2)

    def test_list_accounts_empty(self):
        resp = self.app.get('/accounts')
        self.assertEqual(resp.status_code, 200)
        data = json.loads(resp.data)
        self.assertEqual(len(data), 0)

    def test_get_account(self):
        resp = self._create_account("Alice")
        data = json.loads(resp.data)
        account_id = data['id']
        resp = self.app.get(f'/accounts/{account_id}')
        self.assertEqual(resp.status_code, 200)
        data = json.loads(resp.data)
        self.assertEqual(data['name'], 'Alice')

    def test_get_account_not_found(self):
        resp = self.app.get('/accounts/999')
        self.assertEqual(resp.status_code, 404)

    def test_update_account(self):
        resp = self._create_account("Alice")
        data = json.loads(resp.data)
        account_id = data['id']
        resp = self.app.put(f'/accounts/{account_id}', json={"name": "Alice Updated"}, content_type='application/json')
        self.assertEqual(resp.status_code, 200)
        data = json.loads(resp.data)
        self.assertEqual(data['name'], 'Alice Updated')

    def test_update_account_not_found(self):
        resp = self.app.put('/accounts/999', json={"name": "No One"}, content_type='application/json')
        self.assertEqual(resp.status_code, 404)

    def test_delete_account(self):
        resp = self._create_account("Alice")
        data = json.loads(resp.data)
        account_id = data['id']
        resp = self.app.delete(f'/accounts/{account_id}')
        self.assertEqual(resp.status_code, 204)

    def test_delete_account_not_found(self):
        resp = self.app.delete('/accounts/999')
        self.assertEqual(resp.status_code, 404)

    def test_data_contains_10_accounts(self):
        for i in range(10):
            self._create_account(f"User {i}")
        resp = self.app.get('/accounts')
        data = json.loads(resp.data)
        self.assertEqual(len(data), 10)

    def test_content_type_equals_json(self):
        resp = self.app.get('/accounts')
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.content_type, 'application/json')

    def test_it_should_return_a_cors_header(self):
        resp = self.app.get('/accounts')
        self.assertEqual(resp.status_code, 200)
        self.assertIn('Access-Control-Allow-Origin', resp.headers)
        self.assertEqual(resp.headers.get('Access-Control-Allow-Origin'), '*')

    def test_it_should_return_security_headers(self):
        resp = self.app.get('/accounts')
        self.assertEqual(resp.status_code, 200)
        self.assertIn('X-Content-Type-Options', resp.headers)
        self.assertEqual(resp.headers.get('X-Content-Type-Options'), 'nosniff')
