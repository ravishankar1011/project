Feature: LOS service's Journey scenarios

  Background: Set Customer Profile

    Given I set and verify customer Cid1, customer profile CPid1 in the context

    Then I onboard Customer Profile Cid1 to LOS and verify onboard status as ONBOARD_SUCCESS

    Then I create following LOS Params and verify status
      | condition_config_case | is_active | description  | status_code | param_identifier |
      | valid_region_case     | true      | region param | 200         | PARAM_1          |

  Scenario: Successful LOSJourney Creation

    Then I create following LOS Journey and verify status as 200
      | journey_name | description | rules_case | param_code | journey_code | journey_identifier |
      | journey_1    | journey     | valid_case | PARAM_1    | JC1          | JOUR1              |

  Scenario: LOS Journey Creation failed because of using unsupported operators in rules

    Then I create following LOS Journey and verify status as E9400
      | journey_name | description | rules_case                | param_code | journey_code |
      | journey_1    | journey     | unsupported_operator_used | PARAM_1    | JC1          |

  Scenario: LOS Journey Creation failed because of using invalid type for value

      Then I create following LOS Journey and verify status as E9400
        | journey_name | description | rules_case        | param_code | journey_code |
        | journey_1    | journey     | invalid_type_used | PARAM_1    | JC1          |

  Scenario: LOS Journey Creation failed because of missing mandatory fields

    Then I create following LOS Journey and verify status as E9400
      | journey_name | description | rules_case               | param_code | journey_code |
      | journey_1    | journey     | missing_mandatory_fields | PARAM_1    | JC1          |

  Scenario: LOS Journey Creation failed because of weightage less than 100

    Then I create following LOS Journey and verify status as E9400
      | journey_name | description | rules_case                | param_code | journey_code |
      | journey_1    | journey     | total_weightage_under_100 | PARAM_1    | JC1          |

  Scenario: LOS Journey Creation failed because of empty journey rules

    Then I create following LOS Journey and verify status as E9400
      | journey_name | description | rules_case          | param_code | journey_code |
      | journey_1    | journey     | empty_journey_rules | PARAM_1    | JC1          |

  Scenario: LOS Journey Creation failed because of unknow LOS param

    Then I create following LOS Journey and verify status as E9400
      | journey_name | description | rules_case         | param_code | journey_code |
      | journey_1    | journey     | unknown_param_code | PARAM_2    | JC1          |

  Scenario: LOS Journey Creation failed because of duplicate los param

    Then I create following LOS Journey and verify status as E9400
      | journey_name | description | rules_case           | param_code | journey_code |
      | journey_1    | journey     | duplicate_param_code | PARAM_1    | JC1          |

  Scenario: LOS Journey Creation failed because of duplicate los param

    Then I create following LOS Journey and verify status as E9500
      | journey_name | description | rules_case               | param_code | journey_code |
      | journey_1    | journey     | unknown_customer_profile | PARAM_1    | JC1          |

  Scenario: Successful LOS journey params retrieval for a journey code

    Then I create following LOS Journey and verify status as 200
      | journey_name | description | rules_case | param_code | journey_code | journey_identifier |
      | journey_1    | journey     | valid_case | PARAM_1    | JC2          | JOUR1              |

    Then I get Journey params for a journey code JC2 and verify status as 200

  Scenario: LOS Journey Params Retrieval failed for a unknown Journey code
    Then I get Journey params for a journey code JC12 and verify status as LOSM_9602

  Scenario: Successful Applications retrieval for a journey

    Then I create following LOS Journey and verify status as 200
      | journey_name | description | rules_case | param_code | journey_code | journey_identifier |
      | journey_1    | journey     | valid_case | PARAM_1    | JC3          | JOUR1              |

    Then I create following LOS Application and verify status as 200
      | application_identifier | journey_code |  | end_customer_profile_id | input_data_case |
      | AID1                   | JC3          |  | ECPid1                  | VALID_CASE      |

    Then I get applications for a journey code JC3 and verify journey id JOUR1 and status as 200

  Scenario: LOS Journey Application retrieval failed for a unknown journey code
    Then I get applications for a journey code JC12 and verify journey id JOUR1 and status as LOSM_9602
