"""URL Shortening API Integration Service."""

import logging
import httpx

logger = logging.getLogger(__name__)


class URLShortenerService:
    """Service class handling third-party API interactions with fallback options."""

    @staticmethod
    async def shorten_tinyurl(long_url: str) -> str:
        """Shorten URL via TinyURL API."""
        api_url = f"https://tinyurl.com/api-create.php?url={long_url}"
        async with httpx.AsyncClient(timeout=10.0) as client:
            response = await client.get(api_url)
            response.raise_for_status()
            return response.text.strip()

    @staticmethod
    async def shorten_isgd(long_url: str) -> str:
        """Fallback: Shorten URL via is.gd API."""
        api_url = "https://is.gd/create.php"
        params = {"format": "simple", "url": long_url}
        async with httpx.AsyncClient(timeout=10.0) as client:
            response = await client.get(api_url, params=params)
            response.raise_for_status()
            return response.text.strip()

    @classmethod
    async def shorten(cls, long_url: str) -> str:
        """Primary shorten handler with fallback strategy."""
        try:
            return await cls.shorten_tinyurl(long_url)
        except Exception as e:
            logger.warning(f"TinyURL failed: {e}. Retrying with is.gd...")
            try:
                return await cls.shorten_isgd(long_url)
            except Exception as ex:
                logger.error(f"Fallback shortener failed: {ex}")
                raise RuntimeError(
                    "All shortener services are currently unreachable."
                ) from ex
