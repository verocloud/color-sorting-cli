import logging
import sqlite3
from abc import ABC, abstractmethod
from typing import Any, Callable, Dict, List, Set, Tuple

import typer

from harmony import __version__
from harmony.constants import Resources, TableNames
from harmony.exceptions import InvalidObjectToSaveException
from harmony.models import ColorName, DataModel, InsertQueryData
from harmony.utils import get_resource


class CommandWithVersion:
    """Decorator that adds the CLI installed version to the command help text before
    assigning to the app"""

    def __init__(self, app: typer.Typer) -> None:
        self._app = app

    def __call__(self, command: Callable[..., Any]) -> Any:
        command.__doc__ = self._add_version(command)

        return self._app.command()(command)

    def _add_version(self, command: Callable[..., Any]):
        command_docs = command.__doc__

        if not command_docs:
            command_docs = ""

        return f"*Harmony {__version__} [{command.__name__}]*\n\n{command.__doc__}"


class DatabaseSession(ABC):
    """Interface for the adapter to access a database"""

    def execute_query(self, query: str) -> Set[Tuple[str, ...]]:
        """Execute the passed SQL query and returns its results for SELECT operations

        Args:
            query (str): SQL query

        Returns:
            Set[Tuple[str, ...]]: results of the SELECT query or empty
        """
        self.log_executing_query(query)
        return self.do_execute_query(query)

    @abstractmethod
    def do_execute_query(self, query: str) -> Set[Tuple[str, ...]]:
        """Execute general query

        Args:
            query (str): query to be executed
        """

    def execute_insert(self, query_data: InsertQueryData) -> None:
        """Execute INSERT query

        Args:
            query_data (InsertQueryData): data for executing the INSERT query
        """
        self.execute_query(self.make_insert_query(query_data))

    @abstractmethod
    def commit(self):
        """Commit the changes to the database"""

    @abstractmethod
    def rollback(self):
        """Rollback the changes to the database"""

    @abstractmethod
    def close(self):
        """Close connection to the database"""

    def make_insert_query(self, query_data: InsertQueryData) -> str:
        """Make a insert query string based on the passed data

        Args:
            query_data (InsertQueryData): data to generate the insert query

        Returns:
            str: Query string
        """
        return (
            "INSERT INTO"
            + f"\n\t{query_data.table_name}{str(query_data.columns)}"
            + f"\nVALUES\n\t{str(query_data.values_to_insert)};"
        )

    @property
    @abstractmethod
    def logger(self) -> logging.Logger:
        """Logger for logging the class information"""

    def log_executing_query(self, query: str) -> None:
        """Log query passed

        Args:
            query (str): query to be logged
        """
        self.logger.info("Executing query:\n\n%s\n", query)


class SQLiteSession(DatabaseSession):
    """Adapter for accessing the SQLite database"""

    def __init__(self, connection_string):
        self._connection = sqlite3.connect(connection_string)

    def do_execute_query(self, query: str) -> Set[Tuple[str, ...]]:
        cursor = self._connection.cursor()
        cursor.execute(query)

        results: List[Tuple[str, ...]] = list(cursor)

        cursor.close()

        if results:
            return set(results)

        return set()

    def commit(self) -> None:
        self._connection.commit()

    def rollback(self) -> None:
        self._connection.rollback()

    def close(self) -> None:
        self._connection.close()

    @property
    def logger(self) -> logging.Logger:
        return logging.getLogger(self.__class__.__name__)


class SQLiteSessionFactory:
    # pylint: disable=missing-class-docstring

    def make_session(self) -> DatabaseSession:
        """Make a new session for accessing the SQLite database"""
        return SQLiteSession(get_resource(Resources.SQLITE_DATABASE))


class Repository(ABC):
    """Interface for the database table access adapters"""

    @abstractmethod
    def create_table_if_not_exists(self) -> None:
        """Create the table refered to the repository if it does not exist"""

    @abstractmethod
    def save(self, object_to_store: DataModel) -> None:
        """Save the passed object to the database"""


class ColorNameRepository(Repository):
    """Provide access to the basic CRUD operation on the color names table on
    database"""

    NAME_COLUMN = "name"
    HUE_COLUMN = "hue"
    SATURATION_COLUMN = "saturation"
    LUMINOSITY_COLUMN = "luminosity"

    def __init__(self, session: DatabaseSession) -> None:
        self._session = session
        self.create_table_if_not_exists()

    def create_table_if_not_exists(self) -> None:
        self._session.execute_query(
            f"CREATE TABLE IF NOT EXISTS {TableNames.COLOR_NAME} ("
            + "id INTEGER PRIMARY KEY AUTOINCREMENT,"
            + f"{self.NAME_COLUMN} VARCHAR(255) NOT NULL UNIQUE,"
            + f"{self.HUE_COLUMN} FLOAT NOT NULL,"
            + f"{self.SATURATION_COLUMN} FLOAT NOT NULL,"
            + f"{self.LUMINOSITY_COLUMN} FLOAT NOT NULL"
            + ");"
        )

    def save(self, object_to_store: DataModel) -> None:
        self._session.execute_insert(
            self._make_insert_query_data_from_data_model(object_to_store)
        )

    def _make_insert_query_data_from_data_model(
        self, data_model: DataModel
    ) -> InsertQueryData:
        return self._make_insert_query_data(
            self._parse_data_model_to_color_name(data_model)
        )

    def _make_insert_query_data(self, color_name_data) -> InsertQueryData:
        return InsertQueryData(
            TableNames.COLOR_NAME, self._get_data_to_insert(color_name_data)
        )

    @staticmethod
    def _parse_data_model_to_color_name(object_to_parse: DataModel) -> ColorName:
        if isinstance(object_to_parse, ColorName):
            return object_to_parse

        raise InvalidObjectToSaveException("Passed object is not a ColorName instance")

    def _get_data_to_insert(self, color_name_data: ColorName) -> Dict[str, Any]:
        return {
            self.NAME_COLUMN: color_name_data.name,
            self.HUE_COLUMN: color_name_data.hsl.hue,
            self.SATURATION_COLUMN: color_name_data.hsl.saturation,
            self.LUMINOSITY_COLUMN: color_name_data.hsl.luminosity,
        }
