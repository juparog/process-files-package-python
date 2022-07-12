# tests/test_process_files.py

from typer.testing import CliRunner

from process_files import __app_name__, __version__, cli

runner = CliRunner()

def test_version():
    result = runner.invoke(cli.app, ["--version"])
    assert result.exit_code == 0
    assert f"{__app_name__} v{__version__}\n" in result.stdout

# test for upload exfel file
def test_load_excel_file():
    result = runner.invoke(cli.app, ["load_excel_file", "./test/files/test-data-file.xls", "-u", "root", "-p", "supersecret", "-n", "company", "-s", "./test/files/spec_data_load.json"])
    assert result.exit_code == 0
    assert f"Data upload successful!" in result.stdout

    result = runner.invoke(cli.app, ["load_excel_file", "-u", "root", "-p", "supersecret", "-n", "company", "-s", "./test/files/spec_data_load.json"])
    assert result.exit_code == 2
    assert f"Missing argument 'EXCEL_FILE'" in result.stdout
