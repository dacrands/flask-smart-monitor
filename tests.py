import unittest
from app import app, db
from app.models import User

class UserModelCase(unittest.TestCase):
  def setUp(self):
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite://'
        db.create_all()

  def tearDown(self):
      db.session.remove()
      db.drop_all()

  def test_password_hashing(self):
    user = User(username='dave')
    user.set_password('dog')
    self.assertFalse(user.check_password('cat'))
    self.assertTrue(user.check_password('dog'))    

  def test_verify_token(self):
    user = User(id=0)
    token = user.get_email_token()
    valid_token = user.verify_email_token(token)    
    self.assertEqual(user.id, valid_token)

if __name__ == '__main__':
  unittest.main(verbosity=2)