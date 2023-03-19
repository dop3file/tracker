from datetime import datetime
from base64 import b64encode

import aiohttp
import asyncio

from schemas.service_schemas import SpotifyTrack, SpotifyTrackDetails, SpotifyArtist
from exceptions import SearchInvalidException


class SpotifyAPI:
    def __init__(self, access_token: str) -> None:
        self._token = access_token
        self.default_headers = {
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "	application/x-www-form-urlencoded"
        }

    async def get_artist_id(self, artist_name: str) -> int:
        async with aiohttp.ClientSession() as session:
            url = f"https://api.spotify.com/v1/search"
            params = {
                "q": artist_name,
                "type": "artist"
            }
            async with session.get(url=url, headers=self.default_headers, params=params) as response:
                response_json = await response.json()
                try:
                    artists = response_json['artists']
                except KeyError:
                    await self.refresh_token()
                    return await self.get_artist_id(artist_name)
                first_artist_id = artists['items'][0]['id']
                return first_artist_id

    async def get_artist(self, artist_id: int):
        async with aiohttp.ClientSession() as session:
            url = f"https://api.spotify.com/v1/artists/{artist_id}"
            async with session.get(url=url, headers=self.default_headers) as response:
                response_json = await response.json()
                try:
                    artist = SpotifyArtist(
                        name=response_json["name"],
                        genres=response_json["genres"],
                        followers_count=response_json["followers"]["total"],
                        avatar_photo=response_json["images"][0]["url"],
                        popularity=response_json["popularity"],
                    )
                    return artist
                except Exception as e:
                    raise SearchInvalidException

    async def get_artist_top_tracks(self, artist_id: int) -> list[SpotifyTrack]:
        async with aiohttp.ClientSession() as session:
            url = f"https://api.spotify.com/v1/artists/{artist_id}/top-tracks?market=ES"
            async with session.get(url=url, headers=self.default_headers) as response:
                response_json = await response.json(content_type=None)
                tracks = response_json["tracks"]
                tracks_items: list[SpotifyTrack] = [
                    SpotifyTrack(
                            id=track["id"],
                            title=track["name"],
                            release_date=track["album"]["release_date"],
                            cover_url=track["album"]["images"][0]["url"],
                            preview_url=track["preview_url"],
                            explicit=track["explicit"],
                            details=await self.get_track_details(track["id"])
                        ) for track in tracks[:10]
                ]
                return tracks_items

    async def get_track_details(self, track_id: str) -> SpotifyTrackDetails:
        async with aiohttp.ClientSession() as session:
            url = f"https://api.spotify.com/v1/audio-features/{track_id}"
            async with session.get(url=url, headers=self.default_headers) as response:
                response_json = await response.json(content_type=None)
                try:
                    track_details = SpotifyTrackDetails.parse_obj(response_json)
                    return track_details
                except Exception as excp:
                    print(excp)

    async def refresh_token(self):
        async with aiohttp.ClientSession() as session:
            url = f"https://accounts.spotify.com/api/token"
            data = {
                "grant_type": "refresh_token",
                "refresh_token": "AQC8go0eBcz7032k0cxHC9Y89zhGYk0zgcvYXP7tYpAX_kJUaJVAZWWXfQ-wGVgn2XxBh_WjZqp7od4PnrCiknp0OAIf-CbnvSYLN03uK4RFCc1h9Bo6Sl6KnQaHMJHe3Y4",
            }
            headers = {
                'Content-Type': 'application/x-www-form-urlencoded',
                'Authorization': 'Basic ODIzMzdhZGNlYzY5NDgzYWJhZjgwNTdlYzRjMDM2MzU6NzI3YTg0ZTQzMTgxNDdjMmEwYjY5MTRiOGU2ZmRjNzY='
            }
            async with session.post(url=url, headers=headers, data=data) as response:
                json = await response.json()
                print(json)
                self._token = json["access_token"]
                self.default_headers["Authorization"] = f"Bearer {self._token}"