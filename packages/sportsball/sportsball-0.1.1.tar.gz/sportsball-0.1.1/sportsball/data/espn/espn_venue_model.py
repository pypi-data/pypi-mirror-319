"""ESPN venue model."""

import datetime
from typing import Any

import requests

from ...cache import MEMORY
from ..google.google_address_model import create_google_address_model
from ..venue_model import VenueModel


@MEMORY.cache(ignore=["session"])
def create_espn_venue_model(
    venue: dict[str, Any], session: requests.Session, dt: datetime.datetime
) -> VenueModel:
    """Create a venue model from an ESPN result."""
    identifier = venue["id"]
    name = venue["fullName"]
    venue_address = venue["address"]
    city = venue_address.get("city", "")
    state = venue_address.get("state", "")
    zipcode = venue_address.get("zipCode", "")
    address = create_google_address_model(
        " - ".join([x for x in [name, city, state, zipcode] if x]),
        session,
        dt,
    )
    grass = venue["grass"]
    indoor = venue["indoor"]
    return VenueModel(
        identifier=identifier,
        name=name,
        address=address,  # pyright: ignore
        is_grass=grass,
        is_indoor=indoor,
    )
