Feature: LOS service's Application scenarios

  Background: Set Customer Profile

    Given I set and verify customer Cid1, customer profile CPid1 in the context

    Then I onboard Customer Profile Cid1 to LOS and verify onboard status as ONBOARD_SUCCESS

    Then I create below End-Customer-Profile
      | customer_identifier | customer_profile_identifier | end_customer_profile_identifier | first_name   | last_name   | region   | email         | phone_number   |
      | Cid1                | CPid1                       | ECPid1                          | John         | Snow        | SG       | john@snow.com | +63 1234567890 |

    Then I verify End-Customer-Profile exist with values
      | customer_profile_identifier | end_customer_profile_identifier | first_name | last_name | email         | phone_number   | status |
      | CPid1                       | ECPid1                          | John       | Snow      | john@snow.com | +63 1234567890 | ACTIVE |

    Then I onboard End Customer Profile ECPid1 to LOS and verify onboard status as ONBOARD_SUCCESS and status code as 200

    Then I create following LOS Params and verify status
      | param_identifier | condition_config_case | is_active | description  | status_code |
      | PARAM_1          | valid_region_case     | true      | region param | 200         |
      | PARAM_2          | valid_age_case        | true      | age param    | 200         |

    Then I create following LOS Journey and verify status as 200
      | journey_name | description | rules_case | param_code | journey_code | journey_identifier |
      | journey_1    | journey     | valid_case | PARAM_1    | JC1          | JOUR1              |

  Scenario: Successful LOS Application Creation
    Then I create following LOS Application and verify status as 200
      | journey_code | end_customer_profile_id | input_data_case | application_identifier |
      | JC1          | ECPid1                  | VALID_CASE      | APN1                   |

  Scenario: Attempt to Create LOS Application with missing mandatory fields in the request
   Then I create following LOS Application and verify status as E9400
     | journey_code | end_customer_profile_id | input_data_case    |
     | JC1          | ECPid1                  | MISSING_INPUT_DATA |

  Scenario: Attempt to create LOS Application with unknow customer profile id
    Then I create following LOS Application and verify status as E9500
      | journey_code | end_customer_profile_id | input_data_case  |
      | JC1          | ECPid2                  | UNKNOWN_CUSTOMER |

  Scenario: Attempt to Create LOS Application with unknow journey_code
    Then I create following LOS Application and verify status as LOSM_9602
      | journey_code | end_customer_profile_id | input_data_case |
      | JC2          | ECPid1                  | VALID_CASE      |

  Scenario: Attempt to Create LOS Application with unknown LOS param
    Then I create following LOS Application and verify status as E9400
      | journey_code | end_customer_profile_id | input_data_case             |
      | JC1          | ECPid1                  | UNKNOWN_PARAM_IN_INPUT_DATA |

  Scenario: Attempt to Create LOS Application with Wrong input data for a param
      Then I create following LOS Application and verify status as E9400
        | journey_code | end_customer_profile_id | input_data_case   |
        | JC1          | ECPid1                  | WRONG_INPUT_VALUE |

  Scenario: Attempt to Create LOS Application with undefined journey param
    Then I create following LOS Application and verify status as E9400
      | journey_code | end_customer_profile_id | input_data_case                       |
      | JC1          | ECPid1                  | UNDEFINED_JOURNEY_PARAM_IN_INPUT_DATA |

  Scenario: Successful Application Evaluation
    Then I create following LOS Application and verify status as 200
      | application_identifier | journey_code |  | end_customer_profile_id | input_data_case |
      | AID1                   | JC1          |  | ECPid1                  | VALID_CASE      |
    Then I Evaluate Application AID1 and verify status as 200

  Scenario: Attempt to Evaluate Unknow Application
      Then I Evaluate Application AID2 and verify status as LOSM_9603
