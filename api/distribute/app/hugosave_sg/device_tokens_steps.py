from behave import *
import tests.api.distribute.app_helper as ah
from tests.util.common_util import check_status_distribute

use_step_matcher("re")


@Step("I push device token for user ([^']*) and check if saved")
def push_device_token(context, uid):
    request = context.request

    token = str(ah.get_rand_number(5))

    response = request.hugosave_post_request(
        path=ah.device_urls["root"],
        data={"token": token},
        headers=ah.get_user_header(context, uid),
    )

    assert check_status_distribute(response, "200"), f"Failed to push device token\nReceived : {response}"

    response = request.hugosave_get_request(
        path=ah.device_urls["list"],
        headers=ah.get_user_header(context, uid),
    )
    if check_status_distribute(response, 200):
        assert "pnToken" in response["data"], f"Expected token in response, but received response: {response}"
        saved_token = response["data"]["pnToken"]


@Step("I push another device token for user ([^']*) and check if updated")
def push_device_token(context, uid):
    request = context.request
    token = str(ah.get_rand_number(5))

    response = request.hugosave_post_request(
        path=ah.device_urls["root"],
        data={"token": token},
        headers=ah.get_user_header(context, uid),
    )

    assert check_status_distribute(response, 200), f"Failed to push device token,\nReceived response: {response}"

    response = request.hugosave_get_request(
        path=ah.device_urls["list"],
        headers=ah.get_user_header(context, uid),
    )
    if check_status_distribute(response, 200):
        for returned_token in response["data"]["pnToken"]:
            assert returned_token["token"] == token, f"The expected token: {token} and the received token: {response["data"]["pnToken"]} don't match"
        context.data["users"][uid]['savedToken'] = response["data"]["pnToken"]


@Step("I delete device token for user ([^']*)")
def remove_token(context, uid):
    request = context.request

    items = context.data["users"][uid]['savedToken']
    headers=ah.get_user_header(context, uid)
    headers["x-final-user-authorisation-token"] = context.data["users"][uid]["user_authorisation_token"]
    for token_item in items:
        token = token_item['token']

    response = request.hugosave_delete_request(
        path=ah.device_urls["delete"].replace("token", token),
        headers = headers,
    )
    assert check_status_distribute(response, 200), f"Expected status 200, but received the response: {response}"

    response = request.hugosave_get_request(
        path=ah.device_urls["list"],
        headers=ah.get_user_header(context, uid),
    )

    if check_status_distribute(response, 200):
        assert len(response["data"]["pnToken"]) == 0, f"Failed deleting token, received response: {response}"
