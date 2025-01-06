"""AFL aussportsbetting game model."""

# pylint: disable=too-many-arguments
import datetime

import requests

from ....cache import MEMORY
from ...game_model import GameModel
from ...league import League
from .afl_aussportsbetting_team_model import \
    create_afl_aussportsbetting_team_model
from .afl_aussportsbetting_venue_model import \
    create_afl_aussportsbetting_venue_model


@MEMORY.cache(ignore=["session"])
def create_afl_aussportsbetting_game_model(
    dt: datetime.datetime,
    home_team: str,
    away_team: str,
    venue: str,
    session: requests.Session,
    home_points: float,
    away_points: float,
    home_odds: float,
    away_odds: float,
    league: League,
) -> GameModel:
    """Create a game model based off aus sports betting."""
    venue_model = create_afl_aussportsbetting_venue_model(venue, session, dt)
    home_team_model = create_afl_aussportsbetting_team_model(
        home_team, home_points, home_odds
    )
    away_team_model = create_afl_aussportsbetting_team_model(
        away_team, away_points, away_odds
    )
    return GameModel(
        dt=dt,
        week=None,
        game_number=None,
        venue=venue_model,
        teams=[home_team_model, away_team_model],  # pyright: ignore
        end_dt=None,
        attendance=None,
        league=league,
        year=None,
        season_type=None,
    )
