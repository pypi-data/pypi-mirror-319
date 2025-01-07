class DataStorageClient:
    def __init__(self, client):
        """
        Initialize the Data Storage client.
        :param client: Instance of ServerClient
        """
        self.client = client

    def store_event(self, data):
        """
        Store event data on the server.
        :param data: Dictionary containing event data
        :return: Server response as a dictionary
        """
        return self.client.post("/store-event", data)

    def query_events(self, filters):
        """
        Query events from the server.
        :param filters: Dictionary containing query filters
        :return: Server response as a dictionary
        """
        return self.client.get("/query-events", filters)
