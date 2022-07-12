"""This module provides the Process Files database functionality."""
# process_files/database.py

import configparser
from pathlib import Path
from mysql.connector import connect, Error, CMySQLConnection
import typer

from process_files import DB_CONNECT_ERROR, SUCCESS

DEFAULT_DB_HOST = "localhost"
DEFAULT_DB_PORT = 3306

DEFAULT_DB_FILE_PATH = Path.home().joinpath(
    "." + Path.home().stem + "_process_files.json"
)

def connect_database(
    db_host: str,
    db_port: int,
    db_user: str,
    db_password: str,
    db_name: str
) -> (CMySQLConnection | int):
    """Connect the database"""
    print(SUCCESS)
    try:
        with connect(
            host=db_host,
            port=db_port,
            user=db_user,
            password=db_password,
            database=db_name,
        ) as connection:
            # print(connection)
            typer.secho(
                f"Connection successful in {db_host}:{db_port}", fg=typer.colors.GREEN
            )
            return connection
    except Error as e:
        # print(e)
        return DB_CONNECT_ERROR
