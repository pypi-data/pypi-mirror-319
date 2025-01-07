from typing import Any
from typing import Dict
import os

from dbt.adapters.duckdb.plugins import BasePlugin
from dbt.adapters.duckdb.utils import SourceConfig
from dbt.adapters.duckdb.utils import TargetConfig
from dbt.adapters.events.logging import AdapterLogger
from duckdb import DuckDBPyConnection
from duckdb.functional import FunctionNullHandling, PythonUDFType

from dbt_duckdb_udf.utils.utils import FUNCTIONS, register_folder
from dbt_duckdb_udf import udf


logger = AdapterLogger("DuckDBUDF")


class Plugin(BasePlugin):
    def initialize(self, plugin_config: Dict[str, Any]):
        self._config = plugin_config
        logger.info(f"Initialized custom plugin: {plugin_config}")

    def configure_connection(self, conn: DuckDBPyConnection):
        """
        Configure the DuckDB connection with any necessary extensions and/or settings.
        This method should be overridden by subclasses to provide additional
        configuration needed on the connection, such as user-defined functions.

        :param conn: A DuckDBPyConnection instance to be configured.
        """
        if "external_udf_paths" in self._config:
            external_udf_paths = self._config.get("external_udf_paths")
            for external_udf_path in external_udf_paths:
                try:
                    logger.info(f"Loading UDFs from {external_udf_path} ...")
                    register_folder(external_udf_path)
                except Exception as e:
                    logger.info(f"Error loading UDFs from {external_udf_path}: {e}")
                    raise e
        logger.info(f"Loading UDFs from {os.path.dirname(udf.__file__)} ...")
        register_folder(os.path.dirname(udf.__file__))
        for k, v in FUNCTIONS.items():
            conn.create_function(k, v, null_handling=FunctionNullHandling.SPECIAL, type='arrow')
            logger.info(f"Loaded custom function {k}")
        logger.info(f"{len(FUNCTIONS)} functions discovered!")

    def load(self, source_config: SourceConfig):
        # Implement loading logic if needed
        logger.info("Loading data")
        return None

    def store(self, target_config: TargetConfig):
        # Implement storing logic if needed
        logger.info("Storing data")
        pass
