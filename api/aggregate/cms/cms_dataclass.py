import dataclasses
from datetime import datetime
from typing import Optional


@dataclasses.dataclass
class DevDepositRequestDTO:
    account_type: str
    amount: float
    currency: str
    purpose: Optional[str]
    customer_profile_id: Optional[str]

    def get_dict(self, customer_profile_id):
        return {
            "account_type": self.account_type,
            "amount": self.amount,
            "currency": self.currency,
            "customer_profile_id": customer_profile_id,
        }


@dataclasses.dataclass
class ProductDTO:
    product_id: Optional[str]
    product_code: Optional[str]
    product_name: Optional[str]
    product_class: Optional[str]
    product_type: Optional[str]
    profile_type: Optional[str]
    product_category: Optional[str]
    description: Optional[str]
    param_group: Optional[str]

    def get_dict(self, product_code):
        return {
            "product_id": self.product_id,
            "product_name": self.product_name,
            "product_type": self.product_type,
            "description": self.description,
            "product_code": product_code,
            "product_class": self.product_class,
            "profile_type": self.profile_type,
            "product_category": self.product_category,
            "param_group": self.param_group,
        }


@dataclasses.dataclass
class ProductIdDTO:
    product_id: Optional[str]
    expected_status_code: Optional[str]

    def get_dict(self):
        return {"product_id": self.product_id, "status_code": self.expected_status_code}


@dataclasses.dataclass
class UpdateProductDTO:
    product_id: str
    product_code: Optional[str] = None
    product_name: Optional[str] = None
    product_description: Optional[str] = None
    product_class: Optional[str] = None
    profile_type: Optional[str] = None
    param_group: Optional[str] = None
    expected_status_code: Optional[str] = None

    def get_dict(self):
        return {k: v for k, v in self.__dict__.items() if v is not None}


@dataclasses.dataclass
class CreateLoanAccountRequestDTO:
    end_customer_profile_id: Optional[str]
    account_id: Optional[str]
    product_id: Optional[str]
    approved_amount: Optional[float]
    tenure: Optional[int]
    interest_rate: Optional[float]
    beneficiary_account: Optional[str]

    def get_dict(self):
        return {
            "end_customer_profile_id": self.end_customer_profile_id,
            "product_id": self.product_id,
            "approved_amount": self.approved_amount,
            "tenure": self.tenure,
            "interest_rate": self.interest_rate,
        }

@dataclasses.dataclass
class LoanDisbursementRequestDTO:
    loan_account_id: str
    amount: float
    currency: str
    txn_code: str

    def get_dict(self, loan_account_id):
        return {
            "loan_account_id": loan_account_id,
            "amount": self.amount,
            "currency": self.currency,
            "txn_code": self.txn_code,
        }

@dataclasses.dataclass
class CreateCreditAccountRequestDTO:
    end_customer_profile_id: str
    account_id: Optional[str]
    product_id: str
    country: Optional[str]
    currency: Optional[str]
    approved_limit: float
    interest_rate: float
    los_journey_code: Optional[str]
    los_application_id: Optional[str]

    # Only add values that would be sent to create object using REST call
    def get_dict(self):
        return {
            "end_customer_profile_id": self.end_customer_profile_id,
            "product_id": self.product_id,
            "currency": self.currency,
            "country": self.country,
            "approved_limit": self.approved_limit,
            "interest_rate": self.interest_rate,
            "los_journey_code": self.los_journey_code,
            "los_application_id": self.los_application_id,
        }


@dataclasses.dataclass
class AttachCardRequest:
    customer_profile_id: Optional[str]
    account_id: Optional[str]
    status: Optional[str]


@dataclasses.dataclass
class TransactionRequest:
    transaction_id: str
    account_id: str
    currency: str
    transaction_amount: float
    metadata: dict
    status_code: str
    status: str

    def get_dict(self, credit_account_id, sub_txn_type, card_txn_type=None, advice=False):
        data = {
            "credit_account_id": credit_account_id,
            "amount": self.transaction_amount,
            "currency": self.currency,
            "purpose": "random_str_here",
            "metadata": self.metadata,
            "sub_txn_type": sub_txn_type,
            "advice": advice
        }

        if card_txn_type is not None:
            data["card_transaction_type"] = card_txn_type

        return data


@dataclasses.dataclass
class ClearTransactionRequest:
    transaction_id: str
    group_id: str
    clearing_amount: float
    status_code: str
    status: str

    # Only add values that would be sent to create object using REST call
    def get_dict(self):
        return {
            "group_id": self.group_id,
            "amount": self.clearing_amount,
            "metadata": {"some-random": "value"},
        }


@dataclasses.dataclass
class UpdateTransactionRequest:
    transaction_id: str
    account_id: str
    advice: bool
    updated_txn_amount: float
    status_code: str
    status: str

    # Only add values that would be sent to create object using REST call
    def get_dict(self):
        return {"updated_amount": self.updated_txn_amount}


@dataclasses.dataclass
class RevertTransactionRequest:
    transaction_id: str
    customer_profile_id: Optional[str]
    metadata: Optional[str]
    status_code: str
    status: str
    refund: bool

    def get_dict(self):
        return {
            "transaction_id": self.transaction_id,
            "customer_profile_id": self.customer_profile_id,
            "metadata": {"some-random": "value"},
        }


@dataclasses.dataclass
class DebitSettlementDTO:
    clearing_group_id: str
    cumulative_amount: float
    external_ref: str
    settlement_account_detail: str
    status_code: str
    status: str

    def get_dict(self, customer_profile_id, clearing_group_id, settlement_account_detail):
        return {
            "clearing_group_id": clearing_group_id,
            "settlement_account_detail": settlement_account_detail,
            "cumulative_amount": self.cumulative_amount,
            "external_ref": self.external_ref,
            "customer_profile_id": customer_profile_id,
        }


@dataclasses.dataclass
class ReconcileClearingRequest:
    group_id: str
    total_amount: float
    txn_count: int


@dataclasses.dataclass
class SendRequest:
    group_id: str
    total_amount: float
    status_code: str
    transaction_status: str

    def get_dict(self):
        return {"total_amount": self.total_amount}


@dataclasses.dataclass
class AuthorizationDTO:
    transaction_id: str
    message_type: str
    account_id: str
    amount: float
    currency: str
    metadata: dict
    status_code: str
    status: str
    transaction_code: str

    def get_dict(self, credit_account_id):
        return {
            "account_id": credit_account_id,
            "message_type": self.message_type,
            "amount": self.amount,
            "currency": self.currency,
            "metadata": self.metadata,
            "transaction_code": self.transaction_code,
        }


@dataclasses.dataclass
class AuthorizationUpdateDTO:
    transaction_id: str
    message_type: str
    account_id: str
    amount: float
    metadata: dict
    status_code: str
    status: str

    def get_dict(self, credit_account_id, transaction_id):
        return {
            "account_id": credit_account_id,
            "transaction_id": transaction_id,
            "message_type": self.message_type,
            "amount": self.amount,
            "status": self.status,
            "metadata": self.metadata,
            "status": self.status
        }


@dataclasses.dataclass
class ClearingRequestDTO:
    transaction_id: str
    clearing_group_id: str
    amount: float
    status_code: str
    status: str

    # Only add values that would be sent to create object using REST call
    def get_dict(self):
        return {
            "transaction_id: str": self.transaction_id,
            "clearing_group_id": self.clearing_group_id,
            "amount": self.amount,
        }


@dataclasses.dataclass
class ContextParams:
    customer_profile_id: str
    product_id: str
    end_customer_profile_id: str


@dataclasses.dataclass
class DevTransaction:
    txn_time: str
    txn_type: str
    txn_code: str
    amount: float

    def get_dict(self):
        print(self.txn_time + datetime.now().strftime("T%H:%M:%S.%fZ"))
        return {
            "txn_time": self.txn_time + datetime.now().strftime("T%H:%M:%S.%fZ"),
            "txn_type": self.txn_type,
            "txn_code": self.txn_code,
            "amount": self.amount,
            "category": 1,
        }


@dataclasses.dataclass
class TransactionRequestDTO:
    credit_account_id: str
    amount: float
    txn_code: str
    currency: str
    receiver: Optional[str]

    def get_dict(self, receiver, account_id):
        return {
            "credit_account_id": account_id,
            "amount": self.amount,
            "txn_code": self.txn_code,
            "currency": self.currency,
            "receiver": receiver,
        }


@dataclasses.dataclass
class CreateTransactionLimitDTO:
    product_id: str
    limit_code: str
    limit_description: str
    rule_group: Optional[str]

    def get_dict(self, rule_group, product_id):
        return {
            "product_id": product_id,
            "limit_code": self.limit_code,
            "limit_description": self.limit_description,
            "rule_group": rule_group
        }


@dataclasses.dataclass
class VerifyCardAttachableRequestDTO:
    customer_profile_id: Optional[str]
    account_id: Optional[str]
    status: Optional[str]


@dataclasses.dataclass
class DetachCardRequest:
    account_id: str
    status: str
    status_code: str


@dataclasses.dataclass
class CreateTransactionEMIRequest:
    transaction_id: Optional[str]
    credit_account_id: str
    interest_rate: float
    tenure: int

    def get_dict(self, transaction_id, credit_account_id):
        return {
            "transaction_id": transaction_id,
            "credit_account_id": credit_account_id,
            "interest_rate": self.interest_rate,
            "tenure": self.tenure,
        }

@dataclasses.dataclass
class CreateFeeRequest:
    product_id: str
    fee_code: str
    txn_code: str
    rule_group: str
    fee_type: str
    push_overdraft: bool
    fee_details: str

    def get_dict(self, rule_group, product_id, fee_details):
        return {
            "product_id": product_id,
            "fee_code": self.fee_code,
            "txn_code": self.txn_code,
            "rule_group": rule_group,
            "fee_type": self.fee_type,
            "push_overdraft": self.push_overdraft,
            "fee_details": fee_details
        }

@dataclasses.dataclass
class CreateTaxRequest:
    tax_id: str
    product_id: str
    tax_code: str
    txn_code: str
    rule_group: str
    push_overdraft: bool

    def get_dict(self, rule_group, product_id):
        return {
            "product_id": product_id,
            "tax_code": self.tax_code,
            "txn_code": self.txn_code,
            "rule_group": rule_group,
            "push_overdraft": self.push_overdraft,
        }

@dataclasses.dataclass
class UpdateTaxRequest:
    tax_id: str
    tax_code: str
    txn_code: str
    rule_group: str
    push_overdraft: bool

    def get_dict(self, rule_group):
        return {
            "tax_code": self.tax_code,
            "txn_code": self.txn_code,
            "rule_group": rule_group,
            "push_overdraft": self.push_overdraft,
        }
