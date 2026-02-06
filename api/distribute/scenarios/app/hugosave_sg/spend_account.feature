Feature: Spend Account Hugosave Scenario

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

  Scenario: Spend Account Auto-Topup without card transactions

    Given The user UID2 provides a valid mobile number on device_1 to initiate onboarding and the expected status is VERIFICATION_INITIATED
      | user_name | user_name_type | ph_prefix |
      | random    | PHONE_NUMBER   | +378      |

    Then The user UID2 submits OTP to proceed with verification and expects a status code of 200 and a status of VERIFICATION_SUCCESS

    Given I open a new HUGOSAVE user account and expect the status code 200
      | user_profile_identifier | email          | legal_name | name   | account_type |
      | UID2                    | test@gmail.com | John Doe   | Johnny | PERSONAL     |

    Then I check the authorisation status of the device_1 for the user UID2 and expect a device authorisation status of DEVICE_AUTHORISATION_SUCCESS

    And Create a binding signature for the user UID2 to bind the device_1 and the device binding status should be ACTIVE

    And I check the user details to confirm if user UID2 is L3 and the user profile status should be PROFILE_ACTIVE

    Then I initiate the initial user authorisation to ADD_PAYEE for user UID1 and expect a status of USER_AUTHORISATION_SUCCESS

    Then I initiate the final user authorisation to ADD_PAYEE and expect a user authorisation status as USER_AUTHORISATION_INITIATED for user UID1

    And I initiate the OTP journey within the OTP_STEP for user UID1 to authorise the user and expect a status JOURNEY_INITIATED

    Then I process the OTP journey within the OTP_STEP for user UID1 to authorise the user and expect a status JOURNEY_PROCESSED

    And I submit the OTP journey within the OTP_STEP for user UID1 to authorise the user and expect a status JOURNEY_SUCCESSFUL

    Then I submit the final user authorisation for ADD_PAYEE of user UID1 and expect a status USER_AUTHORISATION_SUBMITTED

    And I get the final user authorisation token for ADD_PAYEE of user UID1 and expect a status USER_AUTHORISATION_SUCCESS

    Then I get the user cash wallets for the user UID2 and expect the account status of CASH_ACCOUNT_STATUS_CREATED

    Then I add the wallet with product code CASH_WALLET_SAVE of user UID2 to user UID1 as payee PID1 with valid_swift_bic and expect a status code of 200 and a status of BENEFICIARY_STATUS_PENDING

    And I check if the wallet with product code CASH_WALLET_SAVE of user UID2 is added as payee to user UID1 and expect a status of BENEFICIARY_STATUS_CREATED

    Then I get the user cash wallets for the user UID1 and expect the account status of CASH_ACCOUNT_STATUS_CREATED

    Then I deposit 150 SGD into wallet with product code CASH_WALLET_SAVE for user UID1 and expect a status code of 200

    And I check the balance of wallet with product code CASH_WALLET_SAVE of user UID1 is 150

    Then I deposit 50 SGD into wallet with product code CASH_WALLET_SPEND for user UID1 and expect a status code of 200

    And I check the balance of wallet with product code CASH_WALLET_SPEND of user UID1 is 50

    Then I verify below intent record in present in intents list
      | user_profile_identifier | product_code     | intent_type      | intent_status | count | view |
      | UID1                    | CASH_WALLET_SAVE | EXTERNAL_DEPOSIT | SETTLED       | 1     | cash |

    Given I setup auto topup for below cash wallet
      | user_profile_identifier | cash_wallet_id    | auto_topup_enabled | trigger_amount | topup_amount | is_external | funding_cash_wallet_id |
      | UID1                    | CASH_WALLET_SPEND | true               | 25             | 50           | false       | CASH_WALLET_SAVE       |

    Then I verify auto topup enabled for CASH_WALLET_SPEND of user UID1

    Then I initiate the initial user authorisation to PAY_PAYEE for user UID1 and expect a status of USER_AUTHORISATION_SUCCESS

    Then I initiate the final user authorisation to PAY_PAYEE and expect a user authorisation status as USER_AUTHORISATION_INITIATED for user UID1

    And I initiate the OTP journey within the OTP_STEP for user UID1 to authorise the user and expect a status JOURNEY_INITIATED

    Then I process the OTP journey within the OTP_STEP for user UID1 to authorise the user and expect a status JOURNEY_PROCESSED

    And I submit the OTP journey within the OTP_STEP for user UID1 to authorise the user and expect a status JOURNEY_SUCCESSFUL

    Then I submit the final user authorisation for PAY_PAYEE of user UID1 and expect a status USER_AUTHORISATION_SUBMITTED

    And I get the final user authorisation token for PAY_PAYEE of user UID1 and expect a status USER_AUTHORISATION_SUCCESS

    Then I transfer 30 SGD from user UID1 to user UID2 with no reference and valid payee id and expect a status code of 200

    And I check the balance of wallet with product code CASH_WALLET_SAVE of user UID2 is 30

    Then I verify below intent record in present in intents list
      | user_profile_identifier | product_code      | intent_type      | intent_status | count | view |
      | UID1                    | CASH_WALLET_SPEND | PAY_PAYEE        | SETTLED       | 1     | cash |
      | UID2                    | CASH_WALLET_SAVE  | EXTERNAL_DEPOSIT | SETTLED       | 1     | cash |

    And I check the balance of wallet with product code CASH_WALLET_SPEND of user UID1 is 70

    Then I verify below intent record in present in intents list
      | user_profile_identifier | product_code      | intent_type | intent_status | count | view |
      | UID1                    | CASH_WALLET_SPEND | AUTO_TOP_UP | SETTLED       | 1     | cash |

    Then I transfer 45 SGD from user UID1 to user UID2 with no reference and valid payee id and expect a status code of 200

    Then I check the balance of wallet with product code CASH_WALLET_SPEND of user UID1 is 25

    Then I verify below intent record in present in intents list
      | user_profile_identifier | product_code      | intent_type      | intent_status | count | view |
      | UID1                    | CASH_WALLET_SPEND | PAY_PAYEE        | SETTLED       | 2     | cash |
      | UID2                    | CASH_WALLET_SAVE  | EXTERNAL_DEPOSIT | SETTLED       | 2     | cash |

    Then I verify below intent record in present in intents list
      | user_profile_identifier | product_code      | intent_type | intent_status | count | view |
      | UID1                    | CASH_WALLET_SPEND | AUTO_TOP_UP | SETTLED       | 1     | cash |

    #withdraw to save account and spend account balance is below trigger amount
    And I withdraw 5 SGD from card account of user UID1

    Then I check the balance of wallet with product code CASH_WALLET_SPEND of user UID1 is 20


  Scenario: Stock and flow limits verification.

    Then I get the user cash wallets for the user UID1 and expect the account status of CASH_ACCOUNT_STATUS_CREATED

    Given I deposit 35000 SGD into wallet with product code CASH_WALLET_SAVE for user UID1 and expect a status code of 200

    And I check the balance of wallet with product code CASH_WALLET_SAVE of user UID1 is 35000

    Given I deposit 5050 SGD into wallet with product code CASH_WALLET_SPEND for user UID1 and expect a status code of 200

    And I check the balance of wallet with product code CASH_WALLET_SAVE of user UID1 is 35000

    And I check the balance of wallet with product code CASH_WALLET_SPEND of user UID1 is 0

    Given The user UID2 provides a valid mobile number on device_1 to initiate onboarding and the expected status is VERIFICATION_INITIATED
      | user_name | user_name_type | ph_prefix |
      | random    | PHONE_NUMBER   | +378      |

    Then The user UID2 submits OTP to proceed with verification and expects a status code of 200 and a status of VERIFICATION_SUCCESS

    Given I open a new HUGOSAVE user account and expect the status code 200
      | user_profile_identifier | email          | legal_name | name   | account_type |
      | UID2                    | test@gmail.com | John Doe   | Johnny | PERSONAL     |

    Then I check the authorisation status of the device_1 for the user UID2 and expect a device authorisation status of DEVICE_AUTHORISATION_SUCCESS

    And Create a binding signature for the user UID2 to bind the device_1 and the device binding status should be ACTIVE

    And I check the user details to confirm if user UID2 is L3 and the user profile status should be PROFILE_ACTIVE

    Then I initiate the initial user authorisation to ADD_PAYEE for user UID1 and expect a status of USER_AUTHORISATION_SUCCESS

    Then I initiate the final user authorisation to ADD_PAYEE and expect a user authorisation status as USER_AUTHORISATION_INITIATED for user UID1

    And I initiate the OTP journey within the OTP_STEP for user UID1 to authorise the user and expect a status JOURNEY_INITIATED

    Then I process the OTP journey within the OTP_STEP for user UID1 to authorise the user and expect a status JOURNEY_PROCESSED

    And I submit the OTP journey within the OTP_STEP for user UID1 to authorise the user and expect a status JOURNEY_SUCCESSFUL

    Then I submit the final user authorisation for ADD_PAYEE of user UID1 and expect a status USER_AUTHORISATION_SUBMITTED

    And I get the final user authorisation token for ADD_PAYEE of user UID1 and expect a status USER_AUTHORISATION_SUCCESS

    Then I get the user cash wallets for the user UID2 and expect the account status of CASH_ACCOUNT_STATUS_CREATED

    Then I add the wallet with product code CASH_WALLET_SAVE of user UID2 to user UID1 as payee PID1 with valid_swift_bic and expect a status code of 200 and a status of BENEFICIARY_STATUS_PENDING

    And I check if the wallet with product code CASH_WALLET_SAVE of user UID2 is added as payee to user UID1 and expect a status of BENEFICIARY_STATUS_CREATED

    Given I deposit 5000 SGD into wallet with product code CASH_WALLET_SPEND for user UID1 and expect a status code of 200

    And I check the balance of wallet with product code CASH_WALLET_SPEND of user UID1 is 5000

    Then I transfer 5000 SGD from user UID1 to user UID2 with no reference and valid payee id and expect a status code of 200

    And I check the balance of wallet with product code CASH_WALLET_SAVE of user UID2 is 5000

    And I check the balance of wallet with product code CASH_WALLET_SPEND of user UID1 is 0

    Given I deposit 5000 SGD into wallet with product code CASH_WALLET_SPEND for user UID1 and expect a status code of 200

    And I check the balance of wallet with product code CASH_WALLET_SPEND of user UID1 is 5000

    Then I transfer 5000 SGD from user UID1 to user UID2 with no reference and valid payee id and expect a status code of 200

    And I check the balance of wallet with product code CASH_WALLET_SAVE of user UID2 is 10000

    And I check the balance of wallet with product code CASH_WALLET_SPEND of user UID1 is 0

    Given I deposit 5000 SGD into wallet with product code CASH_WALLET_SPEND for user UID1 and expect a status code of 200

    And I check the balance of wallet with product code CASH_WALLET_SPEND of user UID1 is 5000

    Then I transfer 5000 SGD from user UID1 to user UID2 with no reference and valid payee id and expect a status code of 200

    And I check the balance of wallet with product code CASH_WALLET_SAVE of user UID2 is 15000

    And I check the balance of wallet with product code CASH_WALLET_SPEND of user UID1 is 0

    Given I deposit 5000 SGD into wallet with product code CASH_WALLET_SPEND for user UID1 and expect a status code of 200

    And I check the balance of wallet with product code CASH_WALLET_SPEND of user UID1 is 5000

    Then I transfer 5000 SGD from user UID1 to user UID2 with no reference and valid payee id and expect a status code of 200

    And I check the balance of wallet with product code CASH_WALLET_SAVE of user UID2 is 20000

    And I check the balance of wallet with product code CASH_WALLET_SPEND of user UID1 is 0

    Given I deposit 5000 SGD into wallet with product code CASH_WALLET_SPEND for user UID1 and expect a status code of 200

    And I check the balance of wallet with product code CASH_WALLET_SPEND of user UID1 is 5000

    Then I transfer 5000 SGD from user UID1 to user UID2 with no reference and valid payee id and expect a status code of 200

    And I check the balance of wallet with product code CASH_WALLET_SAVE of user UID2 is 25000

    And I check the balance of wallet with product code CASH_WALLET_SPEND of user UID1 is 0

    Given I deposit 5000 SGD into wallet with product code CASH_WALLET_SPEND for user UID1 and expect a status code of 200

    And I check the balance of wallet with product code CASH_WALLET_SPEND of user UID1 is 5000

    Then I transfer 5000 SGD from user UID1 to user UID2 with no reference and valid payee id and expect a status code of 200

    And I check the balance of wallet with product code CASH_WALLET_SAVE of user UID2 is 30000

    And I check the balance of wallet with product code CASH_WALLET_SPEND of user UID1 is 0

    Given I deposit 5000 SGD into wallet with product code CASH_WALLET_SPEND for user UID1 and expect a status code of 200

    And I check the balance of wallet with product code CASH_WALLET_SPEND of user UID1 is 5000

    Then I transfer 5000 SGD from user UID1 to user UID2 with no reference and valid payee id and expect a status code of 200

    And I check the balance of wallet with product code CASH_WALLET_SAVE of user UID2 is 30000

    And I check the balance of wallet with product code CASH_WALLET_SPEND of user UID1 is 5000

