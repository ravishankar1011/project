Feature: LOS service's Param scenarios

  Background: Set Customer Profile

    Given I set and verify customer Cid1, customer profile CPid1 in the context

    Then I onboard Customer Profile Cid1 to LOS and verify onboard status as ONBOARD_SUCCESS

  Scenario:
    Then I create following LOS Params and verify status
      | condition_config_case | is_active | description | status_code | param_identifier |
      | valid_age_case        | true      | age param   | 200         | PARAM_1          |
