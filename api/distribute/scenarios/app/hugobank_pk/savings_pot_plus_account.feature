Feature: Savings Pot for PLUS account

  Background: Create a new HUGOBANK PLUS account

    # user 1
    Given The user UID1 provides a valid mobile number on device_1 to initiate onboarding and the expected status is VERIFICATION_INITIATED
      | user_name | user_name_type | ph_prefix |
      | random    | PHONE_NUMBER   | +373      |

    Then The user UID1 submits OTP to proceed with verification and expects a status code of 200 and a status of VERIFICATION_SUCCESS

    Given I open a new HUGOBANK user account and expect the status code 200
      | user_profile_identifier | email          | legal_name | name   | account_type |
      | UID1                    | test@gmail.com | John Doe   | Johnny | PERSONAL     |

    Then I initiate the initial onboarding of the user UID1 and expect a status INITIATED

    Then I initiate the initial onboarding journey HUGOBANK_VERISYS within the ID_VERIFICATION_STEP for the user UID1 and expect a status of JOURNEY_INITIATED

    Then I update HUGOBANK_VERISYS journey within the ID_VERIFICATION_STEP for user UID1 as pass

    Then I process the initial onboarding journey HUGOBANK_VERISYS within the ID_VERIFICATION_STEP for user UID1, and expect a status JOURNEY_PROCESSED

    Then I check status of the initial onboarding journey HUGOBANK_VERISYS within the ID_VERIFICATION_STEP for the user UID1, the status should be JOURNEY_PROCESSED

    Then I submit the initial onboarding journey HUGOBANK_VERISYS within the ID_VERIFICATION_STEP for the user UID1 and expect the journey status to be JOURNEY_SUBMITTED

    Then I check status of the initial onboarding journey HUGOBANK_VERISYS within the ID_VERIFICATION_STEP for the user UID1, the status should be JOURNEY_SUCCESSFUL

    Then I initiate the initial onboarding journey HUGOBANK_BIO_VERISYS within the BIOMETRIC_VERIFICATION_STEP for the user UID1 and expect a status of JOURNEY_INITIATED

    Then I update HUGOBANK_BIO_VERISYS journey within the BIOMETRIC_VERIFICATION_STEP for user UID1 as pass

    Then I process the initial onboarding journey HUGOBANK_BIO_VERISYS within the BIOMETRIC_VERIFICATION_STEP for user UID1, and expect a status JOURNEY_PROCESSED

    Then I check status of the initial onboarding journey HUGOBANK_BIO_VERISYS within the BIOMETRIC_VERIFICATION_STEP for the user UID1, the status should be JOURNEY_PROCESSED

    Then I submit the initial onboarding journey HUGOBANK_BIO_VERISYS within the BIOMETRIC_VERIFICATION_STEP for the user UID1 and expect the journey status to be JOURNEY_SUBMITTED

    Then I submit the initial onboarding for UID1, the onboarding status should be IN_PROGRESS and the account level should be L1

    And I check the status of initial onboarding for UID1 and expect a onboarding status of COMPLETED

    And I get user details for user UID1 and the user profile status should be PROFILE_IN_PROGRESS

    Then I check the authorisation status of the device_1 for the user UID1 and expect a device authorisation status of DEVICE_AUTHORISATION_SUCCESS

    And Create a binding signature for the user UID1 to bind the device_1 and the device binding status should be ACTIVE

    Then I list all user devices for user UID1 and the user should have device_1

    And I check the user details to confirm if user UID1 is L1 and the user profile status should be PROFILE_ACTIVE

    When I initiate progress onboarding for the user UID1 to upgrade the account to L2 and expect an onboarding status of INITIATED

    Then I initiate the progress onboarding journey HUGOBANK_VERIFY_INCOME within the INCOME_VERIFICATION_STEP for the user UID1 and expect a status of JOURNEY_INITIATED

    Then I upload document1 for salaryDetails for the HUGOBANK_VERIFY_INCOME journey for user UID1 as the fundsProof

    Then I upload document2 for salaryDetails for the HUGOBANK_VERIFY_INCOME journey for user UID1 as the fundsProof

    Then I upload document3 for salaryDetails for the HUGOBANK_VERIFY_INCOME journey for user UID1 as the fundsProof

    Then I upload document1 for salaryDetails for the HUGOBANK_VERIFY_INCOME journey for user UID1 as the employmentProof

    Then I upload document2 for salaryDetails for the HUGOBANK_VERIFY_INCOME journey for user UID1 as the employmentProof

    Then I upload document3 for salaryDetails for the HUGOBANK_VERIFY_INCOME journey for user UID1 as the employmentProof

    Then I process the progress onboarding journey HUGOBANK_VERIFY_INCOME within the INCOME_VERIFICATION_STEP for user UID1, and expect a status JOURNEY_HOLD

    Then I update the HUGOBANK_VERIFY_INCOME journey status within the INCOME_VERIFICATION_STEP as ACCEPT if operator action status is OPERATOR_ACTION_REQUIRED for user UID1

    Then I submit the progress onboarding for user UID1, the onboarding status should be IN_PROGRESS and the account level should be L2

    Given I update the onboarding status as ACCEPT if operator action status is OPERATOR_ACTION_REQUIRED for user UID1 to upgrade the account to level L2

    And I check progress onboarding status for the user UID1, the onboardingStatus status should be COMPLETED

    And I get user details for user UID1 and the user profile status should be PROFILE_ACTIVE

    And I check the user details to confirm if user UID1 is L2 and the user profile status should be PROFILE_ACTIVE

  Scenario Outline: Invest, Withdraw

    Given I create a Map MPID1 and expect a status of MAP_CREATED
      | user_profile_identifier | name   | asset_allocation_details                  | allocation_type | goal_date  | goal_amount |
      | UID1                    | random | [{"asset_id": "CASH" ,"percentage": 100}] | FIXED           | 03-06-2024 | 70000       |

    Then I check if the map MPID1 is created for user UID1 and expect a status of MAP_CREATED

    Given I withdraw from map MPID1 and expect a status of PENDING
      | user_profile_identifier | transaction_amount | withdraw_amount | fee_amount | status_code |
      | UID1                    | 7                  | 7               | 0          | 200         |

    Then I get the user cash wallets for the user UID1 and expect the account status of CASH_ACCOUNT_STATUS_CREATED

    Then I check if the intent with type CASH_MAP_WITHDRAW has the status DECLINED and a total of 1 intents exist for the user UID1 in the cash view

    And I check the balance of the wallet with product code CASH_WALLET_CURRENT for user UID1 and the balance should be 0 PKR exact

    Then I deposit 60000 PKR into wallet with product code CASH_WALLET_CURRENT for user UID1 and expect a status code of 200

    And I check the balance of the wallet with product code CASH_WALLET_CURRENT for user UID1 and the balance should be 60000 PKR exact

    Then I check if the intent with type EXTERNAL_DEPOSIT has the status SETTLED and a total of 1 intents exist for the user UID1 in the cash view

    Given I invest in map MPID1 and expect a status of PENDING
      | user_profile_identifier | transaction_amount | investment_amount | fee_amount | status_code |
      | UID1                    | 50500              | 50500             | 0          | 200         |

    Then I check the balance of map MPID1 of user UID1 to be 50500 PKR

    And I check the balance of the wallet with product code CASH_WALLET_CURRENT for user UID1 and the balance should be 9500 PKR exact

    Then I check if the intent with type CASH_MAP_INVEST has the status SETTLED and a total of 1 intents exist for the user UID1 in the cash view

    Then I check if the intent with type CASH_MAP_INVEST has the status SETTLED and a total of 1 intents exist for the user UID1 in the map_intent_view,MPID1 view

    Given I withdraw from map MPID1 and expect a status of PENDING
      | user_profile_identifier | transaction_amount | withdraw_amount | fee_amount | status_code |
      | UID1                    | 7                  | 7               | 0          | 200         |

    Then I check the balance of map MPID1 of user UID1 to be 50493 PKR

    Then I check if the intent with type CASH_MAP_WITHDRAW has the status DECLINED and a total of 1 intents exist for the user UID1 in the cash view

    Then I check if the intent with type CASH_MAP_WITHDRAW has the status SETTLED and a total of 1 intents exist for the user UID1 in the map_intent_view,MPID1 view

    Then I update the map MPID1 and check if update was successful
      | user_profile_identifier | name       | goal_date  | goal_amount | status_code |
      | UID1                    | Investment | 30-04-2024 | 60000.0     | 200         |

    Given I invest in map MPID1 and expect a status of Insufficient Balance.
      | user_profile_identifier | transaction_amount | investment_amount | fee_amount | status_code |
      | UID1                    | 111180             | 111180            | 0          | HSA_9145    |

    Given I withdraw from map MPID1 and expect a status of PENDING
      | user_profile_identifier | transaction_amount | withdraw_amount | fee_amount | status_code |
      | UID1                    | 50500              | 50500           | 0          | 200         |

    Then I check if the intent with type CASH_MAP_WITHDRAW has the status DECLINED and a total of 2 intents exist for the user UID1 in the cash view

    Given I invest in map MPID1 and expect a status of Invalid map id
      | user_profile_identifier | transaction_amount | investment_amount | fee_amount | status_code | invalid_map |
      | UID1                    | 50500              | 50500             | 0          | HSA_9107    | Y           |

    Given I withdraw from map MPID1 and expect a status of Invalid map id
      | user_profile_identifier | transaction_amount | withdraw_amount | fee_amount | status_code | invalid_map |
      | UID1                    | 9500               | 9500            | 0          | HSA_9107    | Y           |

    Then I update the map MPID1 and check if update was successful
      | user_profile_identifier | name       | goal_date  | goal_amount | status_code | invalid_map |
      | UID1                    | Investment | 30-04-2024 | 75000.5     | HSA_9107    | Y           |

    Then I delete the map MPID1 of user UID1 and expect a status code of 200

    Then I check if the cash map MPID1 is deleted successfully for user UID1

    And I check the balance of the wallet with product code CASH_WALLET_CURRENT for user UID1 and the balance should be 60000 PKR exact

    Then I check if the intent with type CASH_MAP_FULL_WITHDRAW has the status SETTLED and a total of 1 intents exist for the user UID1 in the cash view
    Examples:
      | org-id      |
      | HUGOSAVE_SG |

  Scenario: Create Schedule, Trigger Schedule, Delete Schedule

    Then I get the user cash wallets for the user UID1 and expect the account status of CASH_ACCOUNT_STATUS_CREATED

    Then I deposit 60000 PKR into wallet with product code CASH_WALLET_CURRENT for user UID1 and expect a status code of 200

    And I check the balance of the wallet with product code CASH_WALLET_CURRENT for user UID1 and the balance should be 60000 PKR exact

    Given I create a Map MPID1 and expect a status of MAP_CREATED
      | user_profile_identifier | name | asset_allocation_details                  | allocation_type | goal_date  | goal_amount |
      | UID1                    | Bike | [{"asset_id": "CASH" ,"percentage": 100}] | FIXED           | 03-06-2024 | 70000       |

    Then I check if the map MPID1 is created for user UID1 and expect a status of MAP_CREATED

    Then I create a schedule for map MPID1 and expect status 200
      | user_profile_identifier | schedule_identifier | frequency | schedule_type       | product_code     | target_weekdays | target_week | amount |
      | UID1                    | SID1                | DAILY     | SCHEDULE_MAP_INVEST | CASH_WALLET_SAVE |                 | 1           | 50500  |

    Then I check if the schedule SID1 has a status code of 200 and a status of SCHEDULE_STATUS_ACTIVE for user UID1

    Then I trigger schedule SID1 for user UID1 and expect a status code of 200

    And I check the balance of the wallet with product code CASH_WALLET_CURRENT for user UID1 and the balance should be 9500 PKR approx

    Then I check the balance of map MPID1 of user UID1 to be 50500 PKR

    Then I check if the intent with type SCHEDULE_CASH_MAP_INVEST has the status SETTLED and a total of 1 intents exist for the user UID1 in the map_intent_view,MPID1 view

    Then I delete schedule SID1 for user UID1 and expect a status code of 200

    Then I check if the schedule SID1 has a status code of HSA_9108 and a status of no_status_check_required for user UID1

    Given I create a Map MPID2 and expect a status of MAP_CREATED
      | user_profile_identifier | name   | asset_allocation_details                  | allocation_type | goal_date  | goal_amount |
      | UID1                    | Camera | [{"asset_id": "CASH" ,"percentage": 100}] | FIXED           | 03-06-2024 | 70000       |

    Then I check if the map MPID2 is created for user UID1 and expect a status of MAP_CREATED

    Then I create a schedule for map MPID2 and expect status 200
      | user_profile_identifier | schedule_identifier | frequency | schedule_type       | product_code     | target_weekdays | target_week | amount |
      | UID1                    | SID2                | WEEKLY    | SCHEDULE_MAP_INVEST | CASH_WALLET_SAVE |                 | 1           | 5000   |

    Then I check if the schedule SID2 has a status code of 200 and a status of SCHEDULE_STATUS_ACTIVE for user UID1

    Then I trigger schedule SID2 for user UID1 and expect a status code of 200

    And I check the balance of the wallet with product code CASH_WALLET_CURRENT for user UID1 and the balance should be 4500 PKR approx

    Then I check the balance of map MPID2 of user UID1 to be 5000 PKR

    Then I check if the intent with type SCHEDULE_CASH_MAP_INVEST has the status SETTLED and a total of 1 intents exist for the user UID1 in the map_intent_view,MPID2 view

    Then I delete schedule SID2 for user UID1 and expect a status code of 200

    Then I check if the schedule SID2 has a status code of HSA_9108 and a status of no_status_check_required for user UID1

  Scenario: Skip Schedule

    Then I get the user cash wallets for the user UID1 and expect the account status of CASH_ACCOUNT_STATUS_CREATED

    Then I deposit 200000 PKR into wallet with product code CASH_WALLET_CURRENT for user UID1 and expect a status code of 200

    And I check the balance of the wallet with product code CASH_WALLET_CURRENT for user UID1 and the balance should be 200000 PKR exact

    Given I create a Map MPID1 and expect a status of MAP_CREATED
      | user_profile_identifier | name | asset_allocation_details                  | allocation_type | goal_date  | goal_amount |
      | UID1                    | Car  | [{"asset_id": "CASH" ,"percentage": 100}] | FIXED           | 03-06-2025 | 70000       |

    Then I check if the map MPID1 is created for user UID1 and expect a status of MAP_CREATED

    Then I create a schedule for map MPID1 and expect status 200
      | user_profile_identifier | schedule_identifier | frequency | schedule_type       | product_code     | target_weekdays | target_week | amount |
      | UID1                    | SID1                | DAILY     | SCHEDULE_MAP_INVEST | CASH_WALLET_SAVE |                 | 1           | 50500  |

    Then I check if the schedule SID1 has a status code of 200 and a status of SCHEDULE_STATUS_ACTIVE for user UID1

    Then I check schedule status as SCHEDULE_STATUS_ACTIVE for schedule SID1 for user UID1

    Then I check schedule status as ACTIVE for upcoming schedule SID1 for user UID1

    Then I skip the schedule SID1 for user UID1 and expect a status of SR_REMARK_TO_BE_SKIPPED

    Then I check schedule status as SR_REMARK_TO_BE_SKIPPED for upcoming schedule SID1 for user UID1

    Then I trigger schedule SID1 for user UID1 and expect a status code of 200

    And I check the balance of map MPID1 of user UID1 to be 0 PKR

    Then I check if the upcoming schedule date is updated for schedule SID1 for user UID1

    Then I check schedule status as ACTIVE for upcoming schedule SID1 for user UID1

    Then I invest in map MPID1 and expect a status of PENDING
      | user_profile_identifier | transaction_amount | investment_amount | fee_amount | status_code |
      | UID1                    | 50500              | 50500             | 0          | 200         |

    Then I check the balance of map MPID1 of user UID1 to be 50500 PKR

    Then I delete schedule SID1 for user UID1 and expect a status code of 200

    Then I check if the schedule SID1 has a status code of HSA_9108 and a status of no_status_check_required for user UID1

    Given I create a Map MPID2 and expect a status of MAP_CREATED
      | user_profile_identifier | name  | asset_allocation_details                  | allocation_type | goal_date  | goal_amount |
      | UID1                    | Phone | [{"asset_id": "CASH" ,"percentage": 100}] | FIXED           | 03-06-2025 | 10000       |

    Then I check if the map MPID2 is created for user UID1 and expect a status of MAP_CREATED

    Then I create a schedule for map MPID2 and expect status 200
      | user_profile_identifier | schedule_identifier | frequency | schedule_type       | product_code     | target_weekdays | target_week | amount |
      | UID1                    | SID2                | WEEKLY    | SCHEDULE_MAP_INVEST | CASH_WALLET_SAVE |                 | 1           | 5000   |

    Then I check if the schedule SID2 has a status code of 200 and a status of SCHEDULE_STATUS_ACTIVE for user UID1

    Then I check schedule status as SCHEDULE_STATUS_ACTIVE for schedule SID2 for user UID1

    Then I check schedule status as ACTIVE for upcoming schedule SID2 for user UID1

    Then I skip the schedule SID2 for user UID1 and expect a status of SR_REMARK_TO_BE_SKIPPED

    Then I check schedule status as SR_REMARK_TO_BE_SKIPPED for upcoming schedule SID2 for user UID1

    Then I trigger schedule SID2 for user UID1 and expect a status code of 200

    And I check the balance of map MPID2 of user UID1 to be 5000 PKR

    Then I check if the upcoming schedule date is updated for schedule SID2 for user UID1

    Then I check schedule status as ACTIVE for upcoming schedule SID2 for user UID1

    Then I invest in map MPID2 and expect a status of PENDING
      | user_profile_identifier | transaction_amount | investment_amount | fee_amount | status_code |
      | UID1                    | 500.32             | 500.32            | 0          | 200         |

    Then I check the balance of map MPID2 of user UID1 to be 5500.32 PKR

    Then I delete schedule SID2 for user UID1 and expect a status code of 200

    Then I check if the schedule SID2 has a status code of HSA_9108 and a status of no_status_check_required for user UID1

  Scenario: Update/Edit Schedule

    Then I get the user cash wallets for the user UID1 and expect the account status of CASH_ACCOUNT_STATUS_CREATED

    Then I deposit 60000 PKR into wallet with product code CASH_WALLET_CURRENT for user UID1 and expect a status code of 200

    And I check the balance of the wallet with product code CASH_WALLET_CURRENT for user UID1 and the balance should be 60000 PKR exact

    Given I create a Map MPID1 and expect a status of MAP_CREATED
      | user_profile_identifier | name  | asset_allocation_details                  | allocation_type | goal_date  | goal_amount |
      | UID1                    | House | [{"asset_id": "CASH" ,"percentage": 100}] | FIXED           | 03-06-2024 | 70000       |

    Then I check if the map MPID1 is created for user UID1 and expect a status of MAP_CREATED

    Then I create a schedule for map MPID1 and expect status 200
      | user_profile_identifier | schedule_identifier | frequency | schedule_type       | product_code     | target_weekdays | target_week | amount |
      | UID1                    | SID1                | DAILY     | SCHEDULE_MAP_INVEST | CASH_WALLET_SAVE |                 | 1           | 4.56   |

    Then I check if the schedule SID1 has a status code of 200 and a status of SCHEDULE_STATUS_ACTIVE for user UID1

    Then I update the schedule for map MPID1 and expect status 200
      | user_profile_identifier | schedule_identifier | frequency | schedule_type       | product_code     | target_weekdays | target_week | amount |
      | UID1                    | SID1                | WEEKLY    | SCHEDULE_MAP_INVEST | CASH_WALLET_SAVE |                 | 1           | 6      |

  Scenario: Stop Schedule

    Then I get the user cash wallets for the user UID1 and expect the account status of CASH_ACCOUNT_STATUS_CREATED

    Then I deposit 60000 PKR into wallet with product code CASH_WALLET_CURRENT for user UID1 and expect a status code of 200

    And I check the balance of the wallet with product code CASH_WALLET_CURRENT for user UID1 and the balance should be 60000 PKR exact

    Given I create a Map MPID1 and expect a status of MAP_CREATED
      | user_profile_identifier | name  | asset_allocation_details                  | allocation_type | goal_date  | goal_amount |
      | UID1                    | House | [{"asset_id": "CASH" ,"percentage": 100}] | FIXED           | 03-06-2024 | 50500       |

    Then I check if the map MPID1 is created for user UID1 and expect a status of MAP_CREATED

    Then I create a schedule for map MPID1 and expect status 200
      | user_profile_identifier | schedule_identifier | frequency | schedule_type       | product_code     | target_weekdays | target_week | amount |
      | UID1                    | SID1                | DAILY     | SCHEDULE_MAP_INVEST | CASH_WALLET_SAVE |                 | 1           | 4.56   |

    Then I check if the schedule SID1 has a status code of 200 and a status of SCHEDULE_STATUS_ACTIVE for user UID1

    Then I trigger schedule SID1 for user UID1 and expect a status code of 200

    And I check the balance of the wallet with product code CASH_WALLET_CURRENT for user UID1 and the balance should be 59995.44 PKR approx

    Then I check the balance of map MPID1 of user UID1 to be 4.56 PKR

    Then I check if the intent with type SCHEDULE_CASH_MAP_INVEST has the status SETTLED and a total of 1 intents exist for the user UID1 in the map_intent_view,MPID1 view

    Then I update the schedule status of SID1 with action PAUSE for user UID1

    Then I check schedule status as SCHEDULE_STATUS_PAUSED for schedule SID1 for user UID1

    Then I trigger schedule SID1 for user UID1 and expect a status code of 200

    And I check the balance of the wallet with product code CASH_WALLET_CURRENT for user UID1 and the balance should be 59995.44 PKR approx

    Then I check the balance of map MPID1 of user UID1 to be 4.56 PKR

    Then I check if the intent with type SCHEDULE_CASH_MAP_INVEST has the status SETTLED and a total of 1 intents exist for the user UID1 in the map_intent_view,MPID1 view

    Then I update the schedule status of SID1 with action RESUME for user UID1

    Then I check schedule status as SCHEDULE_STATUS_ACTIVE for schedule SID1 for user UID1
