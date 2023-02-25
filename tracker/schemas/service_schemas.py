from pydantic import BaseModel, HttpUrl, Field, EmailStr


class GeniusArtist(BaseModel):
    # general
    id: int 
    name: str
    alternative_names: list[str] | None

    # social
    instagram_name: str | None
    twitter_name: str | None
    followers_count: int

    # photo
    header_photo: str = Field(alias="header_image_url")
    avatar_photo: str = Field(alias="image_url")

