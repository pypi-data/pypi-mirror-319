from datetime import datetime
from client.ds.checks import Check


class Settings:
    _instrument_type: str
    _region: str
    _universe: str
    _delay: int
    _decay: int
    _neutralization: str
    _truncation: float
    _pasteurization: str
    _unit_handling: str
    _nan_handling: str
    _language: str
    _visualization: bool


class Regular:
    _code: str
    _description: str | None
    _operator_count: int


class IS:
    _checks: list[Check]


class OS:
    _checks: list[Check]


class Pyramid:
    _name: str
    _multiplier: float


class Alpha:
    _id: str
    _type: str
    _author: str
    _settings: Settings
    _regular: Regular
    _date_created: datetime
    _date_submitted: datetime | None
    _date_modified: datetime
    _name: str | None
    _favorite: bool
    _hidden: bool
    _color: str | None
    _category: None
    _tags: list
    _classifications: list
    _grade: None
    _stage: str
    _status: str
    _is: IS
    _os: OS
    _train: None
    _test: None
    _prod: None
    _competitions: None
    _themes: None
    _pyramids: None
    _team: None
