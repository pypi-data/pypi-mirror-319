# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from .bulk.bulk import (
    BulkResource,
    AsyncBulkResource,
    BulkResourceWithRawResponse,
    AsyncBulkResourceWithRawResponse,
    BulkResourceWithStreamingResponse,
    AsyncBulkResourceWithStreamingResponse,
)
from ...._compat import cached_property
from .blank.blank import (
    BlankResource,
    AsyncBlankResource,
    BlankResourceWithRawResponse,
    AsyncBlankResourceWithRawResponse,
    BlankResourceWithStreamingResponse,
    AsyncBlankResourceWithStreamingResponse,
)
from ...._resource import SyncAPIResource, AsyncAPIResource
from .prompt_templates import (
    PromptTemplatesResource,
    AsyncPromptTemplatesResource,
    PromptTemplatesResourceWithRawResponse,
    AsyncPromptTemplatesResourceWithRawResponse,
    PromptTemplatesResourceWithStreamingResponse,
    AsyncPromptTemplatesResourceWithStreamingResponse,
)

__all__ = ["V0Resource", "AsyncV0Resource"]


class V0Resource(SyncAPIResource):
    @cached_property
    def blank(self) -> BlankResource:
        return BlankResource(self._client)

    @cached_property
    def bulk(self) -> BulkResource:
        return BulkResource(self._client)

    @cached_property
    def prompt_templates(self) -> PromptTemplatesResource:
        return PromptTemplatesResource(self._client)

    @cached_property
    def with_raw_response(self) -> V0ResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return the
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/evrimai/python-client#accessing-raw-response-data-eg-headers
        """
        return V0ResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> V0ResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/evrimai/python-client#with_streaming_response
        """
        return V0ResourceWithStreamingResponse(self)


class AsyncV0Resource(AsyncAPIResource):
    @cached_property
    def blank(self) -> AsyncBlankResource:
        return AsyncBlankResource(self._client)

    @cached_property
    def bulk(self) -> AsyncBulkResource:
        return AsyncBulkResource(self._client)

    @cached_property
    def prompt_templates(self) -> AsyncPromptTemplatesResource:
        return AsyncPromptTemplatesResource(self._client)

    @cached_property
    def with_raw_response(self) -> AsyncV0ResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return the
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/evrimai/python-client#accessing-raw-response-data-eg-headers
        """
        return AsyncV0ResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncV0ResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/evrimai/python-client#with_streaming_response
        """
        return AsyncV0ResourceWithStreamingResponse(self)


class V0ResourceWithRawResponse:
    def __init__(self, v0: V0Resource) -> None:
        self._v0 = v0

    @cached_property
    def blank(self) -> BlankResourceWithRawResponse:
        return BlankResourceWithRawResponse(self._v0.blank)

    @cached_property
    def bulk(self) -> BulkResourceWithRawResponse:
        return BulkResourceWithRawResponse(self._v0.bulk)

    @cached_property
    def prompt_templates(self) -> PromptTemplatesResourceWithRawResponse:
        return PromptTemplatesResourceWithRawResponse(self._v0.prompt_templates)


class AsyncV0ResourceWithRawResponse:
    def __init__(self, v0: AsyncV0Resource) -> None:
        self._v0 = v0

    @cached_property
    def blank(self) -> AsyncBlankResourceWithRawResponse:
        return AsyncBlankResourceWithRawResponse(self._v0.blank)

    @cached_property
    def bulk(self) -> AsyncBulkResourceWithRawResponse:
        return AsyncBulkResourceWithRawResponse(self._v0.bulk)

    @cached_property
    def prompt_templates(self) -> AsyncPromptTemplatesResourceWithRawResponse:
        return AsyncPromptTemplatesResourceWithRawResponse(self._v0.prompt_templates)


class V0ResourceWithStreamingResponse:
    def __init__(self, v0: V0Resource) -> None:
        self._v0 = v0

    @cached_property
    def blank(self) -> BlankResourceWithStreamingResponse:
        return BlankResourceWithStreamingResponse(self._v0.blank)

    @cached_property
    def bulk(self) -> BulkResourceWithStreamingResponse:
        return BulkResourceWithStreamingResponse(self._v0.bulk)

    @cached_property
    def prompt_templates(self) -> PromptTemplatesResourceWithStreamingResponse:
        return PromptTemplatesResourceWithStreamingResponse(self._v0.prompt_templates)


class AsyncV0ResourceWithStreamingResponse:
    def __init__(self, v0: AsyncV0Resource) -> None:
        self._v0 = v0

    @cached_property
    def blank(self) -> AsyncBlankResourceWithStreamingResponse:
        return AsyncBlankResourceWithStreamingResponse(self._v0.blank)

    @cached_property
    def bulk(self) -> AsyncBulkResourceWithStreamingResponse:
        return AsyncBulkResourceWithStreamingResponse(self._v0.bulk)

    @cached_property
    def prompt_templates(self) -> AsyncPromptTemplatesResourceWithStreamingResponse:
        return AsyncPromptTemplatesResourceWithStreamingResponse(self._v0.prompt_templates)
