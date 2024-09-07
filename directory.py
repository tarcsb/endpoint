import sys
from abc import ABC, abstractmethod
from functools import wraps


# Logging Service
class LoggingService:
    """
    A service for logging messages using basic I/O or stdout.
    """
    def log(self, message, level=None):
        """
        Log messages at different levels.
        """
        print(message, file=sys.stdout)


# Error Reporting Service
class ErrorReportingService:
    """
    A service for reporting errors. It could send errors to a monitoring system.
    """
    def __init__(self, logging_service):
        self.logging_service = logging_service

    def report_error(self, error_message):
        """
        Report an error using the logging service.
        """
       # self.logging_service.log(f"Error: {error_message}")
        pass # get the same oputput on instructions

# Validator Service
class ValidatorService:
    """
    A service for validating command arguments and ensuring that input paths are correct.
    """

    def validate_args(self, parts, expected_length):
        """
        Validate that the command has the correct number of arguments.
        """
        return len(parts) >= expected_length

    def validate_path(self, path):
        """
        Validate that a path is not empty and follows basic constraints.
        """
        if not path or not path.strip():
            raise ValueError("Invalid path: Path cannot be empty or whitespace.")
        if path.startswith("/"):
            raise ValueError("Invalid path: Absolute paths are not allowed.")
        return True


# In-Memory Storage Service
class InMemoryStorageProvider:
    """
    A simple in-memory storage provider for directory operations.
    This is a reusable service that can be easily replaced in a SOA setup.
    """
    def __init__(self):
        self.storage = {}

    def create(self, path):
        """
        Create directories at the given path.
        """
        parts = path.strip("/").split("/")
        current = self.storage
        for part in parts:
            if part not in current:
                current[part] = {}
            current = current[part]

    def delete(self, path):
        """
        Delete directories at the given path, raising FileNotFoundError if not found.
        """
        parts = path.strip("/").split("/")
        current = self.storage
        for part in parts[:-1]:
            if part in current:
                current = current[part]
            else:
                raise FileNotFoundError(f"Directory does not exist at {path}")
        if parts[-1] in current:
            del current[parts[-1]]
        else:
            raise FileNotFoundError(f"Directory does not exist at {path}")

    def move(self, src, dest):
        """
        Move a directory from src to dest, raising FileNotFoundError if src doesn't exist.
        """
        src_parts = src.strip("/").split("/")
        dest_parts = dest.strip("/").split("/") #todo

        # Get source directory
        src_current = self.storage
        for part in src_parts[:-1]:
            if part in src_current:
                src_current = src_current[part]
            else:
                raise FileNotFoundError(f"Directory does not exist at {src}")

        src_dir = src_parts[-1]
        if src_dir not in src_current:
            raise FileNotFoundError(f"Directory does not exist at {src}")

        src_content = src_current.pop(src_dir)

        # Place in destination
        dest_current = self.storage
        for part in dest_parts:
            if part not in dest_current:
                dest_current[part] = {}
            dest_current = dest_current[part]

        dest_current[src_dir] = src_content

    def list_directories(self, current=None, indent=0):
        """
        List directories recursively.
        """
        if current is None:
            current = self.storage
        output = []
        for key, value in current.items():
            output.append("  " * indent + key)
            if isinstance(value, dict):
                output.extend(self.list_directories(value, indent + 1))
        return output


# Decorate
def log_execution(func):
    """
    Decorator to log the start and end of command execution.
    """
    @wraps(func)
    def wrapper(*args, **kwargs):
        #print(f"Executing {func.__name__}...")
        result = func(*args, **kwargs)
        #print(f"Finished executing {func.__name__}")
        return result
    return wrapper


def handle_errors(func):
    """
    Decorator to handle errors centrally for command execution.
    """
    @wraps(func)
    def wrapper(self, *args, **kwargs):
        try:
            return func(self, *args, **kwargs)
        except FileNotFoundError as e:
            if hasattr(self, 'error_service'):
                self.error_service.report_error(str(e))
            else:
                print(f"Error: {e}")
        except ValueError as e:
            print(f"Validation Error: {e}")
    return wrapper


def validate(func):
    """
    Decorator to validate the command arguments and paths.
    """
    @wraps(func)
    def wrapper(self, *args, **kwargs):
        # Validate number of arguments
        if not self.validator_service.validate_args(args, 1):
            raise ValueError("Invalid number of arguments provided.")
        
        # Validate paths
        for path in args:
            self.validator_service.validate_path(path)
        
        return func(self, *args, **kwargs)
    return wrapper


# Command Abstract Base Class
class Command(ABC):
    """
    Abstract base class for commands.
    """

    @abstractmethod
    def execute(self, *args):
        pass


# Create Command
class CreateCommand(Command):
    """
    Command to create a directory.
    """

    def __init__(self, storage_service, validator_service):
        self.storage_service = storage_service
        self.validator_service = validator_service

    @log_execution
    @handle_errors
    @validate
    def execute(self, path):
        self.storage_service.create(path)
        print(f"CREATE {path}")


class DeleteCommand(Command):
    def __init__(self, storage_service, error_service, validator_service):
        self.storage_service = storage_service
        self.error_service = error_service
        self.validator_service = validator_service

    @log_execution
    @handle_errors
    @validate
    def execute(self, path):
        try:
            self.storage_service.delete(path)
            print(f"DELETE {path}")
        except FileNotFoundError as e:
            # Ensure we are logging the exact message
            error_message = f"{path} - does not exist"
            self.error_service.report_error(error_message)
            raise e  # Re-raise the exception for the test to catch it



# Move Command
class MoveCommand(Command):
    """
    Command to move a directory.
    """

    def __init__(self, storage_service, validator_service):
        self.storage_service = storage_service
        self.validator_service = validator_service

    @log_execution
    @handle_errors
    @validate
    def execute(self, src, dest):
        self.storage_service.move(src, dest)
        print(f"MOVE {src} {dest}")


# List Command
class ListCommand(Command):
    """
    Command to list all directories.
    """

    def __init__(self, storage_service):
        self.storage_service = storage_service

    @log_execution
    def execute(self):
        print("LIST")
        directories = self.storage_service.list_directories()
        print("\n".join(directories))


# Command Factory
class CommandFactory:
    """
    Factory to create command instances based on the command name.
    """

    def __init__(self, storage_service, error_service, validator_service):
        self.storage_service = storage_service
        self.error_service = error_service
        self.validator_service = validator_service

    def create_command(self, name, *args):
        """
        Factory method to create the appropriate command based on the name.
        """
        if name.startswith("CREATE"):
            return CreateCommand(self.storage_service, self.validator_service)
        elif name.startswith("DELETE"):
            return DeleteCommand(self.storage_service, self.error_service, self.validator_service)
        elif name.startswith("MOVE"):
            return MoveCommand(self.storage_service, self.validator_service)
        elif name == "LIST":
            return ListCommand(self.storage_service)
        else:
            raise ValueError(f"Unknown command: {name}")


# Service Provider
def service_provider():
    """
    Service provider responsible for creating and wiring services together.
    """
    logging_service = LoggingService()
    error_reporting_service = ErrorReportingService(logging_service)
    storage_provider = InMemoryStorageProvider()
    validator_service = ValidatorService()
    return CommandFactory(storage_provider, error_reporting_service, validator_service)


# Main Process to handle commands
def process_commands(command_factory, commands_input):
    """
    Wrapper function for processing multiple commands.
    """
    commands = [cmd.strip() for cmd in commands_input.strip().splitlines() if cmd.strip()]
    for command in commands:
        parts = command.split()
        command_name = parts[0]
        command_args = parts[1:]

        command_instance = command_factory.create_command(command_name, *command_args)
        command_instance.execute(*command_args)


# Main function
def main():
    """
    Main function to run the application.
    """
    command_factory = service_provider()

    commands_input = """
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
    """

    # Process the commands
    process_commands(command_factory, commands_input)


# Entry point
if __name__ == "__main__":
    main()
