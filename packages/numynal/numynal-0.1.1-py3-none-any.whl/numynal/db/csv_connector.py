"""
Module: csv_connector
======================

This module provides the `CSVConnector` class, which extends the base `Connector`
class. It enables reading from and writing to CSV files using pandas.

Classes:
    - CSVConnector: Handles CSV file operations with pandas.

Usage:
    from numynal.db.csv_connector import CSVConnector

    connector = CSVConnector("input.csv", "output.csv")
    df = connector.read()
    connector.write()

Dependencies:
    - pandas
    - numynal.db.connector

Author:
    Mohammed Affan

Version:
    0.1.0
"""

import pandas as pd

from numynal.db.connector import Connector


class CSVConnector(Connector):
    """
    A connector class for handling CSV files.

    Inherits from the Connector base class and provides functionality to
    read from and write to CSV files.

    Attributes:
        dataframe_ptr (pd.DataFrame): Pointer to the loaded DataFrame.

    Methods:
        connect(): Establishes a connection to a CSV file (placeholder).
        read(filepath: str) -> pd.DataFrame: Reads a CSV file into a DataFrame.
        write(filepath: str) -> None: Writes a DataFrame to a CSV file.
    """

    def __init__(self, i_filepath: str, o_filepath):
        super().__init__(i_filepath)
        self.dataframe_ptr: pd.DataFrame | None = None  # Initialize as None
        self.o_filepath = o_filepath

    def connect(self):
        return

    def read(self) -> pd.DataFrame:
        """
        Reads the input CSV file into a pandas DataFrame.
        """

        self.dataframe_ptr = pd.read_csv(self.database_uri)
        return self.dataframe_ptr

    def write(self) -> None:
        """
        Writes a pandas DataFrame to the output CSV file.
        """

        if self.dataframe_ptr is None:
            raise ValueError("No DataFrame loaded. Use the read method first.")
        self.dataframe_ptr.to_csv(self.o_filepath, index=False)
