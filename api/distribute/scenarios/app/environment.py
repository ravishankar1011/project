from tests.api.distribute.hugosave_test import HugosaveTest
import time
import tests.api.distribute.app_helper as ah


def before_scenario(context, scenario):
    current_time = int(time.time())
    config_yaml_path = f"{context.config.base_dir}/../../config.yaml"
    context.request = HugosaveTest(config_yaml_path)
    config_data = context.request.params
    # For sharing contextual data for each scenario
    context.data = {"config_data": config_data}
    distribute_endpoint = context.data["config_data"]["DISTRIBUTE_ENDPOINT"]
    context.data["org_id"] = ah.determine_org_id(distribute_endpoint)
