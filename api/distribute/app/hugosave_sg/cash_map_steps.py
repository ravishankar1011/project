from behave import *
from hugoutils.utilities.dataclass_util import DataClassParser

from tests.api.distribute.app.hugosave_sg.app_dataclass import (
    CreateMapDTO,
    InvestMapDTO,
    UpdateMapDTO,
    WithdrawMapDTO,
)
from retry import retry
import tests.api.distribute.app_helper as ah
from tests.util.common_util import check_status_distribute

use_step_matcher("re")


def get_maps(request, user_prof_id, context,uid):
    response = request.hugosave_get_request(
        path = ah.user_profile_urls["map-list"],
        headers=ah.get_user_header(context, uid),
    )

    assert check_status_distribute(response, "200")
    return response["data"]["maps"]


@Step("I create a Map ([^']*) and expect a status of ([^']*)")
def create_map(context, map_identifier, expected_status):
    request = context.request
    create_map_list_dto = DataClassParser.parse_rows(
        context.table.rows, data_class=CreateMapDTO
    )

    for create_map_dto in create_map_list_dto:
        create_map_dto_data = create_map_dto.get_dict()
        user_profile_identifier = create_map_dto.user_profile_identifier
        response = request.hugosave_post_request(
            ah.map_urls["root"],
            data=create_map_dto_data,
            headers=ah.get_user_header(context, user_profile_identifier),
        )

        if check_status_distribute(response, "200"):
            assert response["data"]["status"] == expected_status, f"Expected a status of {expected_status}, but received a response: {response}"
            context.data["users"][user_profile_identifier][map_identifier] = create_map_dto_data
            context.data["users"][user_profile_identifier][map_identifier]["mapId"] = response["data"]["mapId"]


@Step("I check if the map ([^']*) is created for user ([^']*) and expect a status of ([^']*)")
def check_map_status(context, map_identifier: str, uid, expected_status):
    request = context.request

    user_prof_id = ah.get_user_profile_id(uid, context)
    user_map_name = context.data["users"][uid][map_identifier]["name"]

    @retry(AssertionError, tries=10, delay=10, logger=None)
    def retry_for_map_status():
        user_maps = get_maps(request, user_prof_id, context,uid)
        context.data["users"][uid]["user_details_response"]["userMaps"] = user_maps
        for map in user_maps:
            if map["mapName"] == user_map_name:
                assert map["status"] == expected_status, f"Expected a status of {expected_status}, but received response: {user_maps}"
                context.data["users"][uid][map_identifier] = map

    retry_for_map_status()


@Step("I invest in map ([^']*) and expect a status of ([^']*)")
def invest_map(context, map_identifier, expected_status):
    request = context.request
    invest_map_dto = DataClassParser.parse_row(
        context.table.rows[0], data_class=InvestMapDTO
    )

    user_profile_identifier = invest_map_dto.user_profile_identifier

    map_id = context.data["users"][user_profile_identifier][map_identifier]["userMapId"]
    if invest_map_dto.invalid_map == "Y":
        map_id = ah.get_uuid()

    response = request.hugosave_post_request(
        path = ah.map_urls["invest"].replace("{map-id}", map_id),
        data = invest_map_dto.get_dict(),
        headers = ah.get_user_header(context, invest_map_dto.user_profile_identifier),
    )

    if invest_map_dto.invalid_map != "Y":
        if invest_map_dto.status_code == "200":
            assert response["data"]["status"] == expected_status
        else:
            assert response["headers"]["message"] == expected_status
    else:
        if check_status_distribute(response, invest_map_dto.status_code):
            assert response["headers"]["message"] == expected_status


@Step("I check the balance of map ([^']*) of user ([^']*) to be ([^']*)")
def check_map_invest_status(context, map_identifier, uid, expected_balance):
    request = context.request
    expected_balance = expected_balance.split(" ")
    for item in expected_balance:
        try:
            expected_balance = float(item)
        except ValueError:
            pass
    user_map_id = ah.get_user_map_id(context, map_identifier, uid)

    @retry(AssertionError, tries=40, delay=15, logger=None)
    def retry_for_asset_balance():
        response = request.hugosave_get_request(
            path=ah.balance_urls["map"].replace("{map-id}", user_map_id),
            headers=ah.get_user_header(context, uid),
        )

        if check_status_distribute(response, 200):
            assert response["data"]["currentValue"] == expected_balance, f"Mismatch in balance, returned response: {response}"

    retry_for_asset_balance()


@Step("I withdraw from map ([^']*) and expect a status of ([^']*)")
def withdraw_map(context, map_identifier, expected_status):
    request = context.request
    withdraw_map_dto = DataClassParser.parse_row(
        context.table.rows[0], data_class=WithdrawMapDTO
    )

    user_profile_identifier = withdraw_map_dto.user_profile_identifier
    map_id = context.data["users"][user_profile_identifier][map_identifier]["userMapId"]
    if withdraw_map_dto.invalid_map == "Y":
        map_id = ah.get_uuid()
    response = request.hugosave_post_request(
        path = ah.map_urls["withdraw"].replace("{map-id}", map_id),
        data = withdraw_map_dto.get_dict(),
        headers = ah.get_user_header(context, user_profile_identifier),
    )

    if check_status_distribute(response, withdraw_map_dto.status_code):
        if withdraw_map_dto.invalid_map != "Y":
            assert response["data"]["status"] == expected_status
        else:
            assert response["headers"]["message"] == expected_status


@Step("I update the map ([^']*) and check if update was successful")
def update_map(context, map_identifier):
    request = context.request
    update_map_dto = DataClassParser.parse_row(
        context.table.rows[0], data_class=UpdateMapDTO
    )

    user_profile_identifier = update_map_dto.user_profile_identifier
    user_prof_id = ah.get_user_profile_id(user_profile_identifier, context)

    update_map_id = context.data["users"][user_profile_identifier][map_identifier][
        "userMapId"
    ]
    if update_map_dto.invalid_map == "Y":
        update_map_id = ah.get_uuid()

    response = request.hugosave_put_request(
        path=ah.map_urls["update"].replace("{map-id}", update_map_id),
        data=update_map_dto.get_dict(),
        headers=ah.get_user_header(context, user_profile_identifier),
    )

    assert check_status_distribute(
        response, update_map_dto.status_code
    ), f"""
        \nExpected Status: {update_map_dto.status_code}\n
        Actual Status: {response["headers"]["statusCode"]}
        """

    if update_map_dto.status_code == "HSA_9107":
        return

    updated_map = None
    returned_maps = get_maps(request, user_prof_id, context,user_profile_identifier)
    for map in returned_maps:
        if map["userMapId"] == update_map_id:
            updated_map = map
            break

    context.data["users"][user_profile_identifier][map_identifier] = updated_map
    assert update_map_dto.name == updated_map["mapName"], "Name not updated"
    for data in updated_map["metadata"]["data"]:
        if data["key"] == "goal_date":
            assert update_map_dto.goal_date == data["stringValue"], "Goal Date not updated"
        elif data["key"] == "goal_amount":
            assert update_map_dto.goal_amount == data["doubleValue"], "Goal Amount not updated"


@Step("I delete the map ([^']*) of user ([^']*) and expect a status code of ([^']*)")
def delete_map(context, map_identifier: str, uid, expected_status_code):
    request = context.request

    map_id = context.data["users"][uid][map_identifier]["userMapId"]

    response = request.hugosave_delete_request(
        ah.map_urls["update"].replace("{map-id}", map_id),
        headers=ah.get_user_header(context, uid),
    )

    assert check_status_distribute(response, expected_status_code), f"Error deleting map.\nReceived : {response}"


@Step("I check if the cash map ([^']*) is deleted successfully for user ([^']*)")
def step_impl(context, map_identifier: str, uid: str):
    request = context.request

    map_id = context.data["users"][uid][map_identifier]["userMapId"]

    @retry(AssertionError, tries=30, delay=10, logger=None)
    def retry_for_map_status():
        response = request.hugosave_get_request(
            ah.map_urls["update"].replace("{map-id}", map_id),
            headers=ah.get_user_header(context, uid),
        )

        assert (
                response["headers"]["statusCode"] == "HSA_9107"
        ), f"Expected map to be deleted. Response : {response}"

    retry_for_map_status()
