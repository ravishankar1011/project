Feature: Admin

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

  Scenario: Block Internal Debits and Internal Credits

    Then I get the user cash wallets for the user UID1 and expect the account status of CASH_ACCOUNT_STATUS_CREATED

    Then I deposit 150 SGD into wallet with product code CASH_WALLET_SAVE for user UID1 and expect a status code of 200

    And I check the balance of the wallet with product code CASH_WALLET_SAVE for user UID1 and the balance should be 150 SGD exact

    Then I deposit 50 SGD into wallet with product code CASH_WALLET_SPEND for user UID1 and expect a status code of 200

    And I check the balance of the wallet with product code CASH_WALLET_SAVE for user UID1 and the balance should be 100 SGD exact

    Given I fetch list of questionnaire

    Given I check if questionnaire exists with name SUITABILITY_ASSESSMENT else create new questionnaire

    Then I fetch questionnaire SUITABILITY_ASSESSMENT and check status as QUESTIONNAIRE_ACTIVE

    Given I create questionnaire UQID1 for user UID1 - questionnaire SUITABILITY_ASSESSMENT

    Then I request to get user questionnaire UQID1 - SUITABILITY_ASSESSMENT for user UID1

    Then I request to update and verify user questionnaire answer UQID1 for user UID1 - questionnaire SUITABILITY_ASSESSMENT and expect a status code of 200

    Then I request to submit user questionnaire UQID1 for user UID1 and expect a status code of 200

    Then I BLOCK the INTERNAL_DEBITS of CASH_WALLET_SAVE for a user UID1 and expect a status code of 200

    Then I check the status of INTERNAl_DEBITS of CASH_WALLET_SAVE for user UID1 to be TRANSACTION_STATUS_ADMIN_BLOCKED

    Then I deposit 50 SGD into wallet with product code CASH_WALLET_SPEND for user UID1 and expect a status code of 200

    And I check the balance of the wallet with product code CASH_WALLET_SAVE for user UID1 and the balance should be 100 SGD exact

    And I check if BALANCED_VAULT is created for user UID1

    Given I invest in ETF_BALANCED_VAULT vault map without rate and expect a status of PENDING
      | user_profile_identifier | transaction_amount | investment_amount | fee_amount | status_code |
      | UID1                    | 10                 | 10                | 0          | 200         |

    And I check the balance of the wallet with product code CASH_WALLET_SAVE for user UID1 and the balance should be 100 SGD exact

    And I check if GOLD_VAULT is created for user UID1

    Given I invest in PM_GOLD_VAULT vault map with rate and expect a status of PENDING
      | user_profile_identifier | transaction_amount | investment_amount | fee_amount | status_code |
      | UID1                    | 20                 | 20                | 0          | 200         |

    And I check the balance of the wallet with product code CASH_WALLET_SAVE for user UID1 and the balance should be 100 SGD exact

    Then I order a physical card for UID1 with card name as random_valid_choice and expect a status code of 200 and expect a card status of CARD_STATUS_PENDING

    Then I wait for card status as CARD_STATUS_INACTIVE to activate PHYSICAL card for user UID1, activate with valid token, with status 200

    Then I check card status is CARD_STATUS_ACTIVE for user UID1 for PHYSICAL card

    And I ENABLE roundups for user UID1

    #checking roundup transaction
    Given I create below transaction for PHYSICAL card for user profile id and expect a status code of 200
      | user_profile_identifier | transaction_permutation_name | billing_amount | is_foreign_txn |
      | UID1                    | AUTH_CLEAR                   | 5.5            | false          |

    And I check the balance of the wallet with product code CASH_WALLET_SPEND for user UID1 and the balance should be 44.5 SGD exact

    Then I UNBLOCK the INTERNAL_DEBITS of CASH_WALLET_SAVE for a user UID1 and expect a status code of 200

    Then I check the status of INTERNAl_DEBITS of CASH_WALLET_SAVE for user UID1 to be TRANSACTION_STATUS_ACTIVE

    Then I deposit 50 SGD into wallet with product code CASH_WALLET_SPEND for user UID1 and expect a status code of 200

    And I check the balance of the wallet with product code CASH_WALLET_SPEND for user UID1 and the balance should be 94.5 SGD exact

    Then I BLOCK the INTERNAL_CREDITS of CASH_WALLET_SPEND for a user UID1 and expect a status code of 200

    Then I check the status of INTERNAl_CREDITS of CASH_WALLET_SPEND for user UID1 to be TRANSACTION_STATUS_ADMIN_BLOCKED

    Then I deposit 50 SGD into wallet with product code CASH_WALLET_SPEND for user UID1 and expect a status code of 200

    And I check the balance of the wallet with product code CASH_WALLET_SPEND for user UID1 and the balance should be 94.5 SGD exact

  Scenario: Block External Debits and External Credits

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

    Then I BLOCK the EXTERNAL_DEBITS of CASH_WALLET_SPEND for a user UID1 and expect a status code of 200

    Then I check the status of EXTERNAL_DEBITS of CASH_WALLET_SPEND for user UID1 to be TRANSACTION_STATUS_ADMIN_BLOCKED

    And I check the balance of the wallet with product code CASH_WALLET_SAVE for user UID2 and the balance should be 0 SGD exact

    Then I deposit 150 SGD into wallet with product code CASH_WALLET_SAVE for user UID1 and expect a status code of 200

    And I check the balance of the wallet with product code CASH_WALLET_SAVE for user UID1 and the balance should be 150 SGD exact

    Then I deposit 150 SGD into wallet with product code CASH_WALLET_SPEND for user UID1 and expect a status code of 200

    And I check the balance of the wallet with product code CASH_WALLET_SPEND for user UID1 and the balance should be 150 SGD exact

    Then I initiate the initial user authorisation to PAY_PAYEE for user UID1 and expect a status of USER_AUTHORISATION_SUCCESS

    Then I initiate the final user authorisation to PAY_PAYEE and expect a user authorisation status as USER_AUTHORISATION_INITIATED for user UID1

    And I initiate the OTP journey within the OTP_STEP for user UID1 to authorise the user and expect a status JOURNEY_INITIATED

    Then I process the OTP journey within the OTP_STEP for user UID1 to authorise the user and expect a status JOURNEY_PROCESSED

    And I submit the OTP journey within the OTP_STEP for user UID1 to authorise the user and expect a status JOURNEY_SUCCESSFUL

    Then I submit the final user authorisation for PAY_PAYEE of user UID1 and expect a status USER_AUTHORISATION_SUBMITTED

    And I get the final user authorisation token for PAY_PAYEE of user UID1 and expect a status USER_AUTHORISATION_SUCCESS

    Then I transfer 150 SGD from user UID1 to user UID2 with no reference and valid payee id and expect a status code of 200

    And I check the balance of the wallet with product code CASH_WALLET_SPEND for user UID1 and the balance should be 150 SGD exact

    And I check the balance of the wallet with product code CASH_WALLET_SAVE for user UID2 and the balance should be 0 SGD exact

    Then I UNBLOCK the EXTERNAL_DEBITS of CASH_WALLET_SPEND for a user UID1 and expect a status code of 200

    Then I check the status of EXTERNAL_DEBITS of CASH_WALLET_SPEND for user UID1 to be TRANSACTION_STATUS_ACTIVE

    Then I BLOCK the EXTERNAL_CREDITS of CASH_WALLET_SAVE for a user UID2 and expect a status code of 200

    Then I check the status of EXTERNAL_CREDITS of CASH_WALLET_SAVE for user UID2 to be TRANSACTION_STATUS_ADMIN_BLOCKED

    Then I initiate the initial user authorisation to PAY_PAYEE for user UID1 and expect a status of USER_AUTHORISATION_SUCCESS

    Then I initiate the final user authorisation to PAY_PAYEE and expect a user authorisation status as USER_AUTHORISATION_INITIATED for user UID1

    And I initiate the OTP journey within the OTP_STEP for user UID1 to authorise the user and expect a status JOURNEY_INITIATED

    Then I process the OTP journey within the OTP_STEP for user UID1 to authorise the user and expect a status JOURNEY_PROCESSED

    And I submit the OTP journey within the OTP_STEP for user UID1 to authorise the user and expect a status JOURNEY_SUCCESSFUL

    Then I submit the final user authorisation for PAY_PAYEE of user UID1 and expect a status USER_AUTHORISATION_SUBMITTED

    And I get the final user authorisation token for PAY_PAYEE of user UID1 and expect a status USER_AUTHORISATION_SUCCESS

    Then I transfer 150 SGD from user UID1 to user UID2 with no reference and valid payee id and expect a status code of 200

    And I check the balance of the wallet with product code CASH_WALLET_SPEND for user UID1 and the balance should be 150 SGD exact

    And I check the balance of the wallet with product code CASH_WALLET_SAVE for user UID2 and the balance should be 0 SGD exact

  Scenario: Block account status for a User

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

    Then I BLOCK the CASH_WALLET_SAVE account for user UID2

    Then I check the status of CASH_WALLET_SAVE for user UID2 to be CASH_WALLET_STATUS_BLOCKED

    And I check the balance of the wallet with product code CASH_WALLET_SAVE for user UID2 and the balance should be 0 SGD exact

    Then I deposit 150 SGD into wallet with product code CASH_WALLET_SAVE for user UID1 and expect a status code of 200

    And I check the balance of the wallet with product code CASH_WALLET_SAVE for user UID1 and the balance should be 150 SGD exact

    Then I deposit 150 SGD into wallet with product code CASH_WALLET_SPEND for user UID1 and expect a status code of 200

    And I check the balance of the wallet with product code CASH_WALLET_SPEND for user UID1 and the balance should be 150 SGD exact

    Then I initiate the initial user authorisation to PAY_PAYEE for user UID1 and expect a status of USER_AUTHORISATION_SUCCESS

    Then I initiate the final user authorisation to PAY_PAYEE and expect a user authorisation status as USER_AUTHORISATION_INITIATED for user UID1

    And I initiate the OTP journey within the OTP_STEP for user UID1 to authorise the user and expect a status JOURNEY_INITIATED

    Then I process the OTP journey within the OTP_STEP for user UID1 to authorise the user and expect a status JOURNEY_PROCESSED

    And I submit the OTP journey within the OTP_STEP for user UID1 to authorise the user and expect a status JOURNEY_SUCCESSFUL

    Then I submit the final user authorisation for PAY_PAYEE of user UID1 and expect a status USER_AUTHORISATION_SUBMITTED

    And I get the final user authorisation token for PAY_PAYEE of user UID1 and expect a status USER_AUTHORISATION_SUCCESS

    And I wait for 10 seconds

    Then I transfer 150 SGD from user UID1 to user UID2 with no reference and valid payee id and expect a status code of 200

    And I check the balance of the wallet with product code CASH_WALLET_SPEND for user UID1 and the balance should be 150 SGD exact

    And I check the balance of the wallet with product code CASH_WALLET_SAVE for user UID2 and the balance should be 0 SGD exact

