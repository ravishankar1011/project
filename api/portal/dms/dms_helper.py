dms_base_url = "/dms/v1"

api_urls = {
    "add_api" : dms_base_url + "/api/add",
    "get_api": dms_base_url + "/api",
    "add_fields": dms_base_url + "/api"
}

field_urls = {
    "create_field": dms_base_url + "/field",
    "get_field": dms_base_url + "/field",
    "update_field": dms_base_url + "/field"
}
def get_principal_id_and_access_key():
    return {
        "x-principal-id": "SUPER_ADMIN",
        "x-principal-access-key": "         "
    }

def generate_random_string(length = 8):
    import random
    import string
    return ''.join(random.choices(string.ascii_lowercase, k=length))

api_request_dto = {
    "api_details": {
        "url": "it url",
        "api_name": "it api",
        "api_description": "Portal: it api",
        "api_code": "",
        "data_provider_id": "",
        "http_method": "GET",
        "api_type": "PAGINATED_READ_API",
        "pagination_details": {
            "pagination_mode": "TOKENIZED",
            "paginated_data_path": "data.group",
            "token_pagination_details": {
                "page_token_path": "pageToken",
                "has_more_pages_path": "hasMorePages",
                "reverse_page_token_path": "reversePageToken",
                "has_more_reverse_pages_path": "hasMoreReversePages"
            }
        }
    },
    "fields": [
        {
            "field_name": "it field",
            "field_description": "it field",
            "field_code": "",
            "fieldType": "OUTPUT",
            "dataType": "STRING",
            "field_order": 7,
            "mapping_path": {
                "requestMappingPath": "",
                "responseMappingPath": "customerProfileId",
                "requestFieldPosition": ""
            }
        }
    ]

}

field_request_dto = {
    "field_name": "test field",
    "field_description": "test field",
    "field_code": "",
    "api_id": "",
    "fieldType": "OUTPUT",
    "dataType": "STRING",
    "field_order": 5,
    "mapping_path": {
        "requestMappingPath": "",
        "responseMappingPath": "testField",
        "requestFieldPosition": ""
    },
    "dependent_field_codes":[]
}
