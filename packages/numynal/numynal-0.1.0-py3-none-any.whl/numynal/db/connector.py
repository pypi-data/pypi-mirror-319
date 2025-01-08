"""
db.connector

This module contains the base Connector class and its specialized subclasses
for handling various data sources, such as CSV, SQL, and MongoDB.

Classes:
    Connector: Abstract base class for database connectors.
"""


class Connector:
    """
    Abstract base class for database connectors.

    This class defines a common interface for different types of data sources.
    Subclasses must implement the `connect` method to establish connections
    and optionally override other methods to handle data interactions.

    Methods:
        connect(): Establishes a connection to the data source.
    """

    def __init__(self, database_uri: str):
        """constructor"""
        self.database_uri = database_uri

    def connect(self) -> None:
        """connects to the data source"""
        raise NotImplementedError("Subclasses must implement this method")

    def read(self):
        """reads the data from the source"""
        raise NotImplementedError("Subclasses must implement this method")

    def write(self):
        """writes the data to a source"""
        raise NotImplementedError("Subclasses must implement this method")
