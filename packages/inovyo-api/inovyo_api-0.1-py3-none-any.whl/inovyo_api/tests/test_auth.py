import unittest
from inovyo_api.auth import generate_token, verify_token

class TestAuthFunctions(unittest.TestCase):

    def setUp(self):
        self.api_token = "seu_api_token"
        self.api_secret = "seu_api_secret"
        self.token = generate_token(self.api_token, self.api_secret)

    def test_generate_token(self):
        self.assertIsNotNone(self.token)

    def test_verify_token(self):
        result = verify_token(self.token)
        self.assertTrue(result.get('valid'))  # Dependendo da resposta da API

if __name__ == '__main__':
    unittest.main()
