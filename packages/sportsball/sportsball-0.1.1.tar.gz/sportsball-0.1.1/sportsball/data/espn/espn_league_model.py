"""ESPN league model."""

from typing import Any, Iterator

import requests

from ..game_model import GameModel
from ..league import League
from ..league_model import LeagueModel
from ..season_type import SeasonType
from .espn_game_model import create_espn_game_model


def _season_type_from_name(name: str) -> SeasonType:
    if name == "Regular Season":
        return SeasonType.REGULAR
    if name == "Preseason":
        return SeasonType.PRESEASON
    if name == "Postseason":
        return SeasonType.POSTSEASON
    if name == "Off Season":
        return SeasonType.OFFSEASON
    raise ValueError(f"Unrecognised season name: {name}")


class ESPNLeagueModel(LeagueModel):
    """ESPN implementation of the league model."""

    def __init__(
        self, start_url: str, league: League, session: requests.Session
    ) -> None:
        super().__init__(league, session)
        self._start_url = start_url

    def _produce_games(
        self, week: dict[str, Any], week_count: int, season_type_json: dict[str, Any]
    ) -> Iterator[GameModel]:
        events_page = 1
        events_count = 0
        while True:
            if "events" not in week:
                break
            events_response = self.session.get(
                week["events"]["$ref"] + f"&page={events_page}"
            )
            events = events_response.json()
            for event_item in events["items"]:
                event_response = self.session.get(event_item["$ref"])
                event_response.raise_for_status()
                event = event_response.json()
                yield create_espn_game_model(
                    event,
                    week_count,
                    events_count,
                    self.session,
                    self.league,
                    season_type_json["year"],
                    _season_type_from_name(season_type_json["name"]),
                )
                events_count += 1
            if events_page >= events["pageCount"]:
                break
            events_page += 1

    def _produce_week_games(
        self, season_type_json: dict[str, Any], page: int
    ) -> Iterator[GameModel]:
        game_page = 1
        week_count = 0
        while True:
            weeks_response = self.session.get(
                season_type_json["weeks"]["$ref"] + f"&page={page}"
            )
            weeks_response.raise_for_status()
            weeks = weeks_response.json()
            for item in weeks["items"]:
                week_response = self.session.get(item["$ref"])
                week_response.raise_for_status()
                week = week_response.json()
                yield from self._produce_games(week, week_count, season_type_json)
                week_count += 1
            if game_page >= weeks["pageCount"]:
                break
            game_page += 1

    @property
    def games(self) -> Iterator[GameModel]:
        page = 1
        while True:
            response = self.session.get(self._start_url + f"&page={page}")
            response.raise_for_status()
            seasons = response.json()
            for item in seasons["items"]:
                season_response = self.session.get(item["$ref"])
                season_response.raise_for_status()
                season_json = season_response.json()

                for season_item in season_json["types"]["items"]:
                    season_type_response = self.session.get(season_item["$ref"])
                    season_type_response.raise_for_status()
                    season_type_json = season_type_response.json()

                    yield from self._produce_week_games(season_type_json, page)

            if page >= seasons["pageCount"]:
                break
            page += 1
