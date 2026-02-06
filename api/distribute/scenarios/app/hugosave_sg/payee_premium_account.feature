Feature: Payee

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

  Scenario: Add, Pay, Delete Payee, Add Note

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

    And I check if user UID2 is in favourites of UID1

    And I check the balance of the wallet with product code CASH_WALLET_SAVE for user UID1 and the balance should be 0 SGD exact

    Then I get the user cash wallets for the user UID1 and expect the account status of CASH_ACCOUNT_STATUS_CREATED

    Then I deposit 50 SGD into wallet with product code CASH_WALLET_SAVE for user UID1 and expect a status code of 200

    And I check the balance of the wallet with product code CASH_WALLET_SAVE for user UID1 and the balance should be 50 SGD exact

    Then I deposit 50 SGD into wallet with product code CASH_WALLET_SPEND for user UID1 and expect a status code of 200

    And I check the balance of the wallet with product code CASH_WALLET_SPEND for user UID1 and the balance should be 50 SGD exact

    Then I initiate the initial user authorisation to PAY_PAYEE for user UID1 and expect a status of USER_AUTHORISATION_SUCCESS

    Then I initiate the final user authorisation to PAY_PAYEE and expect a user authorisation status as USER_AUTHORISATION_INITIATED for user UID1

    And I initiate the OTP journey within the OTP_STEP for user UID1 to authorise the user and expect a status JOURNEY_INITIATED

    Then I process the OTP journey within the OTP_STEP for user UID1 to authorise the user and expect a status JOURNEY_PROCESSED

    And I submit the OTP journey within the OTP_STEP for user UID1 to authorise the user and expect a status JOURNEY_SUCCESSFUL

    Then I submit the final user authorisation for PAY_PAYEE of user UID1 and expect a status USER_AUTHORISATION_SUBMITTED

    And I get the final user authorisation token for PAY_PAYEE of user UID1 and expect a status USER_AUTHORISATION_SUCCESS

    Then I transfer 20 SGD from user UID1 to user UID2 with no reference and valid payee id and expect a status code of 200

    And I check the balance of the wallet with product code CASH_WALLET_SPEND for user UID1 and the balance should be 30 SGD exact

    And I check the balance of the wallet with product code CASH_WALLET_SAVE for user UID2 and the balance should be 20 SGD exact

    Then I add a random note to the latest intent of user UID1 and check if note is saved

    Then I transfer 20 SGD from user UID1 to user UID2 with no reference and invalid payee id and expect a status code of HSA_9104

    Then I transfer 100 SGD from user UID1 to user UID2 with no reference and valid payee id and expect a status code of 200

    And I check the balance of the wallet with product code CASH_WALLET_SPEND for user UID1 and the balance should be 30 SGD exact

    And I check the balance of the wallet with product code CASH_WALLET_SAVE for user UID2 and the balance should be 20 SGD exact

    Given I delete the payee UID2 added to user UID1

    Then I wait for 10 seconds

    And I check if the wallet with product code CASH_WALLET_SAVE of user UID2 is not_added as payee to user UID1 and expect a status of BENEFICIARY_STATUS_CREATED

  Scenario: Deposits - Limit checks and updating it

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

    And I check the balance of the wallet with product code CASH_WALLET_SAVE for user UID1 and the balance should be 0 SGD exact

    Then I get the user cash wallets for the user UID1 and expect the account status of CASH_ACCOUNT_STATUS_CREATED

    Then I deposit 1500 SGD into wallet with product code CASH_WALLET_SAVE for user UID1 and expect a status code of 200

    And I check the balance of the wallet with product code CASH_WALLET_SAVE for user UID1 and the balance should be 1500 SGD exact

    Then I deposit 1500 SGD into wallet with product code CASH_WALLET_SPEND for user UID1 and expect a status code of 200

    And I check the balance of the wallet with product code CASH_WALLET_SPEND for user UID1 and the balance should be 1500 SGD exact

    Then I initiate the initial user authorisation to PAY_PAYEE for user UID1 and expect a status of USER_AUTHORISATION_SUCCESS

    Then I initiate the final user authorisation to PAY_PAYEE and expect a user authorisation status as USER_AUTHORISATION_INITIATED for user UID1

    And I initiate the OTP journey within the OTP_STEP for user UID1 to authorise the user and expect a status JOURNEY_INITIATED

    Then I process the OTP journey within the OTP_STEP for user UID1 to authorise the user and expect a status JOURNEY_PROCESSED

    And I submit the OTP journey within the OTP_STEP for user UID1 to authorise the user and expect a status JOURNEY_SUCCESSFUL

    Then I submit the final user authorisation for PAY_PAYEE of user UID1 and expect a status USER_AUTHORISATION_SUBMITTED

    And I get the final user authorisation token for PAY_PAYEE of user UID1 and expect a status USER_AUTHORISATION_SUCCESS

    Then I transfer 1500 SGD from user UID1 to user UID2 with no reference and valid payee id and expect a status code of 200

    And I check the balance of the wallet with product code CASH_WALLET_SPEND for user UID1 and the balance should be 1500 SGD exact

    And I check the balance of the wallet with product code CASH_WALLET_SAVE for user UID2 and the balance should be 0 SGD exact

    Then I initiate the initial user authorisation to UPDATE_USER_TRANSACTION_LIMITS for user UID1 and expect a status of USER_AUTHORISATION_SUCCESS

    Then I initiate the final user authorisation to UPDATE_USER_TRANSACTION_LIMITS and expect a user authorisation status as USER_AUTHORISATION_INITIATED for user UID1

    And I wait for 5 seconds

    And I initiate the PASSCODE journey within the PASSCODE_STEP for user UID1 to authorise the user and expect a status JOURNEY_INITIATED

    Then I process the PASSCODE journey within the PASSCODE_STEP for user UID1 to authorise the user and expect a status JOURNEY_PROCESSED

    And I submit the PASSCODE journey within the PASSCODE_STEP for user UID1 to authorise the user and expect a status JOURNEY_SUCCESSFUL

    Then I submit the final user authorisation for UPDATE_USER_TRANSACTION_LIMITS of user UID1 and expect a status USER_AUTHORISATION_SUBMITTED

    And I get the final user authorisation token for UPDATE_USER_TRANSACTION_LIMITS of user UID1 and expect a status USER_AUTHORISATION_SUCCESS

    Then I edit the Per Transaction limits for user UID1 to 2000 SGD and expect a status code of 200

    And   I check if the hard limits are updated to 2000 for user UID1

    Then I initiate the initial user authorisation to PAY_PAYEE for user UID1 and expect a status of USER_AUTHORISATION_SUCCESS

    Then I initiate the final user authorisation to PAY_PAYEE and expect a user authorisation status as USER_AUTHORISATION_INITIATED for user UID1

    And I wait for 5 seconds

    And I initiate the OTP journey within the OTP_STEP for user UID1 to authorise the user and expect a status JOURNEY_INITIATED

    Then I process the OTP journey within the OTP_STEP for user UID1 to authorise the user and expect a status JOURNEY_PROCESSED

    And I submit the OTP journey within the OTP_STEP for user UID1 to authorise the user and expect a status JOURNEY_SUCCESSFUL

    Then I submit the final user authorisation for PAY_PAYEE of user UID1 and expect a status USER_AUTHORISATION_SUBMITTED

    And I get the final user authorisation token for PAY_PAYEE of user UID1 and expect a status USER_AUTHORISATION_SUCCESS

    And I wait for 10 seconds

    Then I transfer 1500 SGD from user UID1 to user UID2 with no reference and valid payee id and expect a status code of 200

    And I check the balance of the wallet with product code CASH_WALLET_SAVE for user UID2 and the balance should be 1500 SGD exact

    And I check the balance of the wallet with product code CASH_WALLET_SPEND for user UID1 and the balance should be 0 SGD exact
