import random

from behave import *
import tests.api.distribute.app_helper as ah
from tests.api.distribute.app.hugosave_sg.app_dataclass import WeekDay, CreateBillPaymentsScheduleDTO
from tests.api.distribute.app.hugosave_sg.map_schedule_steps import get_schedule_bill_payments_data
from tests.util.common_util import check_status_distribute
from tests.ui.hugosave_automation.features.steps.data_class_parser import DataClassParser

use_step_matcher("re")


@Step(
    "I list out all the available operators for ([^']*) Bill Payment for the user ([^']*)"
)
def step_impl(context, bill_category, user_profile_identifier):
    request = context.request

    path = ah.bill_payees["list-operators"].replace("biller-category", bill_category)
    headers = ah.get_user_header(context, user_profile_identifier)

    response = request.hugosave_get_request(
        path=path,
        headers=headers)

    if check_status_distribute(response, 200):
        assert "billers" in response["data"], f"Missing biller info in response, received response: {response}"
        biller_data = response.get("data", {})
        context.data["users"][user_profile_identifier].setdefault(
            "biller-info", biller_data
        )


@Step("I add a Consumer ([^']*) to the service ([^']*) for the user ([^']*) and expect the bill payee status ([^']*)")
def step_impl(context, consumer_id, service_operator, user_profile_identifier, expected_status):
    request = context.request

    user_data = context.data["users"][user_profile_identifier]

    user_authorisation_token = context.data["users"][user_profile_identifier][
        "user_authorisation_token"
    ]
    headers = ah.get_user_header(context, user_profile_identifier)
    headers["x-final-user-authorisation-token"] = user_authorisation_token

    biller_category = context.data["users"][user_profile_identifier]["biller-info"][
        "billerCategory"
    ]
    biller_data = context.data["users"][user_profile_identifier]["biller-info"][
        "billers"
    ]

    operator_data = next(
        (op for op in biller_data if op.get("billerName") == service_operator), None
    )

    if not operator_data:
        raise AssertionError(
            f"Operator '{service_operator}' not found in biller data for user '{user_profile_identifier}'."
        )

    data = {
        "consumer_id": consumer_id,
        "biller_id": operator_data.get("billerId"),
        "biller_category": biller_category,
        "nick_name": "Test",
    }

    response = request.hugosave_post_request(
        path=ah.bill_payees["add-bill-payee"],
        data=data,
        headers=headers,
    )

    if check_status_distribute(response, "200"):
        assert response["data"]["billPayeeStatus"] == expected_status, f"Expected status {expected_status}, received response: {response}"
        context.data["users"][user_profile_identifier]["biller-info"]["bill-payee-id"] = (
            response["data"]["billPayeeId"]
        )


@Step("I fetch bill inquiry for user ([^']*) and expect a status ([^']*)")
def step_impl(context, user_profile_identifier, expected_status):
    request = context.request
    bill_payee_id = context.data["users"][user_profile_identifier]["biller-info"][
        "bill-payee-id"
    ]

    path = ah.bill_payees["bill-payee-inquiry"].replace("{bill-payee-id}", bill_payee_id)
    headers = ah.get_user_header(context, user_profile_identifier)

    response = request.hugosave_get_request(path=path, headers=headers)

    if check_status_distribute(response, "200"):
        if "billStatus" in response["data"]:
            assert response["data"]["billStatus"] == expected_status, f"Expected bill status: {expected_status}, but received response: {response}"
        elif "billPayeeStatus" in response["data"]:
            assert response["data"]["billPayeeStatus"] == expected_status, f"Expected bill payee status: {expected_status}, but received the response: {response}"
        else:
            assert False, f"Unexpected response, received response: {response}"
        biller_data = response.get("data", {})
        context.data["users"][user_profile_identifier].setdefault(
            "biller-inquiry", biller_data
        )


@Step("I make a ([^']*) Bill Payment(?: of amount ([^']*))? for the user ([^']*) and expect a intent status ([^']*)")
def step_impl(context, payment_type, amount, user_profile_identifier, expected_status):
    request = context.request

    bill_payee_id = context.data["users"][user_profile_identifier]["biller-info"][
        "bill-payee-id"
    ]

    if payment_type == "Prepaid":
        if amount is None:
            raise ValueError("Prepaid payment requires an amount.")
        payment_amount = amount
    elif payment_type == "Postpaid":
        payment_amount = context.data["users"][user_profile_identifier][
            "biller-inquiry"
        ]["billAmount"]
    else:
        raise ValueError(f"Unsupported payment type: {payment_type}")

    data = {
        "amount": payment_amount,
        "purpose": "Bill Payment",
    }

    user_authorisation_token = context.data["users"][user_profile_identifier][
        "user_authorisation_token"
    ]
    headers = ah.get_user_header(context, user_profile_identifier)
    headers["x-final-user-authorisation-token"] = user_authorisation_token

    response = request.hugosave_post_request(
        path=ah.bill_payees["pay-bill-payee"].replace("{bill-payee-id}", bill_payee_id),
        data=data,
        headers=headers,
    )
    if check_status_distribute(response, "200"):
        assert response["data"]["status"] == expected_status, f"Expected intent status: {expected_status}, received response: {response}"


@Step("I create a schedule for Bill Payments ([^']*) and expect status ([^']*)")
def step_impl(context, schedule_identifier, status):
    request = context.request
    schedule_bill_payments_dto = DataClassParser.parse_row(
        context.table.rows[0], data_class=CreateBillPaymentsScheduleDTO
    )
    user_profile_identifier = schedule_bill_payments_dto.user_profile_identifier
    bill_payee_id = ah.get_bill_payee_id(context, schedule_identifier, user_profile_identifier)
    amount = schedule_bill_payments_dto.amount
    schedule_bill_payments_dto.schedule_bill_payments = get_schedule_bill_payments_data(
        context, bill_payee_id, amount
    )

    schedule_bill_payments_dto.target_week = 0
    schedule_bill_payments_dto.frequency = schedule_bill_payments_dto.frequency
    if schedule_bill_payments_dto.frequency == "MONTHLY":
        schedule_bill_payments_dto.target_weekdays = list(WeekDay)[random.randrange(1, 6)].name
        schedule_bill_payments_dto.target_week = random.randrange(1, 5)
    elif schedule_bill_payments_dto.frequency == "WEEKLY":
        schedule_bill_payments_dto.target_weekdays = list(WeekDay)[random.randrange(1, 6)].name
    response = request.hugosave_post_request(
        path = ah.map_schedule_urls["root"],
        data = schedule_bill_payments_dto.get_dict(),
        headers = ah.get_user_header(context, user_profile_identifier),
    )

    assert check_status_distribute(response, status), f"Bill Payments Schedule creation failed.\nReceived : {response}"
    context.data[schedule_bill_payments_dto.schedule_identifier] = response["data"]

