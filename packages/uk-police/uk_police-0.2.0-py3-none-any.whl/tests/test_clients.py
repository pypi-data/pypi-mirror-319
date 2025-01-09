import unittest
from unittest.mock import patch
from uk_police.client import uk_police
from uk_police.exceptions import *
import requests

class TestPyoliceClient(unittest.TestCase):
    def setUp(self):
        self.client = uk_police()

    @patch("requests.get")
    def test_get_successful_response(self, mock_get):
        mock_response = mock_get.return_value
        mock_response.status_code = 200
        mock_response.json.return_value = {"key": "value"}

        endpoint = "test-endpoint"
        result = self.client._get(endpoint)

        self.assertEqual(result, {"key": "value"})
        mock_get.assert_called_once_with(
            f"{self.client.BASE_URL}/{endpoint}",
            params=None,
            timeout=10
        )

    @patch("requests.get")
    def test_get_with_params(self, mock_get):
        mock_response = mock_get.return_value
        mock_response.status_code = 200
        mock_response.json.return_value = {"key": "value"}

        endpoint = "test-endpoint"
        params = {"param1": "value1", "param2": "value2"}
        result = self.client._get(endpoint, params=params)

        self.assertEqual(result, {"key": "value"})
        mock_get.assert_called_once_with(
            f"{self.client.BASE_URL}/{endpoint}",
            params=params,
            timeout=10
        )

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
    
    @patch("requests.get")
    def test_rate_limit_retry(self, mock_get):
        mock_response = mock_get.return_value
        mock_response.status_code = 429
        mock_response.headers = {"Retry-After": "2"}
        mock_response.raise_for_status.side_effect = requests.exceptions.HTTPError()

        with self.assertRaises(RateLimitError) as context:
            self.client._get("some-endpoint")

        self.assertEqual(context.exception.retry_after, 2)

if __name__ == "__main__":
    unittest.main()
