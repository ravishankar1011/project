Feature: LOS service's customer profile scenarios

  Background: Set Customer Profile

    Given I set and verify customer Cid1, customer profile CPid1 in the context

  Scenario: Onboard Customer Profile

    Then I onboard Customer Profile Cid1 to LOS and verify onboard status as ONBOARD_SUCCESS

  Scenario: Successful Retrieval of LOS journeys for a customer
    Then I create following LOS Params and verify status
      | condition_config_case | is_active | description  | status_code | param_identifier |
      | valid_region_case     | true      | region param | 200         | PARAM_1          |

    Then I create following LOS Journey and verify status as 200
      | journey_name | description  | rules_case | param_code | journey_code | journey_identifier |
      | journey_1    | journey  one | valid_case | PARAM_1    | JC1          | JOUR1              |
      | journey_2    | journey  two | valid_case | PARAM_1    | JC2          | JOUR1              |

    Then I get LOS Journeys for the customer and verify status as 200
