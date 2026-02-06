import json
import logging
import subprocess
import time
import requests
import yaml

logger = logging.getLogger(__name__)
logger.setLevel(logging.NOTSET)

default_headers = {
    "Content-Type": "application/json",
    "Accept": "application/json",
}

MAX_RETRY_SERVER_ERROR = 3

class HugoportalTest:
    def __init__(self, config_file):
        self.params = self.__read_yaml(config_file)
        self.tokens = {}

        self.hugoportal_base_url = self.params["PORTAL_ENDPOINT"]
    def hugoportal_post_request(
            self, path: str, data: dict = None, headers: dict = None
    ):
        """To make post requests to Hugoportal endpoints"""
        return HugoportalTest.__do_post(
            HugoportalTest.__make_hugo_url(self, path), data, headers
        )

    def hugoportal_get_request(
            self, path: str, params: dict = None, headers: dict = None
    ):
        """To make get requests to Hugoportal endpoints"""
        return HugoportalTest.__do_get(
            HugoportalTest.__make_hugo_url(self, path), params, headers
        )

    def hugoportal_delete_request(
            self, path: str, data: dict = None, params: dict = None, headers: dict = None
    ):
        """To make delete requests to Hugoportal endpoints"""
        return HugoportalTest.__do_delete(
            HugoportalTest.__make_hugo_url(self, path), data, params, headers
        )

    def hugoportal_put_request(self, path: str, data: dict = None, headers: dict = None):
        """To make put requests to Hugoportal endpoints"""
        return HugoportalTest.__do_put(
            HugoportalTest.__make_hugo_url(self, path), data, headers
        )

    @staticmethod
    def __run_command(command):
        res = subprocess.run(command, shell=True, capture_output=True)
        res.check_returncode()
        return res.stdout.decode()

    @staticmethod
    def __read_yaml(yaml_file: str):
        with open(yaml_file, "r") as file:
            yaml_file = yaml.safe_load(file)
        return dict(yaml_file.items())

    @staticmethod
    def __make_hugo_url(self, path: str):
        return self.hugoportal_base_url + path

    @staticmethod
    def __do_post(url: str, body: dict = None, headers: dict = None):
        if headers is not None:
            headers = {**default_headers, **headers}
        else:
            headers = default_headers

        response = None
        for i in range(MAX_RETRY_SERVER_ERROR):
            response = requests.post(url, data=json.dumps(body), headers=headers)
            if response.status_code < 500:
                break
            time.sleep(5)
        response.raise_for_status()

        json_response = json.loads(response.text)
        # print(json_response)
        logger.debug(f"POST URL:{url}, Response: {json_response}")

        return json_response

    @staticmethod
    def __do_get(url: str, params: dict = None, headers: dict = None):
        if headers is not None:
            headers = {**default_headers, **headers}
        else:
            headers = default_headers

        logger.debug(f"GET URL:{url}, headers: {headers}, Params: {params}")

        response = None
        for i in range(MAX_RETRY_SERVER_ERROR):
            response = requests.get(url, params=params, headers=headers)
            if response.status_code < 500:
                break
            time.sleep(5)
        response.raise_for_status()

        json_response = json.loads(response.text)

        logger.debug(f"GET URL:{url}, Response: {json_response}")

        return json_response

    @staticmethod
    def __do_delete(
            url: str, body: dict = None, params: dict = None, headers: dict = None
    ):
        if headers is not None:
            headers = {**default_headers, **headers}
        else:
            headers = default_headers

        logger.debug(
                f"DELETE URL:{url}, Headers: {headers}, Body: {body}, params: {params}"
        )

        response = None
        for i in range(MAX_RETRY_SERVER_ERROR):
            response = requests.delete(
                url, data=json.dumps(body), params=params, headers=headers
            )
            if response.status_code < 500:
                break
            time.sleep(5)
        response.raise_for_status()

        json_response = json.loads(response.text)

        logger.debug(f"DELETE URL:{url}, Response: {json_response}")

        return json_response

    @staticmethod
    def __do_put(url: str, body: dict = None, headers: dict = None):
        if headers is not None:
            headers = {**default_headers, **headers}
        else:
            headers = default_headers

        logger.debug(f"PUT URL:{url}, Headers: {headers}, Body: {body}")

        response = None
        for i in range(MAX_RETRY_SERVER_ERROR):
            response = requests.put(url, data=json.dumps(body), headers=headers)
            if response.status_code < 500:
                break
            time.sleep(5)
        response.raise_for_status()

        json_response = json.loads(response.text)

        logger.debug(f"PUT URL:{url}, Response: {json_response}")

        return json_response
