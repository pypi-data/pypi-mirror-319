import logging
import lancedb
from lancedb.table import Table
from typing import Any, Dict, List
from pathlib import Path
import pandas as pd
import pyarrow as pa

from .base_vector_db import BaseVectorDB

from tigergraphx.config import LanceDBConfig

logger = logging.getLogger(__name__)


class LanceDBManager(BaseVectorDB):
    """Implementation of LanceDB vector database management."""

    SCHEMA = pa.schema(
        [
            pa.field("id", pa.string()),
            pa.field("text", pa.string()),
            pa.field("vector", pa.list_(pa.float64())),
            pa.field("attributes", pa.string()),
        ]
    )
    config: LanceDBConfig

    def __init__(
        self,
        config: LanceDBConfig | Dict | str | Path,
    ):
        """
        Initialize the LanceDB manager by connecting and setting up schema.

        Args:
            config (LanceDBConfig | Dict | str | Path): Configuration for LanceDB, either as a
                config object, dictionary, string, or path to configuration file.
        """
        config = LanceDBConfig.ensure_config(config)
        super().__init__(config)
        self.TABLE_NAME = self.config.table_name
        self.connect(
            uri=self.config.uri,
            api_key=self.config.api_key,
            region=self.config.region,
            host_override=self.config.host_override,
            read_consistency_interval=self.config.read_consistency_interval,
            request_thread_pool=self.config.request_thread_pool,
        )

    def connect(self, uri: str | Path, **kwargs: Any) -> None:
        """
        Connect to LanceDB and initialize or open the specified table.

        Args:
            uri (str | Path): The URI to connect to the LanceDB database.
            **kwargs: Additional connection parameters.
        """
        logger.info(f"Attempting to connect to LanceDB at URI: {uri}")

        # Establish connection to the LanceDB database
        self._connection = lancedb.connect(uri, **kwargs)
        logger.info("Successfully connected to LanceDB.")

        # Check if the table exists; if so, open it, otherwise create a new table
        if self.TABLE_NAME in self._connection.table_names():
            logger.info(f"Table '{self.TABLE_NAME}' found. Opening the table.")
            self._table = self._connection.open_table(self.TABLE_NAME)
        else:
            logger.info(f"Table '{self.TABLE_NAME}' not found. Creating a new table.")
            self._table = self._connection.create_table(
                self.TABLE_NAME, schema=self.SCHEMA
            )
            logger.info(f"Table '{self.TABLE_NAME}' created successfully.")

    def get_table(self) -> Table:
        """
        Retrieve the current table.

        Returns:
            Table: The LanceDB table object.
        """
        return self._table

    def insert_data(self, data: pd.DataFrame) -> None:
        """
        Insert data into the LanceDB table.

        Args:
            data (pd.DataFrame): DataFrame containing the data to be inserted.
        """
        records = data.to_dict(orient="records")
        if not self._table:
            self._table = self._connection.open_table(self.TABLE_NAME)
        self._table.add(records)

    def query(
        self, query_embedding: List[float], k: int = 10, **kwargs: Any
    ) -> List[str]:
        """
        Perform a similarity search by vector and return results as a list of IDs.

        Args:
            query_embedding (List[float]): The query vector for similarity search.
            k (int, optional): Number of top results to retrieve. Defaults to 10.
            **kwargs (Any): Additional parameters for the search.

        Returns:
            List[str]: List of IDs from the search results.

        Raises:
            ValueError: If the table is not initialized or no results are found.
        """
        # Ensure the table is initialized
        if not self._table:
            raise ValueError(
                "Table does not exist. Please ensure the table is created first."
            )

        # Perform the similarity search
        docs = self._table.search(query=query_embedding).limit(k).to_list()

        # Return an empty list if no documents are found
        if not docs:
            return []

        # Extract and return IDs from the search results
        return [doc["id"] for doc in docs]
