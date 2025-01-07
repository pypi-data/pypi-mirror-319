# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Dict, List, Union, Optional
from datetime import datetime
from typing_extensions import Required, Annotated, TypedDict

from .._utils import PropertyInfo

__all__ = ["IngestEventParam", "Units"]


class Units(TypedDict, total=False):
    input: int

    output: int


class IngestEventParam(TypedDict, total=False):
    category: Required[str]

    resource: Required[str]

    units: Required[Dict[str, Units]]

    csat_rating: Optional[int]

    end_to_end_latency_ms: Optional[int]

    event_timestamp: Annotated[Union[str, datetime, None], PropertyInfo(format="iso8601")]

    experience_id: Optional[str]

    experience_name: Optional[str]

    experience_properties: Optional[Dict[str, str]]

    http_status_code: Optional[int]

    limit_ids: Optional[List[str]]

    properties: Optional[Dict[str, str]]

    provider_prompt: Optional[str]

    provider_request_headers: Optional[Dict[str, List[str]]]

    provider_response: Optional[List[str]]

    provider_response_headers: Optional[Dict[str, List[str]]]

    provider_uri: Optional[str]

    provisioned_resource_name: Optional[str]

    request_tags: Optional[List[str]]

    time_to_first_token_ms: Optional[int]

    user_id: Optional[str]
