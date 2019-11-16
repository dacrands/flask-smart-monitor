import os
import unittest
import requests
from app import create_app, db
from app.models import User
from config import Config

basedir = os.path.abspath(os.path.dirname(__file__))

TEST_DB_PATH = 'sqlite:///' + os.path.join(basedir, 'test_app.db')


class TestConfig(Config):
    TESTING = True
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'secret-secrets-are-no-fun'
    SQLALCHEMY_DATABASE_URI = TEST_DB_PATH
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'secret-secrets-are-no-fun'
    STOCKS_API_KEY = os.environ.get('STOCKS_API_KEY') or 'nice-try'
    WEATHER_API_KEY = os.environ.get('WEATHER_API_KEY') or 'that-stinks'


class UserModelCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app(TestConfig)
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_password_hashing(self):
        user = User(username='dave')
        user.set_password('dog')
        self.assertFalse(user.check_password('cat'))
        self.assertTrue(user.check_password('dog'))

    def test_user_token(self):
        user = User(id=0)
        token = user.get_email_token()        
        valid_token = user.verify_email_token(token)
        invalid_token = user.verify_email_token("token")
        self.assertEqual(user.id, valid_token)
        self.assertEqual(None, invalid_token)


class TestMainRoutes(unittest.TestCase):
    def setUp(self):
        self.app = create_app(TestConfig)
        self.app_context = self.app.app_context()
        self.app_context.push()
        self.client = self.app.test_client()

    def tearDown(self):
        self.app_context.pop()

    def test_index_request(self):
        request = self.client.get('/')
        self.assertEqual(request.status_code, 302)

    def test_index_redirect(self):
        login_redirect_msg = b"<li>Please log in to access this page.</li>"
        request = self.client.get('/', follow_redirects=True)
        self.assertEqual(request.status_code, 200)
        assert login_redirect_msg in request.data

    def test_settings_redirect(self):
        request = self.client.get('/settings')
        self.assertEqual(request.status_code, 302)

    def test_settings_request(self):
        request = self.client.get('/settings', follow_redirects=True)
        self.assertEqual(request.status_code, 200)


class TestAPIRequests(unittest.TestCase):
    def setUp(self):
        self.app = create_app(TestConfig)
        self.app_context = self.app.app_context()
        self.app_context.push()

    def tearDown(self):
        self.app_context.pop()

    def test_stock_request(self):
        STOCKS_URL = "https://cloud.iexapis.com/v1/stock/market/batch?types=chart&symbols=aapl,goog,fb&token={0}".format(
            self.app.config['STOCKS_API_KEY'])
        stockRes = requests.get(STOCKS_URL)
        self.assertEqual(stockRes.status_code, 200)

    def test_weather_request(self):
        user = User(latitude=0, longitude=2)
        WEATHER_URL = "https://api.darksky.net/forecast/{0}/{1},{2}".format(
            self.app.config['WEATHER_API_KEY'], user.latitude, user.longitude)
        weatherRes = requests.get(WEATHER_URL)
        self.assertEqual(weatherRes.status_code, 200)


if __name__ == '__main__':
    unittest.main(verbosity=2)
