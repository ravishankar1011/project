from behave import *
import tests.api.distribute.app_helper as ah
from tests.util.common_util import check_status_distribute

use_step_matcher("re")


@Step(
    "I add a random note to the latest intent of user ([^']*) and check if note is saved"
)
def create_note(context, uid):
    request = context.request

    cash_wallet_id = ah.get_cash_wallet_id(context, uid)

    response = request.hugosave_get_request(
        path=ah.intent_urls["list_intents_for_account"].replace(
            "{cash-wallet-id}", cash_wallet_id
        ),
        headers=ah.get_user_header(context, uid),
    )

    intent_id = response["data"]["intentViews"][0]["intentId"]
    note_text = ah.get_rand_number(10)

    # create and check
    response = request.hugosave_post_request(
        path = ah.note_urls["root"],
        data = {"intent_id": intent_id, "note": note_text},
        headers = ah.get_user_header(context, uid),
    )

    if check_status_distribute(response, 200):
        response = request.hugosave_get_request(
            path = ah.note_urls["get_note"].replace("{intent_id}", intent_id),
            headers = ah.get_user_header(context, uid),
        )
        if check_status_distribute(response, 200):
            assert response["data"]["note"] == note_text, f"The expected note is: {note_text}, but received response: {response}"

    # update and check
    note_text = ah.get_rand_number(10)
    response = request.hugosave_put_request(
        path=ah.note_urls["root"],
        data={"intent_id": intent_id, "note": note_text},
        headers=ah.get_user_header(context, uid),
    )

    if check_status_distribute(response, 200):
        response = request.hugosave_get_request(
            path=ah.note_urls["get_note"].replace("{intent_id}", intent_id),
            headers=ah.get_user_header(context, uid),
        )

        if check_status_distribute(response, 200):
            assert response["data"]["note"] == note_text, f"The expected note is: {note_text}, but received response: {response}"
