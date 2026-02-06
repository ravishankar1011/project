import dataclasses
from datetime import datetime
from typing import Optional
from enum import Enum


@dataclasses.dataclass
class PotDetails:
    pot_name: Optional[str]
    goal_amount: Optional[float]
    goal_date: Optional[datetime]


class Frequency(str, Enum):
    DAILY = "Daily"
    WEEKLY = "Weekly"
    MONTHLY = "Monthly"
    QUARTERLY = "Quarterly"


class MakePayment(str, Enum):
    ONCE = "Once"
    TWICE = "Twice"
    THRICE = "Thrice"
    CUSTOM = "Custom"
    UNTIL_STOPPED = "Until Stopped"


@dataclasses.dataclass()
class Schedule:
    frequency: Optional[Frequency]
    amount: Optional[float]
    start_date: Optional[datetime]
    make_payment: Optional[MakePayment]
    preview_button: Optional[str]
    save_button: Optional[str]
    bundle_schedule: Optional[bool]
#     schedule table


class AddressOption(str, Enum):
    HOME = "Home"
    WORK = "Work"


@dataclasses.dataclass
class Address:
    Option: AddressOption
    line1: str
    line2: str
    city: str
    postal_code: int
    province: str


class CardOrder:
    name_on_card: str
    address: Address
