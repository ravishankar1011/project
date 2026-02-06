from behave import *

import tests.api.distribute.app_helper as ah
from tests.util.common_util import check_status_distribute

use_step_matcher("re")


@Step("I get QR code for user ([^']*)")
def step_impl(context, uid):
    request = context.request
    cash_wallet_id = ah.get_cash_wallet_id_by_product_code(
        context, uid, "CASH_WALLET_CURRENT"
    )

    response = request.hugosave_get_request(
        ah.cash_urls["cash-wallet-details"].replace("{cash-wallet-id}", cash_wallet_id),
        headers=ah.get_user_header(context, uid),
    )
    context.data["users"][uid]["qr_code"] = response["data"][
        "qrCode"
    ]

    assert check_status_distribute(response, "200"), "Error fetching cash wallet details"


@Step("I get the user ([^']*) transfer out account details using ([^']*) QR code and expect a status of ([^']*)")
def step_impl(context, uid, case, expected_status):
    request = context.request
    if case == "Valid":
        data = {
            "inquiry": {
                "country": "PAK",
                "code_details": {
                    "pk_account": {
                        "qr_code": context.data["users"][uid][
                            "qr_code"
                        ]
                    }
                },
            }
        }
    else:
        data = {"qr_code": 123453}
    response = request.hugosave_post_request(
        ah.payee_urls["inquiry"],
        headers=ah.get_user_header(context, uid),
        data=data,
    )

    if check_status_distribute(response, 200):
        assert response["data"]["status"] == expected_status, f"Expected the status: {expected_status}, but received the response: {response}"
        if "inquiry_info" not in context.data["users"][uid]:
            context.data["users"][uid]["inquiry_info"] = {}

        context.data["users"][uid]["inquiry_info"]["transfer_out_account_details"] = response["data"]["transferOutAccountDetails"]
        context.data["users"][uid]["inquiry_info"]["amount"] = response["data"]["amount"]


@Step("I create dynamic QR code with amount ([^']*) PKR for user ([^']*)")
def step_impl(context, amount, uid):
    request = context.request
    cash_wallet_id = ah.get_cash_wallet_id_by_product_code(
        context, uid, "CASH_WALLET_CURRENT"
    )
    body = {"amount": amount, "valid_ts": "2025-07-29T18:32:56Z"}
    response = request.hugosave_put_request(
        ah.cash_urls["create-dynamic-qr"].replace("{cash-wallet-id}", cash_wallet_id),
        data=body,
        headers=ah.get_user_header(context, uid),
    )


    if check_status_distribute(response, "200"):
        assert "qrCode" in response["data"], f"Dynamic QR missing in the response, received response is: {response}"
        context.data["users"][uid]["qr_code"] = response["data"]["qrCode"]
