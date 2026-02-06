from tests.api.portal.hugoportal_test import HugoportalTest

def before_scenario(context, scenario):
    config_yaml_path = f"{context.config.base_dir}/../../config.yaml"
    context.request = HugoportalTest(config_yaml_path)
    config_data = context.request.params
    context.data = {"config_data": config_data}
