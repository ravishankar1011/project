import dataclasses
import time

import yaml
import os
import tests.api.distribute.app_helper as ah

from behave import *
from dacite import from_dict
from tests.api.distribute.app.hugosave_sg.app_dataclass import CardProductParamRequest, CardAccountProductParamRequest
from tests.util.common_util import check_status_distribute

use_step_matcher("re")


@Step("I initiate the card creation from ([^']*)")
def create_product(context, yaml_file_name):
    request = context.request

    try:
        script_dir = os.path.dirname(os.path.abspath(__file__))
        product_factory_dir = os.path.join(script_dir, "product_factory")
        yaml_file_path = os.path.join(product_factory_dir, yaml_file_name)
        print(yaml_file_name)
        with open(yaml_file_path, 'r') as f:
            product_data = yaml.safe_load(f)

        if product_data is None:
            raise ValueError(f"YAML file '{yaml_file_path}' is empty or invalid.")

        print(f"Attempting card creation by using data from '{yaml_file_path}'")

        service = product_data.get("service")
        if not service:
            raise ValueError("Missing 'service' key in YAML.")
        service_products_list = service.get("products")
        if not service_products_list:
            raise ValueError("Missing 'products' list under 'service' in YAML.")

        for product_details in service_products_list:
            product_code = product_details.get("product_code")
            if not product_code:
                raise ValueError("Product details in YAML missing 'product_code'.")

            request_payload = {
                "service_name": service.get("service_name"),
                "product_code": product_code,
                "end_product_code": product_details.get("end_product_code"),
                "provider_id": product_details.get("provider_id"),
                "profile_type": product_details.get("profile_type"),
                "product_class": product_details.get("product_class"),
                "product_type": product_details.get("product_type"),
                "product_access_type": product_details.get("product_access_type"),
                "product_name": product_details.get("product_name"),
                "product_description": product_details.get("product_description"),
            }

            if "card_params" in product_details:
                card_params_dto = from_dict(data_class=CardProductParamRequest,
                                            data=product_details.get("card_params"))
                request_payload["card_params"] = dataclasses.asdict(card_params_dto)
            elif "card_account_params" in product_details:
                card_account_params_dto = from_dict(data_class=CardAccountProductParamRequest,
                                                    data=product_details.get("card_account_params"))
                request_payload["card_account_params"] = dataclasses.asdict(card_account_params_dto)

            create_product_response = request.hugosave_post_request(
                path=ah.product_urls["create"],
                headers={},
                data=request_payload,
            )
            if not check_status_distribute(create_product_response, "200"):
                assert (
                    False
                ), f"unable to create product: \t {create_product_response}"
            context.data["created_products"] = {}
            context.data["created_products"][product_code] = (
                create_product_response["data"]
            )
    except FileNotFoundError:
        print(yaml_file_path)
        raise FileNotFoundError(f"YAML file not found at path: {yaml_file_path}")
    except Exception as e:
        raise Exception(f"An error occurred during card creation': {e}")


@Step("I check the product status for ([^']*)")
def check_product_status(context, product_code):
    create_product_response = context.data["created_products"].get(product_code)
    product_status = create_product_response.get("productStatus")
    expected_status = "PRODUCT_SUCCESS"
    if not product_status == expected_status:
        assert (
            False
        ), f"Product status is not '{expected_status}'. Actual status: '{product_status}'."
    else:
        print(f"Product status successfully verified as '{expected_status}'.")


@Step("I request for the activation of the product ([^']*)")
def activate_product(context, product_code):
    request = context.request

    product_data_for_activation = context.data["created_products"].get(product_code)
    product_id = product_data_for_activation.get("productId")
    if not product_id:
        raise ValueError(f"Missing 'productId' in product data for '{product_code}' during approval. Data: {product_data_for_activation}")
    approve_product_response = request.hugosave_put_request(
        path=ah.product_urls["approve"].replace("{product-id}", product_id),
        headers={},
    )
    assert check_status_distribute(approve_product_response, "200"), f"unable to approve product: \t {approve_product_response}"
    time.sleep(2)


@Step("I create transaction codes for the product ([^']*) from ([^']*)")
def create_transaction_code(context, product_code, yaml_file_name):
    request = context.request

    create_product_response = context.data["created_products"].get(product_code)
    product_id = create_product_response.get("productId")
    try:
        script_dir = os.path.dirname(os.path.abspath(__file__))
        product_factory_dir = os.path.join(script_dir, "product_factory")
        yaml_file_path = os.path.join(product_factory_dir, yaml_file_name)

        with open(yaml_file_path, 'r') as f:
            product_data = yaml.safe_load(f)

        if product_data is None:
            raise ValueError(f"YAML file '{yaml_file_path}' is empty or invalid.")

        print(f"Creating transaction codes by using data from '{yaml_file_path}'")

        service = product_data.get("service")
        service_products_list = service.get("products")
        for product in service_products_list:
            if not product.get("transaction_codes") is None:
                for request_payload in product.get("transaction_codes"):
                    create_transaction_code_response = request.hugosave_post_request(
                        path=ah.product_urls["transaction_code"].replace("{product-id}", product_id),
                        headers={},
                        data=request_payload,
                    )
                    assert check_status_distribute(create_transaction_code_response, "200"), f"unable to create transaction codes: \t {create_transaction_code_response}"
                    context.data["create_transaction_code_response"] = {}
                    context.data["create_transaction_code_response"][product_code] = (
                        create_transaction_code_response["data"]
                    )
                    time.sleep(2)
    except FileNotFoundError:
        raise FileNotFoundError(f"YAML file not found at path: {yaml_file_path}")
    except Exception as e:
        raise Exception(f"An error occurred during card creation: {e}")
