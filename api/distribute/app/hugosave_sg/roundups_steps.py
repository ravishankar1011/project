from behave import *

import tests.api.distribute.app_helper as ah
from tests.util.common_util import check_status_distribute
from tests.api.distribute.app.hugosave_sg.cash_map_steps import get_maps

use_step_matcher("re")


@Step("I ([^']*) roundups for user ([^']*)")
def toggle_roundups(context, case, uid):
    request = context.request

    response = request.hugosave_put_request(
        path=ah.roundup_urls["enable"],
        data={"action": case},
        headers=ah.get_user_header(context, uid),
    )

    state = "True" if case == "ENABLE" else "False"
    if check_status_distribute(response, "200"):
        assert str(response["data"]["roundupStatus"]) == state, f"Expected round up initialised status of: {state}, but received response: {response}"


@Step("I update Roundup Sweep vault to ([^']*) for user ([^']*)")
def update_sweep_vault(context, sweep_vault: str, uid):
    request = context.request

    response = request.hugosave_put_request(
        path=ah.roundup_urls["update_sweep_vault"],
        data={"sweep_vault": sweep_vault},
        headers=ah.get_user_header(context, uid),
    )

    assert check_status_distribute(response, "200")


@Step("I trigger roundups for the new ([^']*) card user ([^']*) and expect trigger initialisation status as ([^']*)")
def step_impl(context, card_type, uid, expected_status):
    request = context.request
    card_id = ah.get_card_id(context, uid, card_type)
    data = {
        "enabled_triggers": [{"trigger_type": "TRIGGER_CARD", "trigger_id": card_id}]
    }
    response = request.hugosave_put_request(
        path=ah.roundup_urls["trigger"],
        data=data,
        headers=ah.get_user_header(context, uid),
    )
    if check_status_distribute(response, "200"):
        assert response["data"]["triggerInitialised"] == bool(expected_status), f"Expected trigger initialisation status to be: {expected_status}, but received response: {response}"


@Step(
    "I transfer ([^']*) ([^']*) from roundups account to the ([^']*) for user ([^']*) and expect a status code of ([^']*)"
)
def step_impl(context, amount, currency, account_type, uid, expected_status_code):
    request = context.request
    cash_wallet_id = ah.get_cash_wallet_id(context, uid)
    data = {
        "amount": amount,
        "transfer_type": "TRANSFER_OUT",
        "funding_cash_wallet_id": cash_wallet_id,
    }
    response = request.hugosave_post_request(
        path=ah.roundup_urls["transfer"],
        data=data,
        headers=ah.get_user_header(context, uid),
    )

    assert check_status_distribute(response, expected_status_code), f"The expected status code is: {expected_status_code}, but received response: {response}"


@Step("I save map ([^']*) for the Roundup Sweep for the user ([^']*)")
def step_impl(context, map_identifier, uid):
    request = context.request
    userMaps = get_maps(request, uid, context,uid)
    context.data["users"][uid]["user_details_response"]["userMaps"] = userMaps
    map_id = ah.get_user_map_id(context, map_identifier, uid)

    data = {"enabled_sweeps": [{"sweep_type": "SWEEP_MAP", "sweep_id": map_id}]}
    response = request.hugosave_put_request(
        path=ah.roundup_urls["sweep"],
        data=data,
        headers=ah.get_user_header(context, uid),
    )

    assert check_status_distribute(response, "200")

@Step("I set ([^']*) as trigger for roundup for user ([^']*)")
def step_impl(context, asset_name, uid):
    request = context.request

    user_prof_id = ah.get_user_profile_id(uid, context)
    userMaps = get_maps(request, user_prof_id, context,uid)
    context.data["users"][uid]["user_details_response"]["userMaps"] = userMaps
    map_id = ah.get_user_map_id(context, asset_name, uid)
    data = {"enabled_sweeps": [{"sweep_type": "SWEEP_MAP", "sweep_id": map_id}]}