from behave import *
from retry import retry
import tests.api.distribute.app_helper as ah
from tests.util.common_util import check_status_distribute
from hugoutils.utilities.dataclass_util import DataClassParser
from tests.api.distribute.app.hugosave_sg.app_dataclass import TransferRequestDTO, UpdateAutoTopupDTO

use_step_matcher("re")


@Step("I initiate transfer between cash wallets")
def transfer_between_cash_wallets(context):
    request = context.request

    transfer_dto_list = DataClassParser.parse_rows(
        context.table.rows, data_class=TransferRequestDTO
    )

    for transfer_dto in transfer_dto_list:
        transfer_dto = transfer_dto.get_dict()
        user_prof_id = ah.get_user_profile_id(transfer_dto['user_profile_identifier'], context)

        primary_wallet_id = ah.get_cash_wallet_id_by_product_code(context, transfer_dto['user_profile_identifier'],
                                                                  transfer_dto['primary_wallet_id'])

        secondary_wallet_id = ah.get_cash_wallet_id_by_product_code(context, transfer_dto['user_profile_identifier'],
                                                                    transfer_dto['secondary_wallet_id'])

        transfer_response_dto = request.hugosave_put_request(
            path=ah.cash_urls["transfer"].replace("{cash-wallet-id}", primary_wallet_id),
            headers=ah.get_user_header(context, transfer_dto['user_profile_identifier']),
            data={
                "amount": transfer_dto['amount'],
                "funding_cash_wallet_id": secondary_wallet_id,
                "transfer_type": transfer_dto['transfer_type']
            }
        )

        assert check_status_distribute(transfer_response_dto, "200"), f"failed to transfer, Error Response {transfer_response_dto}"


@Step("I check the balance of wallet with product code ([^']*) of user ([^']*) is ([^']*)")
def check_wallet_balance(context, product_code: str, uid: str, balance: float):
    request = context.request

    @retry(AssertionError, tries=10, delay=5, logger=None)
    def retry_for_acc_balance():
        response = request.hugosave_get_request(
            ah.balance_urls["balances"],
            headers=ah.get_user_header(context, uid),
        )

        b1 = ah.get_balance_by_product(response, product_code)
        if b1 == float(balance):
            assert True
        else:
            assert False, f"Balances do not match"

    retry_for_acc_balance()


@Step("I setup auto topup for below cash wallet")
def enable_auto_topup(context):
    request = context.request

    update_auto_topup_list = DataClassParser.parse_rows(
        context.table.rows, data_class=UpdateAutoTopupDTO
    )

    for auto_topup_dto in update_auto_topup_list:
        auto_topup_dto = auto_topup_dto.get_dict()
        user_profile_identifier = auto_topup_dto['user_profile_identifier']
        user_prof_id = ah.get_user_profile_id(user_profile_identifier, context)

        wallet_id = ah.get_cash_wallet_id_by_product_code(context, user_profile_identifier,
                                                          auto_topup_dto['cash_wallet_id'])

        funding_wallet_id = None
        if 'funding_cash_wallet_id' in auto_topup_dto:
            funding_wallet_id = ah.get_cash_wallet_id_by_product_code(context, user_profile_identifier,
                                                                      auto_topup_dto['funding_cash_wallet_id'])

        transfer_response_dto = request.hugosave_put_request(
            path=ah.cash_urls["auto_top_up"].replace("{cash-wallet-id}", wallet_id),
            headers=ah.get_user_header(context, auto_topup_dto['user_profile_identifier']),
            data={
                "autoTopUpEnabled": auto_topup_dto['auto_topup_enabled'],
                "topUpTriggerAmount": auto_topup_dto['trigger_amount'],
                "topUpAmount": auto_topup_dto['topup_amount'],
                "isExternal": auto_topup_dto['is_external'],
                "cashWalletId": funding_wallet_id
            }
        )

        assert check_status_distribute(transfer_response_dto, "200"), f"failed to transfer, Error Response {transfer_response_dto}"


@Step("I verify auto topup ([^']*) for ([^']*) of user ([^']*)")
def verify_auto_topup(context, auto_topup_status, product_code: str, uid: str):
    request = context.request

    wallet_id = ah.get_cash_wallet_id_by_product_code(context, uid, product_code)

    cash_wallet_response_dto = request.hugosave_get_request(
        path=ah.cash_urls["root"] + "/" + wallet_id,
        headers=ah.get_user_header(context, uid)
    )

    assert check_status_distribute(cash_wallet_response_dto, "200"), f"failed to transfer, Error Response {cash_wallet_response_dto}"

    auto_topup_enabled = False
    if auto_topup_status == "enabled":
        auto_topup_enabled = True

    assert cash_wallet_response_dto['data']['autoTopUpDetails']['autoTopUpEnabled'] == auto_topup_enabled, (
        f"\nExpect auto topup status: {auto_topup_enabled}"
        f"\nActual status: {cash_wallet_response_dto['data']['autoTopUpEnabled']}"
        f"\nResponse: {cash_wallet_response_dto}"
    )

@Step("Then I get the user account details for user ([^']*)")
def get_details(context,uid):
    request = context.request

    response = request.hugosave_get_request(
            path = ah.cash_urls["get-details"],
            headers = ah.get_user_header(context, uid)
    )

    assert check_status_distribute(response, "200"), "Failed to retrieve"
