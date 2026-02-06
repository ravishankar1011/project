import time
from behave import *
from hugoutils.utilities.dataclass_util import DataClassParser

from tests.api.distribute.app.hugosave_sg.app_dataclass import (
    InvestMapDTO,
    UpdateScheduleStatusRequestDTO,
    WithdrawMapDTO,
)
from tests.api.distribute.app.hugosave_sg.cash_map_steps import get_maps
from retry import retry
import tests.api.distribute.app_helper as ah
from tests.util.common_util import check_status_distribute

use_step_matcher("re")


@Step("I check if ([^']*) is created for user ([^']*)")
def check_gold_map(context, asset_name: str, uid):
    user_prof_id = ah.get_user_profile_id(uid, context)

    request = context.request
    user_maps = get_maps(request, user_prof_id, context,uid)
    context.data["users"][uid]["user_details_response"][
        "userMaps"
    ] = user_maps
    if len(list(filter(lambda c: c["mapName"] == asset_name, user_maps))) != 1:
        assert False, f"{asset_name} vault not found for user: {user_prof_id}."


@Step("I invest in ([^']*) vault map ([^']*) rate and expect a status of ([^']*)")
def invest_gold_map(context, asset_name: str, rate_case, expected_status):
    request = context.request
    invest_map_dto = DataClassParser.parse_row(
        context.table.rows[0], data_class=InvestMapDTO
    )
    user_prof_id = ah.get_user_profile_id(
        invest_map_dto.user_profile_identifier, context
    )
    userMaps = get_maps(request, user_prof_id, context,invest_map_dto.user_profile_identifier)

    map_id = None
    for map_data in userMaps:
        if "PM_GOLD_VAULT" in asset_name and map_data["mapName"] == "GOLD_VAULT":
            map_id = map_data["userMapId"]
            break
        elif "PM_SILVER_VAULT" in asset_name and map_data["mapName"] == "SILVER_VAULT":
            map_id = map_data["userMapId"]
            break
        elif "PM_PLATINUM_VAULT" == asset_name and map_data["mapName"] == "PLATINUM_VAULT":
            map_id = map_data["userMapId"]
            break
        elif "ETF_GROWTH_VAULT" == asset_name and map_data["mapName"] == "GROWTH_VAULT":
            map_id = map_data["userMapId"]
            break
        elif (
                "ETF_BALANCED_VAULT" == asset_name
                and map_data["mapName"] == "BALANCED_VAULT"
        ):
            map_id = map_data["userMapId"]
            break
        elif (
                "ETF_CAUTIOUS_VAULT" == asset_name
                and map_data["mapName"] == "CAUTIOUS_VAULT"
        ):
            map_id = map_data["userMapId"]
            break
        elif (
                "ETF_MONEY_MARKET_VAULT" == asset_name
                and map_data["mapName"] == "MONEY_MARKET_VAULT"
        ):
            map_id = map_data["userMapId"]
            break

    fee_amount = get_fee_amount(
        context, user_prof_id, map_id, invest_map_dto.transaction_amount, "buy",invest_map_dto.user_profile_identifier
    )
    invest_map_dto.fee_amount = fee_amount
    invest_map_dto.investment_amount = invest_map_dto.transaction_amount - fee_amount
    invest_map_data = invest_map_dto.get_dict()
    if rate_case != "without":
        response = request.hugosave_get_request(
            path=ah.map_urls["rate"].replace("{map-id}", map_id),
            headers=ah.get_user_header(context, invest_map_dto.user_profile_identifier),
        )

        invest_map_data["asset_rates"] = response["data"]["assetsPrice"]
        if rate_case == "invalid":
            invest_map_data["asset_rates"][0] = {
                **invest_map_data["asset_rates"][0],
                "offerPrice": 1.23,
                "bidPrice": 100,
                "token": "hi this is a wrong token. i dont like the price you sent, so i changed it. this should not be validated",
            }

    response = request.hugosave_post_request(
        ah.map_urls["invest"].replace("{map-id}", map_id),
        data=invest_map_data,
        headers=ah.get_user_header(context, invest_map_dto.user_profile_identifier),
    )

    if check_status_distribute(response, invest_map_dto.status_code):
        if invest_map_dto.status_code == 200:
            assert response["data"]["status"] == expected_status, f"Expected status: {expected_status}, but received response: {response}"


def get_fee_amount(context, user_prof_id, map_id, transaction_amount, txn_type: str,uid):
    request = context.request
    response = request.hugosave_get_request(
        path=ah.map_urls["update"].replace("{map-id}", map_id),
        headers=ah.get_user_header(context, uid),
    )

    assert check_status_distribute(response, "200"), f"Unable to fetch map for {map_id}"
    fee_percent = 0

    if txn_type == "buy":
        fee_percent = response["data"]["mapFeeDetails"]["buyFeesPercent"]
        return max(
            round(round(transaction_amount * fee_percent, 2) / 100, 2),
            response["data"]["mapFeeDetails"]["minBuyFees"],
        )
    elif txn_type == "sell":
        fee_percent = response["data"]["mapFeeDetails"]["sellFeesPercent"]
        return max(
            round(round(transaction_amount * fee_percent, 2) / 100, 2),
            response["data"]["mapFeeDetails"]["minSellFees"],
        )


@Step("I check the balance of ([^']*) Map of user ([^']*) to be ([^']*)")
def check_gold_map_balance(
        context, asset_name: str, uid, expect_balance
):
    request = context.request

    user_prof_id = ah.get_user_profile_id(uid, context)
    userMaps = get_maps(request, user_prof_id, context,uid)
    context.data["users"][uid]["user_details_response"]["userMaps"] = userMaps
    map_id = ah.get_user_map_id(context, asset_name, uid)

    if (expect_balance == "ACCOUNT_CREATION_REWARD"):
        expect_balance = context.data["users"][uid]["rewardValue"]
        expect_balance = float(expect_balance)
    elif (expect_balance == "GOLD_REWARD_VALUE"):
        expect_balance = context.data["users"][uid]["rewardValue"]
        expect_balance = float(expect_balance)
        expect_balance = expect_balance + 50
    else:
        expect_balance = float(expect_balance)

    @retry(AssertionError, tries=40, delay=10, logger=None)
    def retry_for_balance():
        response = request.hugosave_get_request(
            ah.balance_urls["map"].replace("{map-id}", map_id),
            headers = ah.get_user_header(context, uid),
        )

        actual_balance = response["data"]["currentValue"]
        threshold_difference = actual_balance * 0.2
        assert (
                expect_balance - threshold_difference
                <= actual_balance
                <= expect_balance + threshold_difference
        ), f"Actual Balance value is unexpected.\nReceived : {response}"

    retry_for_balance()


@Step("I withdraw from the ([^']*) map ([^']*) rate")
def withdraw_gold_map(context, asset_name: str, rate_case):
    request = context.request
    withdraw_map_dto = DataClassParser.parse_row(
        context.table.rows[0], data_class=WithdrawMapDTO
    )

    user = context.data["users"].get(withdraw_map_dto.user_profile_identifier)
    user_prof_id = user["create_new_user_response"]["userProfileId"]
    user_maps = context.data["users"][withdraw_map_dto.user_profile_identifier][
        "user_details_response"
    ]["userMaps"]
    map_id = None

    if "GOLD" in asset_name:
        for map_data in user_maps:
            if map_data["mapName"] == "GOLD_VAULT":
                map_id = map_data["userMapId"]
                break
    elif "SILVER" in asset_name:
        for map_data in user_maps:
            if map_data["mapName"] == "SILVER_VAULT":
                map_id = map_data["userMapId"]
                break
    elif "PLATINUM" in asset_name:
        for map_data in user_maps:
            if map_data["mapName"] == "PLATINUM_VAULT":
                map_id = map_data["userMapId"]
                break
    fee_amount = get_fee_amount(
        context, user_prof_id, map_id, withdraw_map_dto.transaction_amount, "sell",withdraw_map_dto.user_profile_identifier
    )
    withdraw_map_dto.fee_amount = fee_amount
    withdraw_map_dto.withdraw_amount = withdraw_map_dto.transaction_amount - fee_amount
    withdraw_map_data = withdraw_map_dto.get_dict()

    if rate_case != "without":
        response = request.hugosave_get_request(
            path = ah.map_urls["rate"].replace("{map-id}", map_id),
            headers=ah.get_user_header(context, withdraw_map_dto.user_profile_identifier),
        )
        withdraw_map_data["asset_rates"] = response["data"]["assetsPrice"]
        if rate_case == "invalid":
            withdraw_map_data["asset_rates"][0] = {
                **withdraw_map_data["asset_rates"][0],
                "offerPrice": 1.23,
                "bidPrice": 100,
                "token": "hi this is a wrong token. i dont like the price you sent, so i changed it. this should not be validated",
            }

    response = request.hugosave_post_request(
        ah.map_urls["withdraw"].replace("{map-id}", map_id),
        data=withdraw_map_data,
        headers=ah.get_user_header(context, withdraw_map_dto.user_profile_identifier),
    )

    assert check_status_distribute(
        response, withdraw_map_dto.status_code
    ), f"""
        \nExpected Status: {withdraw_map_dto.status_code}\n
        Actual Status: {response["headers"]["statusCode"]}
        """

    if rate_case != "invalid":
        # needed to settle withdraw txn
        context.data["withdrawTxnIntentId"] = response["data"]["intentId"]


@Step("I manually settle the sell transaction of user ([^']*)")
def settle_sell_gold(context, uid):
    time.sleep(10)
    request = context.request

    user_prof_id = ah.get_user_profile_id(uid, context)

    @retry(AssertionError, tries=10, delay=10, logger=None)
    def retry_for_settle_transaction():
        response = request.hugosave_put_request(
            ah.dev_urls["settle-all-txn"],
            headers=ah.get_user_header(context, uid),
        )

        assert check_status_distribute(response, "200")

    retry_for_settle_transaction()


@Step("I update the schedule status of ([^']*) with action ([^']*) for user ([^']*)")
def step_impl(context, schedule_identifier: str, action, uid: str):
    request = context.request

    update_status_dto = UpdateScheduleStatusRequestDTO(action=action)
    if "SCHEDULE_ROUNDUP" in schedule_identifier:
        round_up_schedule_repsonse = request.hugosave_get_request(
            path=ah.dev_urls["roundup_schedule"],
            headers=ah.get_user_header(context, uid),
        )
        check_status_distribute(round_up_schedule_repsonse, "200")
        schedule_id = round_up_schedule_repsonse["data"]["scheduleId"]
    else:
        schedule_id = context.data[schedule_identifier]["scheduleId"]

    response = request.hugosave_put_request(
        path=ah.map_schedule_urls["update-status"].replace("{schedule-id}", schedule_id),
        data=update_status_dto.get_dict(),
        headers=ah.get_user_header(context, uid),
    )
    assert check_status_distribute(response, "200")
