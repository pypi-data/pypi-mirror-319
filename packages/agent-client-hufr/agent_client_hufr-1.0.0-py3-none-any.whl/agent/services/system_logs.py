class SystemLogsClient:
    def __init__(self, client):
        """
        Initialize the System Logs client.
        :param client: Instance of ServerClient
        """
        self.client = client

    def send_system_log(self, data):
        """
        Send system log data to the server.
        :param data: Dictionary containing system log data
        :return: Server response as a dictionary
        """
        return self.client.post("/system-log", data)
