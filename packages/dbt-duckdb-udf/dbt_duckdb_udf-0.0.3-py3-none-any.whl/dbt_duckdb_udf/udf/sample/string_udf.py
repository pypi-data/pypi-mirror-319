from typing import Any
import pyarrow as pa

from dbt_duckdb_udf.utils.utils import register_udf, log_error, get_logger

logger = get_logger(__file__)

def custom_function(x: Any) -> str:
    try:
        return len(x)
    except Exception as e:
        log_error(table="no", column="no", msg=e)

@register_udf("udf_str_len")
def udf_str_len(x: pa.lib.ChunkedArray) -> int:
    try:
        lengths = pa.array([custom_function(item.as_py()) for item in x])
        return lengths
    except Exception as e:
        log_error(table="no", column="no", msg=e)