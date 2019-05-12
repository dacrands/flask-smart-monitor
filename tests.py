import unittest
from app import app, db
from app.models import User

class UserModelCase(unittest.TestCase):
  def test_password_hashing(self):
    u = User(username='dave')
    u.set_password('dog')
    self.assertFalse(u.check_password('cat'))
    self.assertTrue(u.check_password('dog'))    


if __name__ == '__main__':
  unittest.main(verbosity=2)