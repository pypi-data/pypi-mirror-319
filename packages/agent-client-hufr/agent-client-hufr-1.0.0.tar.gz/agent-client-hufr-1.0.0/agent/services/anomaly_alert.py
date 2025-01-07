class AnomalyAlertClient:
    def __init__(self, client):
        """
        Initialize the Anomaly Alert client.
        :param client: Instance of ServerClient
        """
        self.client = client

    def send_alert(self, data):
        """
        Send anomaly alert data to the server.
        :param data: Dictionary containing alert data
        :return: Server response as a dictionary
        """
        return self.client.post("/anomaly-alert", data)
