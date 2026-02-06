import os
import subprocess
import sys
import time
from concurrent.futures import ALL_COMPLETED, ThreadPoolExecutor, wait
from enum import Enum
from glob import glob

from behave.parser import parse_file


class IntegrationTestProduct(Enum):
    # API tests
    # Aggregate
    card = (500, "tests/api/aggregate/scenarios/card")
    cash = (500, "tests/api/aggregate/scenarios/cash")
    cms = (500, "tests/api/aggregate/scenarios/cms")
    los = (500, "tests/api/aggregate/scenarios/los")
    coa = (500, "tests/api/aggregate/scenarios/coa")
    compliance = (500, "tests/api/aggregate/scenarios/compliance")
    core = (500, "tests/api/aggregate/scenarios/core")
    cos = (500, "tests/api/aggregate/scenarios/cos")
    investment = (500, "tests/api/aggregate/scenarios/investment")
    ledger = (500, "tests/api/aggregate/scenarios/ledger")
    notification = (500, "tests/api/aggregate/scenarios/notification")
    payment = (500, "tests/api/aggregate/scenarios/payment")
    profile = (500, "tests/api/aggregate/scenarios/profile")

    # Distribute
    app = (500, "tests/api/distribute/scenarios/app")
    behavioural = (500, "tests/api/distribute/scenarios/behavioural")

    # UI tests
    sg_automation = (20, "tests/ui/sg_automation/features")


class ParallelBehave:
    def __init__(self, product: IntegrationTestProduct, tag_expr: str = None):
        self.product = product
        self.threads = product.value[0]
        self.feature_dir = f"{os.getcwd()}/{product.value[1]}"
        self.tag_expr = tag_expr
        if not os.path.exists(f"{self.feature_dir}/environment.py"):
            FileNotFoundError(f"File {self.feature_dir}/environment.py not found")

        self.feature_files = glob(f"{self.feature_dir}/**/*.feature", recursive=True)
        self.scenarios = []
        for feature_file_path in self.feature_files:
            feature = parse_file(feature_file_path)
            for scenario in feature.scenarios:
                if scenario.keyword == "Scenario Outline":
                    for s in scenario.scenarios:
                        self.scenarios.append({
                            "name": s.name,
                            "file": feature_file_path,
                            "tags": [tag for tag in (feature.tags + scenario.tags)]
                        })
                else:
                    self.scenarios.append({
                        "name": scenario.name,
                        "file": feature_file_path,
                        "tags": [tag for tag in (feature.tags + scenario.tags)]
                    })

    def run(self):
        total_tests = len(self.scenarios)
        start_time = time.time()
        executor = ThreadPoolExecutor(self.threads)
        futures = [
            executor.submit(self.__run_test_case, each_case["name"], each_case["file"])
            for each_case in self.scenarios
        ]
        wait(futures, return_when=ALL_COMPLETED)

        success = sum(1 for f in futures if f.result())
        print(f"Took {int(time.time() - start_time)} Seconds")
        print(f"Coverage: {success}/{total_tests}")
        print(f"Percentage: {round(success / total_tests, 2)}")

        with open(os.path.join(os.getcwd(), f"{self.product.name}-passed.txt"), "w+") as f:
            f.write(str(success) + "\n")
            f.close()
        with open(os.path.join(os.getcwd(), f"{self.product.name}-total.txt"), "w+") as f:
            f.write(str(total_tests) + "\n")
            f.close()

        if success == total_tests:
            sys.exit(0)
        else:
            sys.exit(1)

    def __run_test_case(self, tc_name, feature_file_path) -> bool:
        tag_expr = f"-t {self.tag_expr}" if self.tag_expr else ""
        result = subprocess.run(
            [
                "behave",
                "--no-skipped",
                "-f",
                "allure_behave.formatter:AllureFormatter",
                "-o",
                "allure-test-results",
                feature_file_path,
                # tag_expr,
                "-n",
                tc_name,
            ],
        )
        return result.returncode == 0


if __name__ == "__main__":
    usage = (
        "python3 tests/integrations/parallel_behave.py <product_name> <no_of_processes>"
    )

    name = sys.argv[1]
    threads = sys.argv[2]
    product_name: IntegrationTestProduct = IntegrationTestProduct[name]
    ParallelBehave(product_name, None).run()
