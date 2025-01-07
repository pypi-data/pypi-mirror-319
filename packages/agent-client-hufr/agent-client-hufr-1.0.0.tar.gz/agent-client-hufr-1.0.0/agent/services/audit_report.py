class AuditReportClient:
    def __init__(self, client):
        """
        Initialize the Audit Report client.
        :param client: Instance of ServerClient
        """
        self.client = client

    def generate_report(self, data):
        """
        Generate an audit report on the server.
        :param data: Dictionary containing report data
        :return: Server response as a dictionary
        """
        return self.client.post("/audit-report", data)

    def get_reports(self):
        """
        Retrieve all audit reports from the server.
        :return: Server response as a dictionary
        """
        return self.client.get("/audit-reports")
