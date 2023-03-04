from difflib import SequenceMatcher
from exceptions import SearchInvalidException
from logger import Logger


logger = Logger()


def validate_artist_names(*artist_names: list[str]) -> None:
    for idx in range(len(artist_names)):
        equal_factor_artist_names = SequenceMatcher(None, artist_names[idx - 1], artist_names[idx]).ratio()
        logger.log_info(equal_factor_artist_names)
        if equal_factor_artist_names <= 0.2:
            raise SearchInvalidException("Invalid search query")


