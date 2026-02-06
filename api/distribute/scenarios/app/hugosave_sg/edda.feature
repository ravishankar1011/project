Feature: EDDA

  Background: Create a new User Account

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

    Then I get the user cash wallets for the user UID1 and expect the account status of CASH_ACCOUNT_STATUS_CREATED

  Scenario: EDDA - Create Mandate, Authorise Mandate, Check for Auto Trigger

    Then I deposit 250 SGD into wallet with product code CASH_WALLET_SAVE for user UID1 and expect a status code of 200

    And I check the balance of the wallet with product code CASH_WALLET_SAVE for user UID1 and the balance should be 250 SGD exact

    Then I initiate the initial user authorisation to CREATE_DIRECT_DEBIT for user UID1 and expect a status of USER_AUTHORISATION_SUCCESS

    Then I initiate the final user authorisation to CREATE_DIRECT_DEBIT and expect a user authorisation status as USER_AUTHORISATION_SUCCESS for user UID1

    Given I create a mandate MID1 for the user UID1 and expect a status code of 200 and a status of MANDATE_CREATION_PENDING

    Then I accept the Mandate MID1 for user UID1

    Then I initiate the initial user authorisation to VIEW_DIRECT_DEBIT for user UID1 and expect a status of USER_AUTHORISATION_SUCCESS

    Then I initiate the final user authorisation to CREATE_DIRECT_DEBIT and expect a user authorisation status as USER_AUTHORISATION_SUCCESS for user UID1

    Then I verify mandate MID1 for user UID1 is created with status code of 200

    Then I enable auto-top-up of 200 SGD for user UID1 with trigger amount 15 SGD to CASH_WALLET_SAVE account with Mandate-MID1

    Then I deposit 240 SGD into wallet with product code CASH_WALLET_SPEND for user UID1 and expect a status code of 200

    And I check the balance of the wallet with product code CASH_WALLET_SPEND for user UID1 and the balance should be 240 SGD exact

    Then I wait for 5 seconds

    And I check the balance of the wallet with product code CASH_WALLET_SAVE for user UID1 and the balance should be 210 SGD exact

  Scenario: EDDA - Create more than 2 Mandates and check for Failure (Mandate creation limit reached)

    Then I initiate the initial user authorisation to CREATE_DIRECT_DEBIT for user UID1 and expect a status of USER_AUTHORISATION_SUCCESS

    Then I initiate the final user authorisation to CREATE_DIRECT_DEBIT and expect a user authorisation status as USER_AUTHORISATION_SUCCESS for user UID1

    Given I create a mandate MID1 for the user UID1 and expect a status code of 200 and a status of MANDATE_CREATION_PENDING

    Then I accept the Mandate MID1 for user UID1

    Then I initiate the initial user authorisation to VIEW_DIRECT_DEBIT for user UID1 and expect a status of USER_AUTHORISATION_SUCCESS

    Then I initiate the final user authorisation to CREATE_DIRECT_DEBIT and expect a user authorisation status as USER_AUTHORISATION_SUCCESS for user UID1

    Then I verify mandate MID1 for user UID1 is created with status code of 200

    Then I initiate the initial user authorisation to CREATE_DIRECT_DEBIT for user UID1 and expect a status of USER_AUTHORISATION_SUCCESS

    Then I initiate the final user authorisation to CREATE_DIRECT_DEBIT and expect a user authorisation status as USER_AUTHORISATION_SUCCESS for user UID1

    Given I create a mandate MID1 for the user UID1 and expect a status code of 200 and a status of MANDATE_CREATION_PENDING

    Then I accept the Mandate MID1 for user UID1

    Then I initiate the initial user authorisation to VIEW_DIRECT_DEBIT for user UID1 and expect a status of USER_AUTHORISATION_SUCCESS

    Then I initiate the final user authorisation to CREATE_DIRECT_DEBIT and expect a user authorisation status as USER_AUTHORISATION_SUCCESS for user UID1

    Then I verify mandate MID1 for user UID1 is created with status code of 200

    Then I initiate the initial user authorisation to CREATE_DIRECT_DEBIT for user UID1 and expect a status of USER_AUTHORISATION_SUCCESS

    Then I initiate the final user authorisation to CREATE_DIRECT_DEBIT and expect a user authorisation status as USER_AUTHORISATION_SUCCESS for user UID1

    Then I create a mandate MID1 for the user UID1 and expect a status code of HSA_9046 and a status of MANDATE_CREATION_FAILED

  Scenario: EDDA - Create Mandate, check for 3 triggers on a single day

    Then I deposit 250 SGD into wallet with product code CASH_WALLET_SAVE for user UID1 and expect a status code of 200

    And I check the balance of the wallet with product code CASH_WALLET_SAVE for user UID1 and the balance should be 250 SGD exact

    Then I initiate the initial user authorisation to CREATE_DIRECT_DEBIT for user UID1 and expect a status of USER_AUTHORISATION_SUCCESS

    Then I initiate the final user authorisation to CREATE_DIRECT_DEBIT and expect a user authorisation status as USER_AUTHORISATION_SUCCESS for user UID1

    Given I create a mandate MID1 for the user UID1 and expect a status code of 200 and a status of MANDATE_CREATION_PENDING

    Then I accept the Mandate MID1 for user UID1

    Then I initiate the initial user authorisation to VIEW_DIRECT_DEBIT for user UID1 and expect a status of USER_AUTHORISATION_SUCCESS

    Then I initiate the final user authorisation to CREATE_DIRECT_DEBIT and expect a user authorisation status as USER_AUTHORISATION_SUCCESS for user UID1

    Then I verify mandate MID1 for user UID1 is created with status code of 200

    Then I enable auto-top-up of 200 SGD for user UID1 with trigger amount 15 SGD to CASH_WALLET_SAVE account with Mandate-MID1

    #1st time
    Then I deposit 240 SGD into wallet with product code CASH_WALLET_SPEND for user UID1 and expect a status code of 200

    And I check the balance of the wallet with product code CASH_WALLET_SPEND for user UID1 and the balance should be 240 SGD exact

    And I check the balance of the wallet with product code CASH_WALLET_SAVE for user UID1 and the balance should be 10 SGD exact

    And I check the balance of the wallet with product code CASH_WALLET_SAVE for user UID1 and the balance should be 210 SGD exact

    #2nd time
    Then I deposit 200 SGD into wallet with product code CASH_WALLET_SPEND for user UID1 and expect a status code of 200

    And I check the balance of the wallet with product code CASH_WALLET_SPEND for user UID1 and the balance should be 440 SGD exact

    And I check the balance of the wallet with product code CASH_WALLET_SAVE for user UID1 and the balance should be 210 SGD exact

    #3rd time
    Then I deposit 200 SGD into wallet with product code CASH_WALLET_SPEND for user UID1 and expect a status code of 200

    And I check the balance of the wallet with product code CASH_WALLET_SPEND for user UID1 and the balance should be 640 SGD exact

    And I check the balance of the wallet with product code CASH_WALLET_SAVE for user UID1 and the balance should be 210 SGD exact

    #4th time
    Then I deposit 200 SGD into wallet with product code CASH_WALLET_SPEND for user UID1 and expect a status code of 200

    And I check the balance of the wallet with product code CASH_WALLET_SPEND for user UID1 and the balance should be 840 SGD exact

    And I wait for 20 seconds

    And I check the balance of the wallet with product code CASH_WALLET_SAVE for user UID1 and the balance should be 10 SGD exact
