from behave import *
from hugoutils.utilities.dataclass_util import DataClassParser

from tests.api.aggregate.cms import cms_helper
from tests.util.common_util import check_status
from tests.api.aggregate.cms.cms_dataclass import CreateFeeRequest, CreateTaxRequest, UpdateTaxRequest

use_step_matcher("re")


@Then("I create fee for the Product and verify status code as ([^']*)")
def create_fee_request(context, expected_status_code):
    request = context.request
    customer_profile_id = context.data["config_data"]["customer_profile_id"]

    create_fee_req_rows = DataClassParser.parse_rows(
        context.table.rows, data_class=CreateFeeRequest
    )

    for create_fee_req in create_fee_req_rows:
        product_id = context.data[create_fee_req.product_id]
        rule_group = cms_helper.get_fee_rule_group(create_fee_req.rule_group)
        fee_details = cms_helper.get_fee_details(create_fee_req.fee_details)

        data = create_fee_req.get_dict(rule_group, product_id, fee_details)

        response = request.hugoserve_post_request(
            cms_helper.fee_urls["create"],
            data=data,
            headers=cms_helper.get_headers(customer_profile_id),
        )

        check_status(response, expected_status_code)

        if expected_status_code == "200":
            get_response = request.hugoserve_get_request(
                cms_helper.fee_urls["get"].replace("$fee-id$", response["data"]["fee_id"]),
                headers=cms_helper.get_headers(customer_profile_id),
            )

            check_status(get_response, expected_status_code)
            context.data["fee_id"] = response["data"]["fee_id"]


@Then("I create tax for the Product and verify status code as ([^']*)")
def create_tax_request(context, expected_status_code):
    request = context.request
    customer_profile_id = context.data["config_data"]["customer_profile_id"]

    create_tax_req_rows = DataClassParser.parse_rows(
        context.table.rows, data_class=CreateTaxRequest
    )

    for create_tax_req in create_tax_req_rows:
        product_id = context.data[create_tax_req.product_id]
        rule_group = cms_helper.get_txn_rule_group(create_tax_req.rule_group)

        data = create_tax_req.get_dict(rule_group, product_id)

        response = request.hugoserve_post_request(
            cms_helper.tax_urls["create"],
            data=data,
            headers=cms_helper.get_headers(customer_profile_id),
        )

        check_status(response, expected_status_code)

        if expected_status_code == "200":
            tax_id = response["data"]["tax_id"]
            get_response = request.hugoserve_get_request(
                cms_helper.tax_urls["get"].replace("$tax-id$", tax_id),
                headers=cms_helper.get_headers(customer_profile_id),
            )

            check_status(get_response, expected_status_code)

            context.data[create_tax_req.tax_id] = tax_id


@Then("I update tax for the Product and verify status code as ([^']*) and verify the updated details")
def update_tax_request(context, expected_status_code):
    request = context.request
    customer_profile_id = context.data["config_data"]["customer_profile_id"]

    update_tax_req_rows = DataClassParser.parse_rows(
        context.table.rows, data_class=UpdateTaxRequest
    )

    for update_tax_req in update_tax_req_rows:
        rule_group = cms_helper.get_txn_rule_group(update_tax_req.rule_group)
        data = update_tax_req.get_dict(rule_group)
        tax_id = context.data.get(update_tax_req.tax_id)

        response = request.hugoserve_put_request(
            cms_helper.tax_urls["update"].replace("$tax-id$", tax_id),
            data=data,
            headers=cms_helper.get_headers(customer_profile_id),
        )

        check_status(response, expected_status_code)

        if expected_status_code == "200":
            tax_id = response["data"]["tax_id"]
            get_response = request.hugoserve_get_request(
                cms_helper.tax_urls["get"].replace("$tax-id$", tax_id),
                headers=cms_helper.get_headers(customer_profile_id),
            )

            check_status(get_response, expected_status_code)

            cms_helper.assert_values(
                "tax_code",
                tax_id,
                update_tax_req.tax_code,
                response["data"]["tax_code"],
            )
            cms_helper.assert_values(
                "txn_code",
                tax_id,
                update_tax_req.txn_code,
                response["data"]["txn_code"],
            )
            cms_helper.assert_values(
                "push_overdraft",
                tax_id,
                update_tax_req.push_overdraft,
                response["data"]["push_overdraft"],
            )
            cms_helper.assert_values(
                "rule_group",
                tax_id,
                rule_group,
                response["data"]["rule_group"],
            )
