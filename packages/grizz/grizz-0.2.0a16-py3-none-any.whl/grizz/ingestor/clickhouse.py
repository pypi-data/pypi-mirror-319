r"""Contain the implementation of a clickhouse ingestor."""

from __future__ import annotations

__all__ = ["ClickHouseIngestor"]

import logging
from typing import TYPE_CHECKING, Any

import polars as pl
from coola import objects_are_equal
from iden.utils.time import timeblock

from grizz.ingestor.base import BaseIngestor
from grizz.utils.factory import setup_object
from grizz.utils.format import human_byte
from grizz.utils.imports import check_clickhouse_connect, check_pyarrow

if TYPE_CHECKING:
    from grizz.utils.imports import is_clickhouse_connect_available

    if is_clickhouse_connect_available():
        import clickhouse_connect


logger = logging.getLogger(__name__)


class ClickHouseIngestor(BaseIngestor):
    r"""Implement a clickhouse DataFrame ingestor.

    This ingestor requires ``clickhouse_connect`` and ``pyarrow``.

    Args:
        query: The query to get the data.
        client: The clickhouse client or its configuration.
            Please check the documentation of
            ``clickhouse_connect.get_client`` to get more information.

    Example usage:

    ```pycon

    >>> from grizz.ingestor import ClickHouseIngestor
    >>> import clickhouse_connect
    >>> client = clickhouse_connect.get_client()  # doctest: +SKIP
    >>> ingestor = ClickHouseIngestor(query="", client=client)  # doctest: +SKIP
    >>> frame = ingestor.ingest()  # doctest: +SKIP

    ```
    """

    def __init__(self, query: str, client: clickhouse_connect.driver.Client | dict) -> None:
        check_clickhouse_connect()
        check_pyarrow()
        self._query = str(query)
        self._client: clickhouse_connect.driver.Client = setup_object(client)

    def __repr__(self) -> str:
        return f"{self.__class__.__qualname__}()"

    def equal(self, other: Any, equal_nan: bool = False) -> bool:
        if not isinstance(other, self.__class__):
            return False
        return self._query == other._query and objects_are_equal(
            self._client, other._client, equal_nan=equal_nan
        )

    def ingest(self) -> pl.DataFrame:
        logger.info(
            f"Ingesting data from clickhouse... \n\n"
            "---------------------------------------------------------------------------------\n"
            f"query:\n{self._query}\n"
            "---------------------------------------------------------------------------------\n\n"
        )
        with timeblock("DataFrame ingestion time: {time}"):
            frame = pl.from_arrow(self._client.query_arrow(query=self._query))
            frame = frame.select(sorted(frame.columns))
            logger.info(
                f"DataFrame ingested | shape={frame.shape}  "
                f"estimated size={human_byte(frame.estimated_size())}"
            )
        logger.info(f"number of unique column names: {len(set(frame.columns)):,}")
        return frame
