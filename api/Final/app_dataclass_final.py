import dataclasses
from datetime import datetime
import json
from enum import Enum
from typing import Optional, List

import tests.api.distribute.app_helper as ah

# non prod
# hugosave_profile_id = "375d0aa6-dfe8-4e3d-8a0d-5d6dece088bc"

# dev
hugosave_profile_id = "07651956-706a-47f3-ac69-595b26cd60f8"


@dataclasses.dataclass
class OpenAccountDTO:
    user_profile_identifier: str
    legal_name: str
    name: Optional[str]
    email: str
    phone_number: str
    referral_code: Optional[str]
    status: str
    prefix_ph_num: Optional[str]
    org_id: Optional[str]
    account_type: str

    def get_dict(self):
        return {
            "legal_name": self.legal_name,
            "name": self.name,
            "email": self.email,
            "phone_number": self.phone_number,
            "referral_code": self.referral_code,
            "prefix_ph_num": self.prefix_ph_num,
            "account_type": self.account_type,
        }


@dataclasses.dataclass
class UserStatusDTO:
    user_profile_identifier: str
    status: str


@dataclasses.dataclass
class CreateMapDTO:
    user_profile_identifier: str
    name: str
    asset_allocation_details: str
    allocation_type: str
    goal_date: Optional[str]
    goal_amount: Optional[float]

    def get_dict(self):
        asset_allocation_details = json.loads(self.asset_allocation_details)
        asset_allocation_details = [
            {**a, "asset_id": ah.asset_ids[a["asset_id"]]}
            for a in asset_allocation_details
        ]

        data = {
            "name": ah.get_uuid() if self.name == "random" else self.name,
            "asset_allocation_details": asset_allocation_details,
            "allocation_type": self.allocation_type
        }

        if self.goal_date and self.goal_amount:
            data.update({"goal_date": self.goal_date})
            data.update({"goal_amount": self.goal_amount})

        return data



@dataclasses.dataclass
class InvestMapDTO:
    user_profile_identifier: str
    transaction_amount: float
    investment_amount: float
    fee_amount: float
    status_code: Optional[str]
    invalid_map: Optional[str]

    def get_dict(self):
        return {
            "transaction_amount": self.transaction_amount,
            "investment_amount": self.investment_amount,
            "fee_amount": self.fee_amount,
            "asset_rates": [],
        }


@dataclasses.dataclass
class WithdrawMapDTO:
    user_profile_identifier: str
    transaction_amount: float
    withdraw_amount: float
    fee_amount: float
    status_code: Optional[str]
    invalid_map: Optional[str]

    def get_dict(self):
        return {
            "transaction_amount": self.transaction_amount,
            "withdraw_amount": self.withdraw_amount,
            "fee_amount": self.fee_amount,
            "asset_rates": [],
        }


@dataclasses.dataclass
class UpdateMapDTO:
    user_profile_identifier: str
    name: str
    goal_date: str
    goal_amount: float
    invalid_map: Optional[str]
    status_code: str

    def get_dict(self):
        return {
            "name": self.name,
            "goal_date": self.goal_date,
            "goal_amount": self.goal_amount,
        }


@dataclasses.dataclass
class ScheduleMapInvest:
    map_id: str
    map_name: str
    map_type: str
    amount: str
    units: float
    payee_account_id: str
    map_category: str
    map_goal_amount: Optional[float]
    map_invested_amount: float

    def get_dict(self):
        return {
            "map_id": self.map_id,
            "map_name": self.map_name,
            "map_type": self.map_type,
            "amount": self.amount,
            "units": self.units,
            "payee_account_id": self.payee_account_id,
            "map_category": self.map_category,
            "map_goal_amount": self.map_goal_amount,
            "map_invested_amount": self.map_invested_amount,
        }

@dataclasses.dataclass
class ScheduleBillPaymentsInvest:
    bill_payee_id: str
    amount: float

    def get_dict(self):
        return {
            "bill_payee_id": self.bill_payee_id,
            "amount": self.amount
        }

@dataclasses.dataclass
class SchedulePayeePayments:
    payee_id: str
    amount: float

    def get_dict(self):
        return {
            "payee_id": self.payee_id,
            "amount": self.amount
        }

class Frequency(Enum):
    DAILY = 1
    WEEKLY = 2
    MONTHLY = 3


class WeekDay(Enum):
    WEEKDAY_UNKNOWN = 0
    WEEKDAY_MONDAY = 1
    WEEKDAY_TUESDAY = 2
    WEEKDAY_WEDNESDAY = 3
    WEEKDAY_THURSDAY = 4
    WEEKDAY_FRIDAY = 5


@dataclasses.dataclass
class CreateMapScheduleDTO:
    user_profile_identifier: Optional[str]
    schedule_identifier: Optional[str]
    frequency: str
    schedule_type: str
    product_code: str
    target_weekdays: str
    target_week: Optional[int]
    schedule_map_invest: Optional[ScheduleMapInvest]
    amount: Optional[float]

    def get_dict(self):
        return {
            "frequency": self.frequency,
            "schedule_type": self.schedule_type,
            "product_code": self.product_code,
            "target_weekdays": self.target_weekdays,
            "target_week": self.target_week,
            "schedule_map_invest": self.schedule_map_invest.get_dict(),
        }

@dataclasses.dataclass
class CreateBillPaymentsScheduleDTO:
    user_profile_identifier: Optional[str]
    schedule_identifier: Optional[str]
    frequency: str
    schedule_type: str
    product_code: str
    target_weekdays: str
    target_week: Optional[int]
    schedule_bill_payments: Optional[ScheduleBillPaymentsInvest]
    amount: Optional[float]

    def get_dict(self):
        return {
            "frequency": self.frequency,
            "schedule_type": self.schedule_type,
            "product_code": self.product_code,
            "target_weekdays": self.target_weekdays,
            "target_week": self.target_week,
            "schedule_bill_payments": self.schedule_bill_payments.get_dict(),
        }

@dataclasses.dataclass
class CreatePayPaymentsScheduleDTO:
    user_profile_identifier: Optional[str]
    schedule_identifier: Optional[str]
    frequency: str
    schedule_type: str
    product_code: str
    target_weekdays: str
    target_week: Optional[int]
    schedule_pay_payee: Optional[SchedulePayeePayments]
    amount: Optional[float]

    def get_dict(self):
        return {
            "frequency": self.frequency,
            "schedule_type": self.schedule_type,
            "product_code": self.product_code,
            "target_weekdays": self.target_weekdays,
            "target_week": self.target_week,
            "schedule_pay_payee": self.schedule_pay_payee.get_dict(),
        }

@dataclasses.dataclass
class UpdateMapScheduleDTO:
    user_profile_identifier: Optional[str]
    schedule_identifier: Optional[str]
    frequency: str
    schedule_type: str
    product_code: str
    target_weekdays: str
    target_week: Optional[int]
    schedule_map_invest: Optional[ScheduleMapInvest]
    amount: Optional[float]

    def get_dict(self):
        return {
            "frequency": self.frequency,
            "schedule_type": self.schedule_type,
            "product_code": self.product_code,
            "target_weekdays": self.target_weekdays,
            "target_week": self.target_week,
            "schedule_map_invest": self.schedule_map_invest.get_dict(),
        }

@dataclasses.dataclass
class MockTransactionRequestDTO:
    user_profile_identifier: Optional[str]
    transaction_permutation_name: str
    billing_amount: str
    is_foreign_txn: bool
    channel : Optional[str]

    def get_dict(self):
        data = {
            "transaction_permutation_name": self.transaction_permutation_name,
            "billing_amount": self.billing_amount,
            "is_foreign_txn": self.is_foreign_txn
        }
        if self.channel:
            data.update({"channel": self.channel})
        return data


@dataclasses.dataclass
class CreateUpdateBackwardScheduleDTO:
    action: str
    amount: int
    map_type: str
    target_day: int
    target_weekday: int

    def get_dict(self):
        return {
            "target_day": self.target_day,
            "target_weekday": self.target_weekday,
            "allocations": {},
        }


@dataclasses.dataclass
class SubmitOTPDTO:
    otp: str

    def get_dict(self):
        return {"otp": self.otp}


@dataclasses.dataclass
class UpdateScheduleStatusRequestDTO:
    action: str

    def get_dict(self):
        return {"action": self.action}


@dataclasses.dataclass
class ComplianceInitiateRequestDTO:
    compliance_type: str
    content_type: Optional[str]

    def get_dict(self):
        return {
            "compliance_type": self.compliance_type,
            "content_type": self.content_type,
        }


@dataclasses.dataclass
class ComplianceSubmitRequestDTO:
    compliance_id: str
    compliance_type: str
    document_type: str

    def get_dict(self):
        return {
            "compliance_id": self.compliance_id,
            "compliance_type": self.compliance_type,
            "document_type": self.document_type,
        }


@dataclasses.dataclass
class CreditAccountMockTxnRequestDTO:
    amount: float
    txn_type: str
    txn_code: Optional[str]
    category: Optional[str]
    txn_time: Optional[str]

    def get_dict(self):
        return {
            "amount": self.amount,
            "txn_type": self.txn_type,
            "txn_code": self.txn_code,
            "category": self.category,
            "txn_time": self.txn_time + datetime.now().strftime("T%H:%M:%S.%fZ"),
        }


@dataclasses.dataclass
class VerifyMobileNumberDTO:
    user_name: str
    user_name_type: str
    ph_prefix : Optional[str]

    def get_dict(self):
        return {
            "user_name": self.user_name,
            "user_name_type": self.user_name_type,
            "ph_prefix": self.ph_prefix,
        }


@dataclasses.dataclass
class CreateNewAccountDTO:
    legal_name: str
    name: str
    account_type: str
    referee: Optional[str]
    user_profile_identifier: str

    # status: str
    # org_id: Optional[str]

    def get_dict(self):
        return {
            "legal_name": self.legal_name,
            "name": self.name,
            "account_type": self.account_type,
            "referee": self.referee,
            "user_profile_identifier": self.user_profile_identifier,
        }


@dataclasses.dataclass
class TransferRequestDTO:
    user_profile_identifier: str
    amount: float
    primary_wallet_id: str
    secondary_wallet_id: str
    transfer_type: str

    def get_dict(self):
        return {
            "user_profile_identifier": self.user_profile_identifier,
            "amount": self.amount,
            "primary_wallet_id": self.primary_wallet_id,
            "secondary_wallet_id": self.secondary_wallet_id,
            "transfer_type": self.transfer_type
        }


@dataclasses.dataclass
class ListIntentDTO:
    user_profile_identifier: str
    product_code: str
    intent_type: str
    intent_status: str
    count: int
    view: str

    def get_dict(self):
        return {
            "user_profile_identifier": self.user_profile_identifier,
            "product_code": self.product_code,
            "intent_type": self.intent_type,
            "intent_status": self.intent_status,
            "count": self.count,
            "view": self.view
        }


@dataclasses.dataclass
class UpdateAutoTopupDTO:
    user_profile_identifier: str
    cash_wallet_id: str
    auto_topup_enabled: str
    trigger_amount: int
    topup_amount: int
    is_external: str
    funding_cash_wallet_id: Optional[str]

    def get_dict(self):
        return {
            "user_profile_identifier": self.user_profile_identifier,
            "cash_wallet_id": self.cash_wallet_id,
            "auto_topup_enabled": self.auto_topup_enabled,
            "trigger_amount": self.trigger_amount,
            "topup_amount": self.topup_amount,
            "is_external": self.is_external,
            "funding_cash_wallet_id": self.funding_cash_wallet_id
        }


@dataclasses.dataclass
class RangeValue:
    min_value: int
    max_value: int


@dataclasses.dataclass
class CardProductParamRequest:
    card_account_product_code: str
    card_design_config_code: str
    bin_config_code: str
    scheme: str
    number_of_active_physical_cards: int
    number_of_active_virtual_cards: int
    card_validity: int
    card_emboss_name_length: RangeValue
    allow_non_3ds_transactions: bool
    allow_card_not_present_transactions: bool
    initial_status_of_virtual_card: str
    instant_use: bool
    tap_and_pay: bool
    allowed_card_types: List[str] = dataclasses.field(default_factory=list)
    allowed_countries: List[str] = dataclasses.field(default_factory=list)
    allowed_card_channels: List[str] = dataclasses.field(default_factory=list)
    transaction_region: List[str] = dataclasses.field(default_factory=list)


@dataclasses.dataclass
class CardAccountProductParamRequest:
    create_funding_account: bool
    fund_provider: str
    fund_provider_product_code: str
    number_of_active_accounts: int
    number_of_physical_cards_per_account: int
    number_of_virtual_cards_per_account: int
    number_of_active_physical_cards_per_account: int
    number_of_active_virtual_cards_per_account: int


@dataclasses.dataclass
class OrderCreditCardDTO:
    credit_limit: float

    def get_credit_limit(self):
        return float(self.credit_limit)


@dataclasses.dataclass
class UpdateCardLimitDTO:
    limit_id: str
    value: float

    def get_limit_id(self):
        return self.limit_id

    def get_value(self):
        return float(self.value)

@dataclasses.dataclass
class GetChannelLimitHistoryDTO:
    limit_id: str

    def get_credit_limit_history(self):
        return self.limit_id

@dataclasses.dataclass
class UpdateCreditLimitDTO:
    credit_limit: float

    def get_updated_credit_limit(self):
        return float(self.credit_limit)

@dataclasses.dataclass
class CashAdvanceRequestDTO:
    cash_advance_amount: float

    def get_cash_advance_amount(self):
        return float(self.cash_advance_amount)
