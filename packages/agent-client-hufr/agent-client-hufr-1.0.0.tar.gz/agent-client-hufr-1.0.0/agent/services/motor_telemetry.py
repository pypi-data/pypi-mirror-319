class MotorTelemetryClient:
    def __init__(self, client):
        """
        Initialize the Motor Telemetry client.
        :param client: Instance of ServerClient
        """
        self.client = client

    def send_telemetry(self, data):
        """
        Send motor telemetry data to the server.
        :param data: Dictionary containing motor telemetry data
        :return: Server response as a dictionary
        """
        return self.client.post("/motor-telemetry", data)
