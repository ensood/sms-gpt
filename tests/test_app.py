import unittest
from app import app

class TestApp(unittest.TestCase):
    def setUp(self):
        app.config['TESTING'] = True
        self.app = app.test_client()

    def test_index_route(self):
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data.decode('utf-8'), 'Welcome to SMS GPT!')

    def test_sms_stat_route(self):
        response = self.app.get('/sms-stat?n=5')
        if response.status_code == 200:
            data = response.get_json()
            self.assertIn('message_count', data)
            self.assertIn('list_of_last_5_messages', data)
        else:
            self.assertEqual(response.status_code, 500)

if __name__ == '__main__':
    unittest.main()
    