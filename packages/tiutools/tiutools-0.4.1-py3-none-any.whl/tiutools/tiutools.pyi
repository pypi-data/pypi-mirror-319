from _typeshed import Incomplete
from collections.abc import Generator
from pydantic import BaseModel
from typing import Optional, Union

mod_logger: Incomplete
db: Incomplete

def download_transactions(appid: str, logger=..., date: Incomplete | None = ..., user: Incomplete | None = ..., use_test: bool = ...) -> str: ...
def alert(msg) -> None: ...
def sso_user(is_web: bool = ..., reset_user: bool = ..., logger: Incomplete | None = ...): ...

class Failed:
    order_id: int
    error: str
    person_id: int
    def __init__(self, order_id, error, person_id) -> None: ...

class Corrected:
    order_id: int
    orig_balance: float
    amount: float
    person_id: int
    def __init__(self, order_id, orig_balance, amount, person_id) -> None: ...

class PaymentResults:
    ok: Optional[list[str]]
    corrected: Optional[list[Corrected]]
    not_found: list[str]
    failed: Optional[list[Failed]]
    def __init__(self, ok, corrected, not_found, failed) -> None: ...

class Result:
    results: str
    def __init__(self, results) -> None: ...

class P2A:
    person_id: int
    activity_id: int
    def __init__(self, person_id, activity_id) -> None: ...

class ResultsAndData:
    results: PaymentResults
    data_for_correction_mails: list[P2A]
    def __init__(self, results, data_for_correction_mails) -> None: ...

class CheckPayments:
    db: Incomplete
    logger: Incomplete
    report_only: Incomplete
    in_test: Incomplete
    results: Incomplete
    logbook: str
    data: Incomplete
    data_for_correction_mails: Incomplete
    folder: Incomplete
    def __init__(self, db: Incomplete | None = ..., logger=..., report_only: bool = ..., folder: Incomplete | None = ..., in_test: bool = ...) -> None: ...
    def run(self) -> Union[Result, ResultsAndData]: ...
    def check(self, reader) -> None: ...
    def check_row(self, csv_row) -> None: ...

def tiu_ldap() -> Generator[Incomplete, None, Incomplete]: ...
def parentify(tel): ...
def ldap_search(search: Incomplete | None = ..., fields: Incomplete | None = ...): ...
def ldap_search_staff(): ...
def lookup_user(db, user) -> None: ...
def beheer_check_time_since(datafile): ...
def beheer_get_previous_corrections(): ...
def initials_to_initialsfield(db) -> None: ...

class SsoConfig(BaseModel):
    sso_fields: Incomplete
    def __init__(self, namespace: str = ..., default_url: Incomplete | None = ..., app_window: Incomplete | None = ..., reset_keys: bool = ..., **data) -> None: ...
    def get_values(self, app_window) -> None: ...
    def get_value(self, field) -> Optional[str]: ...
    def reset_keys(self) -> None: ...

class UserModel(BaseModel):
    memo: str
    geslacht: str
    voorletters: str
    voorvoegsels: str
    achternaam: str
    roepnaam: str
    straat: str
    nummer: str
    toevoeging_nummer: str
    aanvulling: str
    postcode: str
    woonplaats: str
    land: str
    telefoonnummer: str
    geboortedatum: str
    email: str
    def geslacht_check(cls, value): ...
    def postcode_not_empty(cls, value): ...
    def geboortedatum_separator(cls, value): ...
