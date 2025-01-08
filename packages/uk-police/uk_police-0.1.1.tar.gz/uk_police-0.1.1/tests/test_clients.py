import unittest
from unittest.mock import patch
from Pyolice.client import Pyolice
from Pyolice.exceptions import APIError

class TestPyoliceClient(unittest.TestCase):
    def setUp(self):
        self.client = Pyolice()

    @patch("requests.get")
    def test_get_successful_response(self, mock_get):
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = {"key": "value"}
        endpoint = "test-endpoint"
        result = self.client._get(endpoint)
        mock_get.assert_called_once_with(f"{self.client.BASE_URL}/{endpoint}", params=None)
        self.assertEqual(result, {"key": "value"})

    @patch("requests.get")
    def test_get_with_params(self, mock_get):
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = {"key": "value"}
        endpoint = "test-endpoint"
        params = {"param1": "value1", "param2": "value2"}
        result = self.client._get(endpoint, params=params)
        mock_get.assert_called_once_with(f"{self.client.BASE_URL}/{endpoint}", params=params)
        self.assertEqual(result, {"key": "value"})

    @patch("requests.get")
    def test_get_raises_api_error_on_failure(self, mock_get):
        from requests.exceptions import RequestException
        mock_get.side_effect = RequestException("Request failed")
        endpoint = "test-endpoint"
        with self.assertRaises(APIError):
            self.client._get(endpoint)

    @patch("requests.get")
    def test_get_raises_api_error_on_non_200_status(self, mock_get):
        from requests.exceptions import RequestException
        mock_get.return_value.status_code = 404
        mock_get.return_value.raise_for_status.side_effect = RequestException("Not Found")
        endpoint = "test-endpoint"
        with self.assertRaises(APIError):
            self.client._get(endpoint)

if __name__ == "__main__":
    unittest.main()
