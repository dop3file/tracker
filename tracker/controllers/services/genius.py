import asyncio
import aiohttp

import controllers.services.utils
from schemas.service_schemas import GeniusArtist
import config as config
from exceptions import SearchInvalidException


class Genius:
    PAGE_LIMIT = 20
    FEATURE_SYMBOLS = [",", "&"]

    def __init__(self, genius_token: str) -> None:
        self._token = genius_token
        self.default_request_params = {
            'access_token': self._token
        }
        
    def is_featured_artist(self, artist_name: str) -> bool:
        for feature_symbol in Genius.FEATURE_SYMBOLS:
            if feature_symbol in artist_name:
                return True
        return False


    async def get_artist_id(self, artist_name: str) -> int:
        async with aiohttp.ClientSession() as session:
            url = "http://api.genius.com/search"
            request_params = self.default_request_params
            request_params['q'] = artist_name
            async with session.get(url=url, params=request_params) as response:
                data = await response.json()
                if data["meta"]["status"] != 200:
                    raise SearchInvalidException("Invalid search query")
                
                hits = data["response"]["hits"]

                # ищем hit без feature_artist
                hit_without_feature = None
                for hit in hits:
                    if not hit["result"]["featured_artists"] and not self.is_featured_artist(hit["result"]["primary_artist"]["name"]):
                        hit_without_feature = hit
                        break
                else:
                    try:
                        hit_without_feature = hits[0]
                    except IndexError:
                        raise SearchInvalidException("Invalid search query")

                artist_id = hit_without_feature["result"]["primary_artist"]["id"]
                return artist_id

    async def get_artist(self, artist_id: int) -> GeniusArtist:
        async with aiohttp.ClientSession() as session:
            url = f"http://api.genius.com/artists/{artist_id}"
            async with session.get(url=url, params=self.default_request_params) as response:
                data = await response.json()
                if data["meta"]["status"] != 200:
                    raise SearchInvalidException("Invalid search query")
                
                artist: dict = data["response"]["artist"]
                if artist["image_url"].startswith('https://assets.genius.com/images/default_avatar'):
                    raise SearchInvalidException("Invalid search query")
                artist = GeniusArtist.parse_obj(artist)
                return artist
 





