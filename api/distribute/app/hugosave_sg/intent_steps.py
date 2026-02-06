from behave import *
from retry import retry
from tests.util.common_util import check_status_distribute
from hugoutils.utilities.dataclass_util import DataClassParser
from tests.api.distribute.app.hugosave_sg.app_dataclass import ListIntentDTO
from tests.api.distribute.app.hugosave_sg.cash_map_steps import get_maps

date_format = "%Y-%m-%dT%H:%M:%S.%fZ"
import tests.api.distribute.app_helper as ah

use_step_matcher("re")


@Step(
    "I check if the intent with type ([^']*) has the status ([^']*) and a total of ([^']*) intents exist for the user ([^']*) in the ([^']*) view"
)
def check_intents(
        context,
        intent_type,
        intent_status,
        total_intents: int,
        uid,
        view_type,
):
    request = context.request
    headers = ah.get_user_header(context, uid)
    user_prof_id = ah.get_user_profile_id(uid, context)
    user_maps = get_maps(request, user_prof_id, context,uid)
    context.data["users"][uid]["user_details_response"]["userMaps"] = user_maps
    if view_type == "cash":
        acc_id = ah.get_cash_wallet_id(context, uid)
        url = ah.intent_urls["list_intents_for_account"].replace(
            "{cash-wallet-id}", acc_id
        )

    if view_type.__contains__("map_intent_view"):
        map_identifier = view_type.split(",")[1]
        map_id = ah.get_user_map_id(context, map_identifier, uid)
        url = ah.intent_urls["list_intents_for_map"].replace("{map-id}", map_id)

    @retry(AssertionError, tries=40, delay=15, logger=None)
    def retry_for_intent_status():
        response = request.hugosave_get_request(
            url,
            headers=ah.get_user_header(context, uid),
        )

        if check_status_distribute(response, "200"):

            intent_views = response["data"]["intentViews"]
            intent_status_count = 0
            for intent in intent_views:
                if intent["status"] == intent_status and intent["type"] == intent_type:
                    intent_status_count += 1

            if intent_status_count != int(total_intents):
                assert False, "Total intents does not match"

    retry_for_intent_status()


@Step("I verify below intent record in present in intents list")
def verify_intent_record_in_list(context):
    request = context.request

    intent_dto_list = DataClassParser.parse_rows(context.table.rows, data_class=ListIntentDTO)

    for intent_record in intent_dto_list:
        intent_record = intent_record.get_dict()
        user_profile_identifier = intent_record['user_profile_identifier']
        intent_view = intent_record['view']
        intent_status = intent_record['intent_status']
        intent_type = intent_record['intent_type']
        intent_count = intent_record['count']

        if intent_view == "cash":
            cash_wallet_id = ah.get_cash_wallet_id_by_product_code(context, user_profile_identifier,
                                                                   intent_record['product_code'])
            url = ah.intent_urls["list_intents_for_account"].replace(
                "{cash-wallet-id}", cash_wallet_id)
        #TODO: Accept card type in step to get the card id while checking card intents
        elif intent_view == "card":
            card_id = ah.get_card_id(context, user_profile_identifier)
            url = ah.intent_urls["list_intents_for_cards"].replace("{card-id}", card_id)

        elif intent_view == "roundup":
            url = ah.intent_urls["list_intents_for_roundup"]

        if intent_view.__contains__("map_intent_view"):
            map_identifier = intent_view.split(",")[1]
            map_id = ah.get_user_map_id(context, map_identifier, user_profile_identifier)
            url = ah.intent_urls["list_intents_for_map"].replace("{map-id}", map_id)

        @retry(AssertionError, tries=30, delay=15, logger=None)
        def retry_for_intent_status():
            response = request.hugosave_get_request(
                path=url,
                headers=ah.get_user_header(context, user_profile_identifier),
            )

            if check_status_distribute(response, "200"):

                intent_views = response["data"]["intentViews"]
                intent_status_count = 0
                for intent in intent_views:
                    if intent["status"] == intent_status and intent["type"] == intent_type:
                        intent_status_count += 1

                if intent_status_count != int(intent_count):
                    assert False, "Total intents does not match"

        retry_for_intent_status()
