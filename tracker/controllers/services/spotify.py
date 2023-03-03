from datetime import datetime

import aiohttp
import asyncio

from schemas.service_schemas import SpotifyTrack, SpotifyTrackDetails


class SpotifyAPI:
    def __init__(self, access_token: str) -> None:
        self._token = access_token
        self.default_headers = {
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "	application/x-www-form-urlencoded"
        }

    async def get_artist_id(self, artist_name) -> int:
        async with aiohttp.ClientSession() as session:
            url = f"https://api.spotify.com/v1/search"
            params = {
                "q": artist_name,
                "type": "artist"
            }
            async with session.get(url=url, headers=self.default_headers, params=params) as response:
                response_json = await response.json()
                try:
                    first_artist_id = response_json['artists']['items'][0]['id']
                    return first_artist_id
                except (KeyError, IndexError) as excp:
                    print(excp)

    async def get_artist_top_tracks(self, artist_id: int) -> list[SpotifyTrack]:
        async with aiohttp.ClientSession() as session:
            url = f"https://api.spotify.com/v1/artists/{artist_id}/top-tracks?market=ES"
            async with session.get(url=url, headers=self.default_headers) as response:
                response_json = await response.json(content_type=None)
                try:
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
                            ) for track in tracks[:5]
                    ]
                    return tracks_items
                except Exception as excp:
                    print(excp)

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
                "client_id": "82337adcec69483abaf8057ec4c03635",
                "refresh_token": self._token
            }
            async with session.get(url=url, headers=self.default_headers, data=data) as response:
                return await response.json()

# spotify = SpotifyAPI("")
# asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
# id = asyncio.run(spotify.get_artist_id("Markul"))
# track = asyncio.run(spotify.get_artist_top_tracks(id))
# print(asyncio.run(spotify.get_track_details(track[0].id)))