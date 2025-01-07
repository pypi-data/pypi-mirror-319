# Copyright 2025 Kasma
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied
# See the License for the specific language governing permissions and
# limitations under the License.

from typing import List, Union, Tuple
from .utils.json import Record
from ._client import ClientImpl
from .utils.utils import DataType

class GraphDatabase:
    @staticmethod
    def driver(uri: str, timeout: int = 120):
        if not uri.startswith("http://"):
            raise ValueError("Invalid URI: Only 'http://' protocol is supported")
        host, port = uri.removeprefix("http://").split(":")
        return Client(host, port, timeout)

class Client:
    """A client for the Flavius graph database"""

    def __init__(self, host: str = "localhost", port: int = 30000, timeout: int = 120):
        self._impl = ClientImpl(host, port, timeout)

    def verify_connectivity(self):
        """Verify the connection to the Flavius server"""
        self._impl.verify_connectivity()

    def close(self):
        """Close the connection to the Flavius server"""
        self._impl.close()

    def create_namespace(self, namespace: str):
        """Create a namespace"""
        self._impl.create_namespace(namespace)

    def drop_namespace(self, namespace: str):
        """Drop a namespace and all graphs inside"""
        self._impl.drop_namespace(namespace)

    def list_namespace(self) -> List[str]:
        """List all namespaces"""
        return self._impl.list_namespace()

    def create_graph(self, graph: str, namespace: str):
        """Create a graph"""
        self._impl.create_graph(graph, namespace)

    def drop_graph(self, graph: str, namespace: str):
        """Drop graph and all underlying vertex tables and edge tables"""
        self._impl.drop_graph(graph, namespace)

    def list_graph(self, namespace: str) -> List[str]:
        """List graph under a namespace"""
        return self._impl.list_graph(namespace)

    def create_vertex_table(
        self,
        table: str,
        columns: List[Union[Tuple[str, DataType], Tuple[str, DataType, bool]]],
        primary_key: Union[str, List[str]],
        namespace: str,
        graph: str,
    ):
        """Create a vertex table in the graph.

        :param table: Name of the vertex table to create
        :param columns: List of column definitions. Each column can be defined as either:\n
            - (column_name, data_type) for nullable columns\n
            - (column_name, data_type, is_nullable) for explicit nullability\n
        :param primary_key: Primary key column name or list of column names for composite key
        :param namespace: Namespace where the vertex table will be created
        :param graph: Graph where the vertex table will be created
        :raises AssertionError: If the vertex table creation fails

        Example::

            driver.create_vertex_table(
                table="Person",
                columns=[
                    ("id", DataType.INT, False), # NOT NULL
                    ("name", DataType.STRING, False), # NOT NULL
                    ("created_at", DataType.TIMESTAMP, False), # NOT NULL
                    ("age", DataType.INT, True), # NULLABLE
                ],
                primary_key="id",
                namespace="social",
                graph="relationships"
            )
        """
        self._impl.create_vertex_table(table, columns, primary_key, namespace, graph)

    def drop_vertex_table(self, table: str, namespace: str, graph: str):
        """Drop a vertex table with given name"""
        self._impl.drop_vertex_table(table, namespace, graph)

    def list_vertex(self, namespace: str, graph: str) -> List[str]:
        """List all vertex table names"""
        return self._impl.list_vertex(namespace, graph)

    def create_edge_table(
        self,
        table: str,
        source_vertex: str,
        target_vertex: str,
        columns: List[Union[Tuple[str, DataType], Tuple[str, DataType, bool]]],
        directed: bool,
        namespace: str,
        graph: str,
        reverse_edge: str = None,
    ):
        """Create a edge table in the graph.

        :param table: Name of the edge table to create
        :param source_vertex: Name of the source vertex table
        :param target_vertex: Name of the target vertex table
        :param columns: List of column definitions. Each column can be defined as either:\n
            - (column_name, data_type) for nullable columns\n
            - (column_name, data_type, is_nullable) for explicit nullability\n
        :param directed: Whether the edge is directed (True) or undirected (False)
        :param namespace: Namespace where the edge table will be created
        :param graph: Graph where the edge table will be created
        :param reverse_edge: Name of the reverse edge table for directed edges, defaults to None
        :raises AssertionError: If the edge table creation fails

        Example::

            driver.create_edge_table(
                table="follow",
                source_vertex="Person",
                target_vertex="Person",
                columns=[
                    ("since", DataType.DATETIME), # NULLABLE
                    ("weight", DataType.FLOAT, False) # NOT NULL
                ],
                directed=True,
                namespace="social",
                graph="relationships",
                reverse_edge="followed_by"
            )
        """
        self._impl.create_edge_table(
            table,
            source_vertex,
            target_vertex,
            columns,
            directed,
            namespace,
            graph,
            reverse_edge,
        )

    def drop_edge_table(self, table: str, namespace: str, graph: str):
        """Drop an edge table with given name"""
        self._impl.drop_edge_table(table, namespace, graph)

    def list_edge(self, namespace: str, graph: str) -> List[str]:
        """List all edge table names"""
        return self._impl.list_edge(namespace, graph)

    def execute_query(
        self,
        query: str,
        namespace: str,
        graph: str,
        parameters: dict = None,
    ) -> Tuple[List[Record], List[str]]:
        """Execute a Cypher query against the graph database.

        :param query: The Cypher query to execute
        :param namespace: The namespace where the query will be executed
        :param graph: The graph where the query will be executed
        :param parameters: Optional dictionary of query parameters. Supports the following types:\n
            - Basic types: int, float, bool, str\n
            - Temporal types: datetime, date, time, TimeStamp\n
            - Complex types: list, dict\n
        :return: A tuple containing (records, keys), where:\n
            - records: List of Record objects containing the query results\n
            - keys: List of strings representing the column names
        :raises AssertionError: If the query execution fails

        Example::

            # Simple query with basic parameters
            records, keys = driver.execute_query(
                "MATCH (n:User) RETURN n",
                namespace="social",
                graph="relationships",
            )

            # Query with complex parameters
            from datetime import datetime
            from flavius import TimeStamp

            records, keys = driver.execute_query(
                "MATCH (n:User) WHERE n.created_at < $timestamp AND n.age IN $age RETURN n",
                namespace="social",
                graph="relationships",
                parameters={
                    "timestamp": TimeStamp(datetime.now()),
                    "age": [18, 20, 22]
                }
            )
        """
        return self._impl.execute_query(query, namespace, graph, parameters)
