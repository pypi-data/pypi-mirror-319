class SensorDataClient:
    def __init__(self, client):
        """
        Initialize the Sensor Data client.
        :param client: Instance of ServerClient
        """
        self.client = client

    def send_sensor_data(self, data):
        """
        Send sensor data to the server.
        :param data: Dictionary containing sensor data
        :return: Server response as a dictionary
        """
        return self.client.post("/sensor-data", data)
