import requests

class ServerClient:
    def __init__(self, base_url):
        """
        Initialize the client with the base URL of the Flask server.
        :param base_url: Base URL of the Flask server (e.g., http://localhost:5000/api)
        """
        self.base_url = base_url

    def post(self, endpoint, data):
        """
        Sends a POST request to the server.
        :param endpoint: API endpoint (e.g., /motor-telemetry)
        :param data: Data to send in the request body
        :return: Server response as a dictionary
        """
        url = f"{self.base_url}{endpoint}"
        try:
            response = requests.post(url, json=data)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            raise Exception(f"POST request failed: {e}")

    def get(self, endpoint, params=None):
        """
        Sends a GET request to the server.
        :param endpoint: API endpoint (e.g., /audit-reports)
        :param params: Query parameters
        :return: Server response as a dictionary
        """
        url = f"{self.base_url}{endpoint}"
        try:
            response = requests.get(url, params=params)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            raise Exception(f"GET request failed: {e}")
