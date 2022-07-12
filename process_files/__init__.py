"""Top-level package for Process Files."""
# process_files/__init__.py

__app_name__ = "process_files"
__version__ = "0.1.0"

(
    SUCCESS,
    VALIDATE_EXTENSION,
    DB_CONNECT_ERROR,
    FILE_NOT_FOUND,
    FILE_PERMISSION,
    FILE_IS_A_DIRECTORY,
    WRONG_FORMAT,
    KEY_ERROR
) = range(8)

ERRORS = {
    VALIDATE_EXTENSION: "The spec file must have a '.json' extension",
    DB_CONNECT_ERROR: "Database connection could not be established.",
    FILE_NOT_FOUND: "File not found!",
    FILE_PERMISSION: "Insufficient permission",
    FILE_IS_A_DIRECTORY: "File is a directory!",
    WRONG_FORMAT: "The content of the file is incorrectly formatted",
    KEY_ERROR: "The key '{}' not found in spec file"
}
