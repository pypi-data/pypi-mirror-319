# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import List, Union, Iterable
from datetime import datetime
from typing_extensions import Literal, Required, Annotated, TypedDict

from .._utils import PropertyInfo

__all__ = [
    "DatasetGetViewParams",
    "Filter",
    "FilterNumericCriteria",
    "FilterStringCriteria",
    "FilterTagsCriteria",
    "FilterTimeRangeCriteria",
]


class DatasetGetViewParams(TypedDict, total=False):
    dataset_file_id: Required[Annotated[str, PropertyInfo(alias="datasetFileId")]]
    """
    The ID of the (pinned) dataset file from which to retrieve content. Requests
    iterating over pages of results are recommended to use this pinned identifier
    after the first page in order to prevent any effects from a dataset changing
    between the queries.
    """

    dataset_id: Required[Annotated[str, PropertyInfo(alias="datasetId")]]
    """The ID of the dataset from which to retrieve content.

    When specified, gets data from the current file in the dataset.
    """

    filters: Required[Iterable[Filter]]

    after: int
    """Pagination: The index, by row-order, after which to query results."""

    limit: int
    """Pagination: The maximum number of results to return on this page."""

    order_by: Annotated[str, PropertyInfo(alias="orderBy")]
    """Column to order results by"""

    order_direction: Annotated[str, PropertyInfo(alias="orderDirection")]
    """Direction to order results ("asc" or "desc")"""

    use_datasets_service: Annotated[bool, PropertyInfo(alias="useDatasetsService")]


class FilterNumericCriteria(TypedDict, total=False):
    float_value: Required[Annotated[float, PropertyInfo(alias="floatValue")]]

    int_value: Required[Annotated[int, PropertyInfo(alias="intValue")]]

    operator: Required[
        Literal[
            "OPERATOR_UNSPECIFIED",
            "OPERATOR_EQUALS",
            "OPERATOR_NOT_EQUALS",
            "OPERATOR_GREATER_THAN",
            "OPERATOR_GREATER_THAN_OR_EQUAL",
            "OPERATOR_LESS_THAN",
            "OPERATOR_LESS_THAN_OR_EQUAL",
        ]
    ]


class FilterStringCriteria(TypedDict, total=False):
    operator: Required[
        Literal[
            "OPERATOR_UNSPECIFIED",
            "OPERATOR_EQUALS",
            "OPERATOR_NOT_EQUALS",
            "OPERATOR_CONTAINS",
            "OPERATOR_STARTS_WITH",
            "OPERATOR_ENDS_WITH",
        ]
    ]

    value: Required[str]


class FilterTagsCriteria(TypedDict, total=False):
    operator: Required[Literal["OPERATOR_UNSPECIFIED", "OPERATOR_HAS_ANY", "OPERATOR_HAS_ALL", "OPERATOR_HAS_NONE"]]

    tags: Required[List[str]]


class FilterTimeRangeCriteria(TypedDict, total=False):
    operator: Required[Literal["OPERATOR_UNSPECIFIED", "OPERATOR_BEFORE", "OPERATOR_AFTER", "OPERATOR_BETWEEN"]]

    timestamp: Required[Annotated[Union[str, datetime], PropertyInfo(format="iso8601")]]

    end_timestamp: Annotated[Union[str, datetime], PropertyInfo(alias="endTimestamp", format="iso8601")]


class Filter(TypedDict, total=False):
    column_name: Required[Annotated[str, PropertyInfo(alias="columnName")]]

    numeric_criteria: Required[Annotated[FilterNumericCriteria, PropertyInfo(alias="numericCriteria")]]

    string_criteria: Required[Annotated[FilterStringCriteria, PropertyInfo(alias="stringCriteria")]]

    tags_criteria: Required[Annotated[FilterTagsCriteria, PropertyInfo(alias="tagsCriteria")]]

    time_range_criteria: Required[Annotated[FilterTimeRangeCriteria, PropertyInfo(alias="timeRangeCriteria")]]
