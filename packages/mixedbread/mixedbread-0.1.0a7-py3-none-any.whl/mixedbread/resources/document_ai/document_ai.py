# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from ..._compat import cached_property
from ..._resource import SyncAPIResource, AsyncAPIResource
from .parse.parse import (
    ParseResource,
    AsyncParseResource,
    ParseResourceWithRawResponse,
    AsyncParseResourceWithRawResponse,
    ParseResourceWithStreamingResponse,
    AsyncParseResourceWithStreamingResponse,
)

__all__ = ["DocumentAIResource", "AsyncDocumentAIResource"]


class DocumentAIResource(SyncAPIResource):
    @cached_property
    def parse(self) -> ParseResource:
        return ParseResource(self._client)

    @cached_property
    def with_raw_response(self) -> DocumentAIResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return the
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/mixedbread-ai/mixedbread-python#accessing-raw-response-data-eg-headers
        """
        return DocumentAIResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> DocumentAIResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/mixedbread-ai/mixedbread-python#with_streaming_response
        """
        return DocumentAIResourceWithStreamingResponse(self)


class AsyncDocumentAIResource(AsyncAPIResource):
    @cached_property
    def parse(self) -> AsyncParseResource:
        return AsyncParseResource(self._client)

    @cached_property
    def with_raw_response(self) -> AsyncDocumentAIResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return the
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/mixedbread-ai/mixedbread-python#accessing-raw-response-data-eg-headers
        """
        return AsyncDocumentAIResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncDocumentAIResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/mixedbread-ai/mixedbread-python#with_streaming_response
        """
        return AsyncDocumentAIResourceWithStreamingResponse(self)


class DocumentAIResourceWithRawResponse:
    def __init__(self, document_ai: DocumentAIResource) -> None:
        self._document_ai = document_ai

    @cached_property
    def parse(self) -> ParseResourceWithRawResponse:
        return ParseResourceWithRawResponse(self._document_ai.parse)


class AsyncDocumentAIResourceWithRawResponse:
    def __init__(self, document_ai: AsyncDocumentAIResource) -> None:
        self._document_ai = document_ai

    @cached_property
    def parse(self) -> AsyncParseResourceWithRawResponse:
        return AsyncParseResourceWithRawResponse(self._document_ai.parse)


class DocumentAIResourceWithStreamingResponse:
    def __init__(self, document_ai: DocumentAIResource) -> None:
        self._document_ai = document_ai

    @cached_property
    def parse(self) -> ParseResourceWithStreamingResponse:
        return ParseResourceWithStreamingResponse(self._document_ai.parse)


class AsyncDocumentAIResourceWithStreamingResponse:
    def __init__(self, document_ai: AsyncDocumentAIResource) -> None:
        self._document_ai = document_ai

    @cached_property
    def parse(self) -> AsyncParseResourceWithStreamingResponse:
        return AsyncParseResourceWithStreamingResponse(self._document_ai.parse)
