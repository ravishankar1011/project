from behave import *
from black.nodes import STATEMENT

import tests.api.distribute.app_helper as ah
from tests.util.common_util import check_status_distribute
from datetime import date
from retry import retry

use_step_matcher("re")

@Step("I get all the user document types for user ([^']*) and expect a status code of ([^']*)")
def get_all_document_types(context, uid, expected_status_code):
    request = context.request
    response = request.hugosave_get_request(
        path = ah.document_urls["root"],
        headers = ah.get_user_header(context, uid),
    )
    if check_status_distribute(response, expected_status_code):
        if "documentTypes" in response["data"]:
            context.data["users"][uid]["documents"] = response


@Step("I generate a ([^']*) of type ([^']*) for user ([^']*) for the ([^']*) account")
def generate_statement(context, document_type, document_code, uid, account_type):
    request = context.request
    headers = ah.get_user_header(context, uid)
    cash_wallet_id = ah.get_cash_wallet_id(context, uid)
    body = {
        "account_id" : cash_wallet_id,
        "document_type" : document_type,
        "account_type" : account_type,
        "document_code": document_code,
        "from_ts": "2025-07-15",
        "to_ts": (date.today()).strftime("%Y-%m-%d"),
        "document_format": "PDF",
        "transaction_status": "TRANSACTION_STATUS_SETTLED",
        "transaction_type": "TRANSACTION_TYPE_CREDIT"
    }
    if document_type == "STATEMENT":
        path = ah.document_urls["generate_statement"]
    else:
        path = ah.document_urls["generate_certificate"]
    response = request.hugosave_post_request(
        path = path,
        headers = headers,
        data = body
    )

    if check_status_distribute(response, 200):
        assert "userDocumentId" in response["data"]
        context.data["users"][uid]["documents"] = {}
        context.data["users"][uid]["documents"][document_type] = {}
        context.data["users"][uid]["documents"][document_type][document_code] = {}
        context.data["users"][uid]["documents"][document_type][document_code]["user_document_id"] = response["data"]["userDocumentId"]


@Step("I get the ([^']*) of type ([^']*) for user ([^']*)")
def get_user_document(context, document_type, document_code, uid):
    request = context.request
    headers = ah.get_user_header(context, uid)
    user_document_id = ah.get_user_document_id(context, uid, document_type, document_code)

    @retry(AssertionError, tries=30, delay=15, logger=None)
    def retry_get_user_document():
        response = request.hugosave_get_request(
            path = ah.document_urls["get_user_document"].replace("{user-document-id}", user_document_id),
            headers = headers,
            params ={"file-type": "PDF"}
        )
        if check_status_distribute(response, 200):
            assert "signedUrl" in response["data"]

    retry_get_user_document()
