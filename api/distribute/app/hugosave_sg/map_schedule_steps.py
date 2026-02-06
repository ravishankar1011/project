import random

from behave import *
from hugoutils.utilities.dataclass_util import DataClassParser

from tests.api.distribute.app.hugosave_sg.app_dataclass import (
    CreateMapScheduleDTO,
    ScheduleMapInvest,
    WeekDay, UpdateMapScheduleDTO, ScheduleBillPaymentsInvest, SchedulePayeePayments,
)
import tests.api.distribute.app_helper as ah
from tests.util.common_util import check_status_distribute

use_step_matcher("re")


def get_schedule_map_invest_data(
        context, user_map_id, user_profile_id, user_main_account_id, amount,uid
):
    request = context.request
    response = request.hugosave_get_request(
        path=ah.map_urls["update"].replace("{map-id}", user_map_id),
        headers=ah.get_user_header(context, uid),
    )

    if not check_status_distribute(response, "200"):
        assert False, f"Unable to fetch map details.\nReceived : {response}"

    return ScheduleMapInvest(
        map_id=user_map_id,
        map_name=response["data"]["mapName"],
        map_type=response["data"]["mapType"],
        amount=amount,
        units=random.randrange(2),
        payee_account_id=user_main_account_id,
        map_category=response["data"]["mapCategory"],
        map_goal_amount=random.randrange(5, 15),
        map_invested_amount=response["data"]["amountInvested"],
    )

def get_schedule_bill_payments_data(
    context, bill_payee_id, amount
):
    return ScheduleBillPaymentsInvest(
        bill_payee_id = bill_payee_id,
        amount  = amount
    )

def get_schedule_payee_payments_data(
    context, payee_id, amount
):
    return SchedulePayeePayments(
        payee_id = payee_id,
        amount  = amount
    )


def get_account_id_by_subtype(
        context, user_profile_identifier: str, account_subtype: str
):
    for account in context.data["users"][user_profile_identifier]["userAccounts"]:
        if account["accountSubtype"] == account_subtype:
            return account["accountId"]

    assert (
        False
    ), f"User {user_profile_identifier} account not found for subtype : {account_subtype}"


@Step("I create a schedule for map ([^']*) and expect status ([^']*)")
def create_map_schedule(context, map_identifier: str, status: str):
    request = context.request
    schedule_map_dto = DataClassParser.parse_row(
        context.table.rows[0], data_class=CreateMapScheduleDTO
    )
    user_profile_identifier = schedule_map_dto.user_profile_identifier
    product_code = schedule_map_dto.product_code
    user_prof_id = ah.get_user_profile_id(user_profile_identifier, context)
    user_map_id = ah.get_user_map_id(context, map_identifier, user_profile_identifier)
    amount = schedule_map_dto.amount
    user_main_account_id = ah.get_cash_wallet_id_by_product_code(context, user_profile_identifier, product_code)
    schedule_map_dto.schedule_map_invest = get_schedule_map_invest_data(
        context, user_map_id, user_prof_id, user_main_account_id, amount,user_profile_identifier
    )

    schedule_map_dto.target_week = 0
    schedule_map_dto.frequency = schedule_map_dto.frequency
    if schedule_map_dto.frequency == "MONTHLY":
        schedule_map_dto.target_weekdays = list(WeekDay)[random.randrange(1, 6)].name
        schedule_map_dto.target_week = random.randrange(1, 5)
    elif schedule_map_dto.frequency == "WEEKLY":
        schedule_map_dto.target_weekdays = list(WeekDay)[random.randrange(1, 6)].name
    response = request.hugosave_post_request(
        path = ah.map_schedule_urls["root"],
        data = schedule_map_dto.get_dict(),
        headers = ah.get_user_header(context, user_profile_identifier),
    )

    if check_status_distribute(response, status):
        if status == "200":
            assert "scheduleId" in response["data"], f"Expected schedule id in response, but received response: {response}"
            context.data[schedule_map_dto.schedule_identifier] = response["data"]


@Step("I trigger schedule ([^']*) for user ([^']*) and expect a status code of ([^']*)")
def trigger_schedule(context, schedule_identifier: str, uid: str, expected_status_code):
    request = context.request

    if "SCHEDULE_ROUNDUP" in schedule_identifier:
        round_up_schedule_response = request.hugosave_post_request(
            path=ah.dev_urls["clear_roundup_schedule"],
            headers=ah.get_user_header(context, uid),
        )
        assert check_status_distribute(round_up_schedule_response, "200"), f"Unexpected status code, returned data: {round_up_schedule_response}"
    else:
        schedule_id = context.data[schedule_identifier]["scheduleId"]
        response = request.hugosave_put_request(
            ah.dev_urls["schedule_trigger"].replace("{schedule-id}", schedule_id),
            headers=ah.get_user_header(context, uid),
        )
        assert check_status_distribute(response, expected_status_code), f"Expected status code: {expected_status_code},but received response: {response}"


@Step("I check if the schedule ([^']*) has a status code of ([^']*) and a status of ([^']*) for user ([^']*)")
def step_impl(context, schedule_identifier: str, expected_status_code, expected_status, uid: str):
    request = context.request
    schedule_id = context.data[schedule_identifier]["scheduleId"]

    get_user_maps_response = request.hugosave_get_request(
        path = ah.map_schedule_urls["detail"].replace("{schedule-id}", schedule_id),
        headers = ah.get_user_header(context, uid),
    )
    if check_status_distribute(get_user_maps_response, expected_status_code):
        if expected_status_code == 200:
            assert get_user_maps_response["data"]["scheduleStatus"] == expected_status, f"Mismatch in the schedule status, expected {expected_status}, received response: {get_user_maps_response}"


@Step("I skip the schedule ([^']*) for user ([^']*) and expect a status of ([^']*)")
def step_impl(context, schedule_identifier, uid, expected_status):
    global dates
    request = context.request
    schedule_id = context.data[schedule_identifier]["scheduleId"]
    upcoming_schedule_data=context.data[schedule_identifier]["details"]["upcomingScheduleData"]
    for item in upcoming_schedule_data:
        dates= []
        if 'date' in item:
            dates.append(item['date'])
    response = request.hugosave_put_request(
        path = ah.map_schedule_urls["skip"].replace("{schedule-id}", schedule_id),
        headers=ah.get_user_header(context, uid),
        data={"dates":[dates]},
    )
    if check_status_distribute(response, 200):
        assert response["data"]["status"] == expected_status, f"Expected a status of: {expected_status}, but received a response of: {response}"
        context.data[schedule_identifier]["previous_date"] = dates


@Step("I check if the upcoming schedule date is updated for schedule ([^']*) for user ([^']*)")
def step_impl(context,schedule_identifier: str, uid: str):
    global upcoming_date
    request = context.request
    schedule_id = context.data[schedule_identifier]["scheduleId"]

    response = request.hugosave_get_request(
        path = ah.map_schedule_urls["detail"].replace("{schedule-id}", schedule_id),
        headers=ah.get_user_header(context, uid),
    )
    if check_status_distribute(response, 200):
        context.data[schedule_identifier]["details"] = response.get("data")
        previous_schedule_date = context.data[schedule_identifier]["previous_date"]
        upcoming_schedule_data = context.data[schedule_identifier]["details"]["upcomingScheduleData"]
        for item in upcoming_schedule_data:
            upcoming_date = []
            if 'date' in item:
                upcoming_date.append(item['date'])
        upcoming_schedule_date = upcoming_date
        assert previous_schedule_date != upcoming_schedule_date, f"Date update in Skip Schedule failed."


@Step("I delete schedule ([^']*) for user ([^']*) and expect a status code of ([^']*)")
def step_impl(context, schedule_identifier: str, uid: str, expected_status_code):
    request = context.request
    schedule_id = context.data[schedule_identifier]["scheduleId"]

    response = request.hugosave_delete_request(
        path=ah.map_schedule_urls["root"] + "/" + schedule_id,
        headers=ah.get_user_header(context, uid),
        )
    assert check_status_distribute(response, expected_status_code), f"Expected status status code:{expected_status_code}, but received response: {response}"


@Step("I check schedule status as ([^']*) for schedule ([^']*) for user ([^']*)")
def step_impl(
        context, status: str, schedule_identifier: str, uid: str
):
    request = context.request
    schedule_id = context.data[schedule_identifier]["scheduleId"]

    response = request.hugosave_get_request(
        path=ah.map_schedule_urls["detail"].replace("{schedule-id}", schedule_id),
        headers=ah.get_user_header(context, uid),
    )
    check_status_distribute(response, "200")
    assert (
            response["data"]["scheduleStatus"] == status
    ), f'Schedule status expected to be {status}. But received: {response["data"]}'


@Step("I check schedule status as ([^']*) for upcoming schedule ([^']*) for user ([^']*)")
def step_impl(
        context, status: str, schedule_identifier: str, uid: str
):
    request = context.request
    schedule_id = context.data[schedule_identifier]["scheduleId"]

    response = request.hugosave_get_request(
        path=ah.map_schedule_urls["detail"].replace("{schedule-id}", schedule_id),
        headers=ah.get_user_header(context, uid),
    )
    check_status_distribute(response, "200")
    context.data[schedule_identifier]["details"] = response.get("data")
    upcoming_schedule_data=context.data[schedule_identifier]["details"]["upcomingScheduleData"]
    for item in upcoming_schedule_data:
        actual_item_status = item.get("status")
        if actual_item_status == status:
            assert True
        else:
            assert False, f'Schedule status expected to be {status}. But received: {actual_item_status}'


@Step("I update the schedule for map ([^']*) and expect status ([^']*)")
def update_map_schedule(context, map_identifier: str, status: str):
    request = context.request
    schedule_map_dto = DataClassParser.parse_row(
        context.table.rows[0], data_class=UpdateMapScheduleDTO
    )
    schedule_identifier=schedule_map_dto.schedule_identifier
    schedule_id = context.data[schedule_identifier]["scheduleId"]
    product_code = schedule_map_dto.product_code
    uid = schedule_map_dto.user_profile_identifier
    user_prof_id = ah.get_user_profile_id(uid, context)
    user_map_id = ah.get_user_map_id(context, map_identifier, uid)
    amount = schedule_map_dto.amount

    user_main_account_id = ah.get_cash_wallet_id_by_product_code(context, uid, product_code)
    schedule_map_dto.schedule_map_invest = get_schedule_map_invest_data(
        context, user_map_id, user_prof_id, user_main_account_id, amount,uid
    )
    schedule_map_dto.target_week = 0
    schedule_map_dto.frequency = schedule_map_dto.frequency
    if schedule_map_dto.frequency == "MONTHLY":
        schedule_map_dto.target_weekdays = list(WeekDay)[random.randrange(1, 6)].name
        schedule_map_dto.target_week = random.randrange(1, 5)
    elif schedule_map_dto.frequency == "WEEKLY":
        schedule_map_dto.target_weekdays = list(WeekDay)[random.randrange(1, 6)].name
    response = request.hugosave_put_request(
        path=ah.map_schedule_urls["update"].replace("{schedule-id}", schedule_id),
        headers=ah.get_user_header(context, schedule_map_dto.user_profile_identifier),
        data=schedule_map_dto.get_dict(),
    )

    assert check_status_distribute(response, status), f"Map Schedule update failed.\nReceived : {response}"
    if "data" in response:
        context.data[schedule_map_dto.schedule_identifier] = response["data"]

    response1 = request.hugosave_get_request(
        path=ah.map_schedule_urls["detail"].replace("{schedule-id}", schedule_id),
        headers=ah.get_user_header(context, uid),
    )
    context.data[schedule_identifier]["details"]=response1.get("data")
