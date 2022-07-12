"""This module provides the Process Files database functionality."""
# process_files/database.py

import configparser
from pathlib import Path
from sqlalchemy import create_engine
import typer
from process_files import DB_CONNECT_ERROR, SUCCESS

DEFAULT_DB_HOST = "localhost"
DEFAULT_DB_PORT = 3306

DEFAULT_DB_FILE_PATH = Path.home().joinpath(
    "." + Path.home().stem + "_process_files.json"
)

def create_db_engine(user: str, password: str, db: str, dialect: str = "mysql", driver: str = "pymysql", host: str = "localhost", port: int = 3306):
    """Create engine"""
    try:
        engine = create_engine(f'{dialect}+{driver}://{user}:{password}@{host}:{port}/{db}')
        typer.secho(
            f"Connection successful in {host}:{port}", fg=typer.colors.GREEN
        )
        return engine
    except Error as e:
        # print(e)
        return DB_CONNECT_ERROR
