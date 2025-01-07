import os, importlib
from dbt.adapters.events.logging import AdapterLogger

def get_logger(context: str):
    return AdapterLogger(context)
logger = get_logger(__file__)

FUNCTIONS = {}
def register_udf(name: str) -> None:
    def load(f):
        FUNCTIONS[name] = f
    return load

def register_folder(folder_path):
    # Get absolute path
    abs_path = os.path.abspath(folder_path)

    # Walk through all files in the folder
    for root, _, files in os.walk(abs_path):
        for file in files:
            if file.endswith('.py'):
                file_path = os.path.join(root, file)
                
                # Import the module dynamically
                module_name = file[:-3]  # Remove .py extension
                spec = importlib.util.spec_from_file_location(module_name, file_path)
                module = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(module)
                # logger.info(module_name + ' loaded')

def log_error(table: str, column: str, msg: str) -> None:
    logger.error(f"ERROR: {table} {column} {msg}")