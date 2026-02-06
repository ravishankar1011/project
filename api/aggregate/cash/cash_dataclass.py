import dataclasses
from dataclasses import field
from enum import Enum
from typing import Optional, List, Dict

@dataclasses.dataclass
class CreateCustomerProfileCashWalletDTO:
    identifier: Optional[str]
    cash_wallet_id: Optional[str]
    customer_profile_id: str
    product_id: Optional[str]
    on_behalf_of: Optional[str]
    metadata: Optional[dict]
    cash_account_id: Optional[str] = ""

    # Only add values that would be sent to create an object using REST call
    def get_dict(self):
        return {
            "customer_profile_id": self.customer_profile_id,
            "product_id": self.product_id,
            "on_behalf_of": self.on_behalf_of,
            "metadata": self.metadata,
            "cash_account_id": self.cash_account_id,
        }


@dataclasses.dataclass
class ProductRequestDTO:
    identifier: Optional[str]
    product_code: Optional[str]
    product_name: Optional[str]
    provider_id: Optional[str]
    profile_type: str
    product_class: str
    product_type: str
    currency: Optional[str]
    country: Optional[str]
    minimum_balance_limit: Optional[float]
    minimum_balance_policy: Optional[str]
    max_active_cash_wallets: Optional[int] = 1
    primary_currency: Optional[str] = 'SGD'
    supported_currencies: Optional[str] = 'SGD'

    # Only add values that would be sent to create an object using REST call
    def get_dict(self):
        return {
            "product_code": self.product_code,
            "product_name": self.product_name,
            "profile_type": self.profile_type,
            "product_class": self.product_class,
            "product_type": self.product_type,
            "currency": self.currency,
            "country": self.country,
            "provider_id": self.provider_id,
            "max_active_cash_wallets": self.max_active_cash_wallets,
            "supported_currencies": self.supported_currencies,
            "primary_currency": self.primary_currency
        }


@dataclasses.dataclass
class CashAccountRequestDTO:
    cash_account_product_id: str
    end_customer_profile_id: Optional[str]

    def get_dict(self):
        return {
            "cash_account_product_id": self.cash_account_product_id,
            "end_customer_profile_id": self.end_customer_profile_id,
        }


@dataclasses.dataclass
class SGBank:
    swift_bic: str
    iban: Optional[str]
    account_number: Optional[str]

    def get_dict(self):
        return {
            "swift_bic": self.swift_bic,
            "iban": self.iban,
            "account_number": self.account_number,
        }


@dataclasses.dataclass
class BankCodeDetailsDTO:
    sg_code_details: Optional[SGBank]

    def get_dict(self):
        return {
            "sg_code_details": self.sg_code_details.get_dict()
        }


@dataclasses.dataclass
class BankAccountDetailsDTO:
    account_number: Optional[str]
    account_holder_name: Optional[str]
    bank_name: str
    currency: str
    country: str
    code_details: Optional[BankCodeDetailsDTO]

    def get_dict(self):
        return {
            "account_number": self.account_number,
            "account_holder_name": self.account_holder_name,
            "bank_name": self.bank_name,
            "currency": self.currency,
            "country": self.country,
            "code_details": self.code_details.get_dict()
        }


@dataclasses.dataclass
class CashWalletDTO:
    identifier: Optional[str]
    cash_wallet_id: Optional[str]
    customer_profile_id: Optional[str]
    end_customer_profile_id: Optional[str]
    cash_wallet_status: str
    cash_wallet_details: BankAccountDetailsDTO
    metadata: Optional[dict]

    @classmethod
    def sanitize_bank_account_dto(cls, expected_bank_acc_dto):
        other = dataclasses.replace(expected_bank_acc_dto)
        other.identifier = None
        other.cash_wallet_id = None
        other.on_behalf_of = None
        other.cash_wallet_details.account_holder_name = None
        other.cash_wallet_details.code_details = None
        other.cash_wallet_details.account_number = None
        return other


@dataclasses.dataclass
class CreateEndCustomerProfileCashWalletDTO:
    identifier: Optional[str]
    cash_wallet_id: Optional[str]
    customer_profile_id: Optional[str]
    end_customer_profile_id: Optional[str]
    provider_id: Optional[str]
    product_id: Optional[str]
    account_type_id: Optional[str]
    currency: str
    country: str
    in_trust: bool
    is_overdraft_allowed: Optional[bool]
    on_behalf_of: Optional[str]
    metadata: Optional[dict]
    cash_account_id: Optional[str] = ""

    # Only add values that would be sent to create object using REST call
    def get_dict(self):
        return {
            "customer_profile_id": self.customer_profile_id,
            "end_customer_profile_id": self.end_customer_profile_id,
            "provider_id": self.provider_id,
            "product_id": self.product_id,
            "account_type_id": self.account_type_id,
            "currency": self.currency,
            "country": self.country,
            "in_trust": self.in_trust,
            "is_overdraft_allowed": self.is_overdraft_allowed,
            "on_behalf_of": self.on_behalf_of,
            "metadata": self.metadata,
            "cash_account_id": self.cash_account_id,
        }


@dataclasses.dataclass
class InitiateTransactionRequestDTO:
    identifier: str
    amount: float
    currency: str
    purpose: str
    is_overdraft_allowed: bool
    metadata: dict
    sub_txn_type: str
    customer_profile_id: str
    idempotency_key: Optional[str]
    transfer_out_details: Optional[dict] = None
    cash_wallet_id: Optional[str] = ""
    cash_account_id: Optional[str] = ""

    def get_dict(self):
        result = {
            "amount": self.amount,
            "currency": self.currency,
            "purpose": self.purpose,
            "is_overdraft_allowed": self.is_overdraft_allowed,
            "metadata": self.metadata,
            "sub_txn_type": self.sub_txn_type,
            "transfer_out_details": self.transfer_out_details
        }
        if self.cash_wallet_id:
            result["cash_wallet_id"] = self.cash_wallet_id
        else:
            result["cash_account_id"] = self.cash_account_id
        return result


@dataclasses.dataclass
class UpdateTransactionRequestDTO:
    transaction_id: str
    amount: float
    is_overdraft_allowed: bool
    metadata: dict
    customer_profile_id: str

    def get_dict(self):
        return {
            "transaction_id": self.transaction_id,
            "amount": self.amount,
            "is_overdraft_allowed": self.is_overdraft_allowed,
            "metadata": self.metadata,
        }


@dataclasses.dataclass
class CancelTransactionRequestDTO:
    transaction_id: str
    metadata: dict
    purpose: str
    customer_profile_id: str

    def get_dict(self):
        return {
            "transaction_id": self.transaction_id,
            "purpose": self.purpose,
            "metadata": self.metadata,
        }


@dataclasses.dataclass
class CloseTransactionRequestDTO:
    transaction_id: str
    metadata: dict
    purpose: str
    customer_profile_id: str

    def get_dict(self):
        return {
            "transaction_id": self.transaction_id,
            "purpose": self.purpose,
            "metadata": self.metadata,
        }


@dataclasses.dataclass
class SettleTransactionRequestDTO:
    transaction_id: str
    amount: float
    is_overdraft_allowed: bool
    metadata: dict
    customer_profile_id: str
    transaction_rail: Optional[str]
    overdraft_funding_cash_wallet_id: Optional[str]
    idempotency_key: Optional[str] = None

    def get_dict(self):
        return {
            "transaction_id": self.transaction_id,
            "amount": self.amount,
            "transaction_rail": self.transaction_rail,
            "is_overdraft_allowed": self.is_overdraft_allowed,
            "metadata": self.metadata,
            "overdraft_funding_cash_wallet_id": self.overdraft_funding_cash_wallet_id,
            "purpose": "Integration_Test",
        }


@dataclasses.dataclass
class RefundRequestDTO:
    original_transaction_id: str
    customer_profile_id: str
    refund_amount: float
    purpose: str
    metadata: dict

    def get_dict(self):
        return {
            "refund_amount": self.refund_amount,
            "original_transaction_id": self.original_transaction_id,
            "purpose": self.purpose,
            "metadata": self.metadata,
        }


@dataclasses.dataclass
class CashDevDepositRequestDTO:
    identifier: str
    cash_wallet_id: Optional[str]
    cash_account_id: Optional[str]
    amount: Optional[float]
    purpose: str
    currency: str
    transaction_rail: Optional[str]
    metadata: Optional[dict]
    customer_profile_id: Optional[str]

    def get_dict(self):
        return {
            "cash_wallet_id": self.cash_wallet_id,
            "cash_account_id": self.cash_account_id,
            "amount": self.amount,
            "purpose": self.purpose,
            "currency": self.currency,
            "transaction_rail": self.transaction_rail,
            "metadata": self.metadata
        }

# Enums based on your protobuf definitions
@dataclasses.dataclass
class Class(Enum):
    CLASS_UNKNOWN = 0
    STANDARD = 1
    SHARIAH = 2


@dataclasses.dataclass
class ProductType(Enum):
    PRODUCT_TYPE_UNKNOWN = 0
    CASH_ACCOUNT = 1


# ParamRequestDTO.Value nested types
@dataclasses.dataclass
class IntegerList:
    value: int


@dataclasses.dataclass
class IntegerRange:
    value: int


@dataclasses.dataclass
class Integer:
    value: int

    def to_dict(self):
        return {"value": self.value}


@dataclasses.dataclass
class RangeIntegers:
    min_value: int
    max_value: int


@dataclasses.dataclass
class DoubleList:
    value: float

    def to_dict(self):
        return {"value": self.value}


@dataclasses.dataclass
class DoubleRange:
    value: float


@dataclasses.dataclass
class Double:
    value: float

    def to_dict(self):
        return {"value": self.value}


@dataclasses.dataclass
class StringList:
    value: str

    def to_dict(self):
        return {"value": self.value}


@dataclasses.dataclass
class String:
    value: str


@dataclasses.dataclass
class Boolean:
    value: bool

    def to_dict(self):
        return {"value": self.value}


@dataclasses.dataclass
class MultiInteger:
    values: List[int]


@dataclasses.dataclass
class MultiDouble:
    values: List[float]


@dataclasses.dataclass
class MultiString:
    values: List[str]

    def to_dict(self):
        return {"values": self.values}


@dataclasses.dataclass
class Timestamp:
    value: str


@dataclasses.dataclass
class Value:
    integer_list_value: Optional[IntegerList] = None
    integer_range_value: Optional[IntegerRange] = None
    integer_value: Optional[Integer] = None
    range_integers_value: Optional[RangeIntegers] = None
    double_list_value: Optional[DoubleList] = None
    double_range_value: Optional[DoubleRange] = None
    double_value: Optional[Double] = None
    string_list_value: Optional[StringList] = None
    string_value: Optional[String] = None
    boolean_value: Optional[Boolean] = None
    multi_integer_value: Optional[MultiInteger] = None
    multi_double_value: Optional[MultiDouble] = None
    multi_string_value: Optional[MultiString] = None
    timestamp_value: Optional[Timestamp] = None


@dataclasses.dataclass
class ParamRequestDTO:
    param_name: str
    value: Value
    metadata: Optional[Dict[str, str]] = field(default_factory=dict)

    def to_dict(self):
        def clean_dict(d):
            if isinstance(d, dict):
                return {k: clean_dict(v) for k, v in d.items() if v is not None}
            elif isinstance(d, list):
                return [clean_dict(i) for i in d if i is not None]
            elif hasattr(d, "to_dict"):
                return d.to_dict()
            elif hasattr(d, "value"):
                return d.value
            return d

        # Convert the ParamRequestDTO to a dictionary and clean None values
        return clean_dict(
            {
                "param_name": self.param_name,
                "value": clean_dict(
                    self.value.__dict__
                ),  # Clean nested Value dataclass
                "metadata": self.metadata,
            }
        )

@dataclasses.dataclass
class PayRequestDTO:
    amount: float
    purpose: str
    currency: str
    push_overdraft: bool
    source_account_id: Optional[String] = ''
    transfer_out_account_details: Optional[dict] = None

    def get_dict(self):
        return {
            "source_account_id": self.source_account_id,
            "amount": self.amount,
            "purpose": self.purpose,
            "currency": self.currency,
            "push_overdraft": self.push_overdraft,
            "transfer_out_account_details": self.transfer_out_account_details
        }


@dataclasses.dataclass
class FloatAccountResponseDTO:
    cash_account_id: str

    def get_dict(self):
        return {
            "cash_account_id": self.cash_account_id
        }

@dataclasses.dataclass
class ApplyFeeRequestDTO:
    amount: float
    currency: str
    push_overdraft: bool
    account_id: Optional[str]

    def get_dict(self):
        return {
            "amount": self.amount,
            "currency": self.currency,
            "push_overdraft": self.push_overdraft,
            "account_id": self.account_id
        }

@dataclasses.dataclass
class MandateRequestDTO:
    cash_wallet_id: str
    segment: str
    max_amount: float
    purpose: str
    metadata: Optional[dict]
    debtor_account_details: Optional[dict] = None

    def get_dict(self):
        return {
            "cash_wallet_id": self.cash_wallet_id,
            "debtor_account_details": self.debtor_account_details,
            "segment": self.segment,
            "max_amount": self.max_amount,
            "purpose": self.purpose,
            "metadate": self.metadata
        }


@dataclasses.dataclass
class MandateTransactionRequestDTO:
    mandate_id: str
    cash_wallet_id: str
    amount: float
    currency: str
    purpose: str
    transaction_rail: str
    txn_code: str
    metadata: dict

    def get_dict(self):
        return {
            "mandate_id": self.mandate_id,
            "cash_wallet_id": self.cash_wallet_id,
            "amount": self.amount,
            "currency": self.currency,
            "purpose": self.purpose,
            "transaction_rail": self.transaction_rail,
            "txn_code": self.txn_code,
            "metadate": self.metadata
        }

@dataclasses.dataclass
class DebitAuthRequestDTO:
    message_type : str
    amount : float
    currency : str
    metadata : dict
    account_id : Optional[str]

    def get_dict(self):
        return {
            "message_type": self.message_type,
            "account_id": self.account_id,
            "amount": self.amount,
            "currency": self.currency,
            "metadata": self.metadata
        }

@dataclasses.dataclass
class ClearingRequestDTO:
    transaction_id : str
    amount : float
    clearing_group_id : str

    def get_dict(self):
        return {
            "amount": self.amount,
            "transaction_id": self.transaction_id,
            "clearing_group_id": self.clearing_group_id
        }

@dataclasses.dataclass
class UnsolicitedClearingRequestDTO:
    amount : float
    clearing_group_id : str
    account_id : str
    currency : str
    metadata : Optional[dict]

    def get_dict(self):
        return {
            "amount": self.amount,
            "clearing_group_id": self.clearing_group_id,
            "account_id": self.account_id,
            "currency": self.currency,
            "metadata": self.metadata
        }

@dataclasses.dataclass
class DebitSettlementDTO:
    clearing_group_id : str
    cumulative_amount : float
    settlement_account_detail : Optional[dict]

    def get_dict(self):
        return {
            "clearing_group_id": self.clearing_group_id,
            "cumulative_amount": self.cumulative_amount,
            "settlement_account_detail": self.settlement_account_detail
        }
