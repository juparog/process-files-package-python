"""This module provides the Process Files CLI."""
# process_files/cli.py

from typing import Optional
import typer
from process_files.utils import get_value_json, upload_excel_to_db, read_excel_file, read_json_file, validate_extension
from process_files import ERRORS, __app_name__, __version__, database

app = typer.Typer()

@app.command(name="load_excel_file")
def load_excel_file(
    excel_file: str = typer.Argument(
        ...,
        help='Excel file with data to upload'
    ),
    db_host: str = typer.Option(
        str(database.DEFAULT_DB_HOST),
        "--db-host",
        "-h",
        help='Database host'
    ),
    db_port: int = typer.Option(
        str(database.DEFAULT_DB_PORT),
        "--db-port",
        "-pr",
        help='Database port'
    ),
    db_user: str = typer.Option(
        ...,
        "--db-user",
        "-u",
        help='Database user'
    ),
    db_password: str = typer.Option(
        ...,
        "--db-password",
        "-p",
        help='Database password'
    ),
    db_name: str = typer.Option(
        ...,
        "--db-name",
        "-n",
        help='Database name'
    ),
    spec_file: str = typer.Option(
        ...,
        "--spec-file",
        "-s",
        help='Spec file to upload'
    )
) -> None:
    """Upload excel file to database"""

    invalid_extension = validate_extension(spec_file, ".json")
    # file extension validation
    if invalid_extension:
        typer.secho(
            f'Spec file load failed with "{ERRORS[invalid_extension]}"',
            fg=typer.colors.RED,
        )
        raise typer.Exit(1)

    spec_data = read_json_file(spec_file)
    # spec load validation
    if type(spec_data).__name__ != "dict":
        typer.secho(
            f'Spec file load failed with "{ERRORS[spec_data]}"',
            fg=typer.colors.RED,
        )
        raise typer.Exit(1)

    data_sheet  = get_value_json(spec_data, "sheet.name")
    # sheet name validation
    if type(data_sheet).__name__ != "dict":
        typer.secho(
            f'Get sheet name failed with "{ERRORS[data_sheet].format("sheet.name")}"',
            fg=typer.colors.RED,
        )
        raise typer.Exit(1)

    df = read_excel_file(excel_file, data_sheet["value"])
    # excel file validation
    if type(df).__name__ != "DataFrame":
        typer.secho(
            f'Excel file load failed with "{ERRORS[df]}"',
            fg=typer.colors.RED,
        )
        raise typer.Exit(1)

    engine = database.create_db_engine(
        db_user,
        db_password,
        db_name
    )

    # connection database validation
    if type(engine).__name__ != "Engine":
        typer.secho(
            f'Creating connectiong database failed with "{ERRORS[engine]}"',
            fg=typer.colors.RED,
        )
        raise typer.Exit(1)

    upload = upload_excel_to_db(df, spec_data, engine)
    # connection database validation
    if type(upload).__name__ != "bool":
        typer.secho(
            f'Insert data failed with "{ERRORS[upload]}"',
            fg=typer.colors.RED,
        )
        raise typer.Exit(1)

    typer.secho(
        f"Data upload successful!", fg=typer.colors.GREEN
    )

def _version_callback(value: bool) -> None:
    if value:
        typer.echo(f"{__app_name__} v{__version__}")
        raise typer.Exit()


@app.callback()
def main(
    version: Optional[bool] = typer.Option(
        None,
        "--version",
        "-v",
        help="Show the application's version and exit.",
        callback=_version_callback,
        is_eager=True,
    )
) -> None:
    return
