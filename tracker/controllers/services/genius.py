import asyncio
import os

import aiohttp
from collections import Counter

from bs4 import BeautifulSoup

from schemas.service_schemas import GeniusArtist
import config as config
from exceptions import SearchInvalidException


class GeniusAPI:
    FEATURE_SYMBOLS = [",", "&"]

    def __init__(self, access_token: str) -> None:
        self._token = access_token
        self.default_request_params = {
            'access_token': self._token
        }

    def is_featured_artist(self, artist_name: str) -> bool:
        for feature_symbol in GeniusAPI.FEATURE_SYMBOLS:
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


class GeniusParser:
    async def get_track_links(self, artist_page_url: str) -> list[str]:
        async with aiohttp.ClientSession() as session:
            links = []
            async with session.get(artist_page_url) as response:
                soup = BeautifulSoup(await response.text(), "lxml")
                for track in soup.find_all(class_="mini_card_grid-song"):
                    link = track.find("a", class_="mini_card", href=True)
                    links.append(link.get('href'))
        return links

    async def parse_text(self, track_url: str) -> list[str]:
        async with aiohttp.ClientSession() as session:
            all_strings = []
            async with session.get(track_url) as response:
                soup = BeautifulSoup(await response.text(), "lxml")
                text = soup.find(class_="Lyrics__Container-sc-1ynbvzw-5")
                for string in text:
                    if string.text and self.validate_text_string(string.text):
                        formated_string = self.format_string(string.text)
                        if formated_string:
                            all_strings.append(formated_string)
            return all_strings

    def validate_text_string(self, string: str) -> bool:
        ban_chars = ['[', '<']
        for char in ban_chars:
            if char in string:
                return False
        return True

    def format_string(self, string: str) -> str:
        return string.replace('(', '').replace(')', '').replace(',', '').replace('.', '')


def get_most_popular_words(tracks_text: list[list[str]]) -> list:
    all_texts: list[str] = [track for track in tracks_text for track in track]
    all_words = []
    for string in all_texts:
        for word in string.split(' '):
            if len(word) >= 5:
                all_words.append(word)
    counter = Counter(all_words)
    return [word[0] for word in counter.most_common(15)]



