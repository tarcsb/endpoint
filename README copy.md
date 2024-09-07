# Directory Tree Coding Challenge

## Overview

This project simulates a directory structure in memory, where you can execute basic file system operations such as creating, moving, deleting, and listing directories. The solution is written in Python and provides a command-line interface to perform these operations based on the input provided. It adheres to the challenge specification provided by Endpoint Recruiting.

## Features

- **Create directories**: Create directories and nested subdirectories in an in-memory storage.
- **Delete directories**: Remove directories from the in-memory structure.
- **Move directories**: Move a directory from one location to another.
- **List directories**: Display the current directory structure in a tree format.

## Commands

- `CREATE <directory_path>`: Create a new directory at the given path.
- `DELETE <directory_path>`: Delete the directory at the given path.
- `MOVE <src_path> <dest_path>`: Move the directory from `src_path` to `dest_path`.
- `LIST`: List all directories in a tree format.

### Input Example

```
CREATE fruits
CREATE vegetables
CREATE grains
CREATE fruits/apples
CREATE fruits/apples/fuji
LIST
CREATE grains/squash
MOVE grains/squash vegetables
CREATE foods
MOVE grains foods
MOVE fruits foods
MOVE vegetables foods
LIST
DELETE fruits/apples
DELETE foods/fruits/apples
LIST
```

### Expected Output

```
CREATE fruits
CREATE vegetables
CREATE grains
CREATE fruits/apples
CREATE fruits/apples/fuji
LIST
fruits
  apples
    fuji
grains
vegetables
CREATE grains/squash
MOVE grains/squash vegetables
CREATE foods
MOVE grains foods
MOVE fruits foods
MOVE vegetables foods
LIST
foods
  fruits
    apples
      fuji
  grains
  vegetables
    squash
DELETE fruits/apples
Cannot delete fruits/apples - fruits does not exist
DELETE foods/fruits/apples
LIST
foods
  fruits
  grains
  vegetables
    squash
```

## How to Run

1. **Install Python**: Make sure you have Python 3.x installed on your system.

2. **Clone the repository** or **download the script**: Save the Python script as `directory.py`.

3. **Run the script**:
   Open a terminal or command prompt, navigate to the directory where `directory.py` is located, and run:

   ```bash
   python directory.py
   ```

4. **Observe Output**: The output should display the directory operations based on the input commands in the script.

## Code Structure

- **`LoggingService`**: Logs messages to the console.
- **`ErrorReportingService`**: Reports errors encountered during directory operations.
- **`ValidationService`**: Validates input commands.
- **`InMemoryStorageProvider`**: Provides an in-memory directory storage.
- **Command Classes**:
  - `CreateCommand`: Handles directory creation.
  - `DeleteCommand`: Handles directory deletion.
  - `MoveCommand`: Handles moving directories.
  - `ListCommand`: Lists the directory structure.
- **`CommandFactory`**: Creates instances of commands based on the input command.
- **`CommandService`**: Processes input commands and delegates them to the appropriate command classes.

## Notes

- This project is a simulation of a file system and does **not** actually create, move, or delete directories on your machine.
- The directory structure is stored in-memory and is represented as nested dictionaries.
  
## Enhancements

If time permits, consider adding more functionality such as:

- Handling edge cases like invalid commands or paths.
- Providing more detailed error messages or a log for debugging.
- Adding the ability to handle file-related operations in addition to directories.
- seprating out the files
- decorators
- development, productionconfig
- error handling, logging
- metrics
- dockoer
- docker compose
- API
- JSON directory
- tests
- ci/cd, Github
- ...
  
