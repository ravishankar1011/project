Feature: Precious Metal Scenarios

  Background:

    Given The user UID1 provides a valid mobile number on device_1 to initiate onboarding and the expected status is VERIFICATION_INITIATED
      | user_name | user_name_type | ph_prefix |
      | random    | PHONE_NUMBER   | +378      |

    Then The user UID1 submits OTP to proceed with verification and expects a status code of 200 and a status of VERIFICATION_SUCCESS

    Given I open a new HUGOSAVE user account and expect the status code 200
      | user_profile_identifier | email          | legal_name | name   | account_type |
      | UID1                    | test@gmail.com | John Doe   | Johnny | PERSONAL     |

    Then I check the authorisation status of the device_1 for the user UID1 and expect a device authorisation status of DEVICE_AUTHORISATION_SUCCESS

    And Create a binding signature for the user UID1 to bind the device_1 and the device binding status should be ACTIVE

    And I check the user details to confirm if user UID1 is L3 and the user profile status should be PROFILE_ACTIVE

  Scenario Outline: Gold,Silver,Platinum Vault - Invest, Withdraw

    Given I check if <vault_name> is created for user UID1

    Then I get the user cash wallets for the user UID1 and expect the account status of CASH_ACCOUNT_STATUS_CREATED

    And I deposit 100 SGD into wallet with product code CASH_WALLET_SAVE for user UID1 and expect a status code of 200

    And I check the balance of the wallet with product code CASH_WALLET_SAVE for user UID1 and the balance should be 100 SGD exact

    # invest without rate token
    Given I invest in <asset_name> vault map without rate and expect a status of PENDING
      | user_profile_identifier | transaction_amount | investment_amount | fee_amount | status_code |
      | UID1                    | 10                 | 10                | 0          | 200         |

    Then I check the balance of <asset_name> Map of user UID1 to be 10

    And I check the balance of the wallet with product code CASH_WALLET_SAVE for user UID1 and the balance should be 90 SGD approx

    # invest with rate token
    Given I invest in <asset_name> vault map with rate and expect a status of PENDING
      | user_profile_identifier | transaction_amount | investment_amount | fee_amount | status_code |
      | UID1                    | 20                 | 20                | 0          | 200         |

    Then I check the balance of <asset_name> Map of user UID1 to be 30

    And I check the balance of the wallet with product code CASH_WALLET_SAVE for user UID1 and the balance should be 70 SGD approx

    # withdraw without rate token
    Given I withdraw from the <asset_name> map without rate
      | user_profile_identifier | transaction_amount | withdraw_amount | fee_amount | status_code |
      | UID1                    | 10                 | 10              | 0          | 200         |

    Then I manually settle the sell transaction of user UID1

    Then I check the balance of <asset_name> Map of user UID1 to be 17

    And I check the balance of the wallet with product code CASH_WALLET_SAVE for user UID1 and the balance should be 70 SGD approx

    # withdraw with rate token
    Given I withdraw from the <asset_name> map with rate
      | user_profile_identifier | transaction_amount | withdraw_amount | fee_amount | status_code |
      | UID1                    | 10                 | 10              | 0          | 200         |

    Then I manually settle the sell transaction of user UID1

#    Then I check the balance of <asset_name> Map of user UID1 to be 10

    # invest with invalid rate token
    Given I invest in <asset_name> vault map invalid rate and expect a status of PENDING
      | user_profile_identifier | transaction_amount | investment_amount | fee_amount | status_code |
      | UID1                    | 10                 | 10                | 0          | HSA_9135    |

    Then I check the balance of <asset_name> Map of user UID1 to be 10

    Then I check the balance of the wallet with product code CASH_WALLET_SAVE for user UID1 and the balance should be 70 SGD approx

    # withdraw with invalid rate token
    Given I withdraw from the <asset_name> map invalid rate
      | user_profile_identifier | transaction_amount | withdraw_amount | fee_amount | status_code |
      | UID1                    | 7                  | 7               | 0          | HSA_9135    |

#    Then I check the balance of <asset_name> Map of user UID1 to be 10

#    Then I check the balance of the wallet with product code CASH_WALLET_SAVE for user UID1 and the balance should be 70 SGD approx

    # invest with insufficient spend acc balance
    Given I invest in <asset_name> vault map without rate and expect a status of PENDING
      | user_profile_identifier | transaction_amount | investment_amount | fee_amount | status_code |
      | UID1                    | 110                | 110               | 0          | HSA_9145    |

    Then I check the balance of <asset_name> Map of user UID1 to be 10

    Then I check the balance of the wallet with product code CASH_WALLET_SAVE for user UID1 and the balance should be 70 SGD approx

    # withdraw without sufficient balance in gold vault
    Given I withdraw from the <asset_name> map with rate
      | user_profile_identifier | transaction_amount | withdraw_amount | fee_amount | status_code |
      | UID1                    | 20                 | 20              | 0          | 200         |

#    Then I check the balance of <asset_name> Map of user UID1 to be 10

#    Then I check the balance of the wallet with product code CASH_WALLET_SAVE for user UID1 and the balance should be 70 SGD approx

    # invest with transaction amount less than fee amount
    Given I invest in <asset_name> vault map without rate and expect a status of PENDING
      | user_profile_identifier | transaction_amount | investment_amount | fee_amount | status_code |
      | UID1                    | 0.01               | 0                 | 0.01       | HSA_9136    |
    Examples:
      | asset_name        | vault_name     |
      | PM_GOLD_VAULT     | GOLD_VAULT     |
      | PM_SILVER_VAULT   | SILVER_VAULT   |
      | PM_PLATINUM_VAULT | PLATINUM_VAULT |

  Scenario Outline: Schedule scenario for precious metals

    And I check if <vault_name> is created for user UID1

    Then I get the user cash wallets for the user UID1 and expect the account status of CASH_ACCOUNT_STATUS_CREATED

    Given I deposit 20 SGD into wallet with product code CASH_WALLET_SAVE for user UID1 and expect a status code of 200

    And I check the balance of the wallet with product code CASH_WALLET_SAVE for user UID1 and the balance should be 20 SGD exact

#    invalid schedule data
    Then I create a schedule for map <asset_name> and expect status HSA_9130
      | user_profile_identifier | schedule_identifier | frequency | schedule_type       | product_code     | target_weekdays | target_week | amount |
      | UID1                    | SID2                | DAILY     | SCHEDULE_MAP_INVEST | CASH_WALLET_SAVE |                 | 1           | 0.01   |

    Then I create a schedule for map <asset_name> and expect status HSA_9130
      | user_profile_identifier | schedule_identifier | frequency | schedule_type       | product_code     | target_weekdays | target_week | amount |
      | UID1                    | SID3                | DAILY     | SCHEDULE_MAP_INVEST | CASH_WALLET_SAVE |                 | 1           | 0      |

    Then I create a schedule for map <asset_name> and expect status HSA_9125
      | user_profile_identifier | schedule_identifier | frequency | schedule_type    | product_code     | target_weekdays | target_week | amount |
      | UID1                    | SID4                | DAILY     | someGarbageValue | CASH_WALLET_SAVE |                 | 1           | 0      |

    Then I create a schedule for map <asset_name> and expect status 200
      | user_profile_identifier | schedule_identifier | frequency | schedule_type       | product_code     | target_weekdays | target_week | amount |
      | UID1                    | SID1                | DAILY     | SCHEDULE_MAP_INVEST | CASH_WALLET_SAVE |                 | 1           | 3.26   |

    Then I check if the schedule SID1 has a status code of 200 and a status of SCHEDULE_STATUS_ACTIVE for user UID1

    Then I trigger schedule SID1 for user UID1 and expect a status code of 200

    And I check the balance of the wallet with product code CASH_WALLET_SAVE for user UID1 and the balance should be 16.74 SGD approx

    Then I check the balance of <asset_name> Map of user UID1 to be 3.26

    Then I check if the intent with type SCHEDULE_MAP_INVEST has the status SETTLED and a total of 1 intents exist for the user UID1 in the map_intent_view,<asset_name> view

    Then I update the schedule status of SID1 with action PAUSE for user UID1

    Then I check schedule status as SCHEDULE_STATUS_PAUSED for schedule SID1 for user UID1

    Then I trigger schedule SID1 for user UID1 and expect a status code of 200

    And I check the balance of the wallet with product code CASH_WALLET_SAVE for user UID1 and the balance should be 16.74 SGD approx

    Then I check the balance of <asset_name> Map of user UID1 to be 3.26

    Then I check if the intent with type SCHEDULE_MAP_INVEST has the status SETTLED and a total of 1 intents exist for the user UID1 in the map_intent_view,<asset_name> view

    Then I update the schedule status of SID1 with action RESUME for user UID1

    Then I check schedule status as SCHEDULE_STATUS_ACTIVE for schedule SID1 for user UID1
    Examples:
      | asset_name        | vault_name     |
      | PM_GOLD_VAULT     | GOLD_VAULT     |
      | PM_SILVER_VAULT   | SILVER_VAULT   |
      | PM_PLATINUM_VAULT | PLATINUM_VAULT |
