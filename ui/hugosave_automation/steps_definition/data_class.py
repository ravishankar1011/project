from dataclasses import dataclass
from typing import Optional

@dataclass
class SignupData:
    casual_name: str
    legal_name: str
    email: str
    passcode: str

@dataclass
class ScheduleData:
    frequency: str
    week: str
    day: str
    amount: float

@dataclass
class PayeeDetails:
   payee_name: Optional[str]
   bank_name:Optional[str]
   account_no:Optional[str]

@dataclass
class UserDetails:
    casual_name: Optional[str]
    legal_name: Optional[str]
    email: Optional[str]
    tick_check_box: Optional[bool]

@dataclass
class Passcode:
   passcode_field1: Optional[str]
   passcode_field2:Optional[str]
