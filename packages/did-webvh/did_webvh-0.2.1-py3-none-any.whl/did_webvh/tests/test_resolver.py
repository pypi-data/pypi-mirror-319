from contextlib import asynccontextmanager

from did_webvh.core.resolver import ResolutionResult
from did_webvh.resolver import resolve_did


@asynccontextmanager
async def error_resolver(url: str):
    raise ValueError("resolution error")
    yield  # necessary for generator


async def test_resolve_did_failed_request():
    # Fail due to connection error
    result = await resolve_did(
        "did:webvh:QmWtQu5Vwi5n7oTz1NHKPtRJuBQmNneLXBGkQW9YBaGYk4:example.com%3A5000",
        resolve_url=error_resolver,
    )
    assert isinstance(result, ResolutionResult)
    assert result.resolution_metadata["error"] is not None
