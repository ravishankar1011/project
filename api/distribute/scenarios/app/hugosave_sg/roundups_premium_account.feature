Feature: Roundups

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

  Scenario: Enable Roundups, Trigger Roundup

    Then I get the user cash wallets for the user UID1 and expect the account status of CASH_ACCOUNT_STATUS_CREATED

    Then I order a physical card for UID1 with card name as random_valid_choice and expect a status code of 200 and expect a card status of CARD_STATUS_PENDING

    Then I wait for card status as CARD_STATUS_INACTIVE to activate PHYSICAL card for user UID1

    Then I wait for 40 seconds

    Then I activate the PHYSICAL card for the user UID1 with valid token, with status 200

    Then I check card status is CARD_STATUS_ACTIVE for user UID1 for PHYSICAL card

    Then I deposit 150 SGD into wallet with product code CASH_WALLET_SAVE for user UID1 and expect a status code of 200

    And I check the balance of the wallet with product code CASH_WALLET_SAVE for user UID1 and the balance should be 150 SGD exact

    Then I deposit 50 SGD into wallet with product code CASH_WALLET_SPEND for user UID1 and expect a status code of 200

    Given I ENABLE roundups for user UID1

    And I check if GOLD_VAULT is created for user UID1

    Then I save map PM_GOLD_VAULT for the Roundup Sweep for the user UID1

    Given I create below transaction for PHYSICAL card for user profile id and expect a status code of 200
      | user_profile_identifier | transaction_permutation_name | billing_amount | is_foreign_txn |
      | UID1                    | AUTH_CLEAR                   | 2.1            | false          |

    And I check the balance of the wallet with product code CASH_WALLET_ROUNDUP for user UID1 and the balance should be 0.9 SGD exact

    And I check the balance of the wallet with product code CASH_WALLET_SAVE for user UID1 and the balance should be 99.1 SGD exact

    Then I trigger schedule SCHEDULE_ROUNDUP for user UID1 and expect a status code of 200

    And I check the balance of the wallet with product code CASH_WALLET_ROUNDUP for user UID1 and the balance should be 0 SGD exact

    Then I check the balance of PM_GOLD_VAULT Map of user UID1 to be 0.9

    Given I create below transaction for PHYSICAL card for user profile id and expect a status code of 200
      | user_profile_identifier | transaction_permutation_name | billing_amount | is_foreign_txn |
      | UID1                    | AUTH_CLEAR                   | 2.1            | false          |

    And I check the balance of the wallet with product code CASH_WALLET_ROUNDUP for user UID1 and the balance should be 0.9 SGD exact

    And I check the balance of the wallet with product code CASH_WALLET_SAVE for user UID1 and the balance should be 98.2 SGD exact

    Then I deposit 98.2 SGD into wallet with product code CASH_WALLET_SPEND for user UID1 and expect a status code of 200

    And I check the balance of the wallet with product code CASH_WALLET_SAVE for user UID1 and the balance should be 0 SGD exact

    And I check the balance of the wallet with product code CASH_WALLET_SPEND for user UID1 and the balance should be 144 SGD exact

    #round-up transaction when SAVE account balance is Zero
    Given I create below transaction for PHYSICAL card for user profile id and expect a status code of 200
      | user_profile_identifier | transaction_permutation_name | billing_amount | is_foreign_txn |
      | UID1                    | AUTH_CLEAR                   | 141.2          | false          |

    And I check the balance of the wallet with product code CASH_WALLET_ROUNDUP for user UID1 and the balance should be 1.7 SGD exact

    And I check the balance of the wallet with product code CASH_WALLET_SPEND for user UID1 and the balance should be 2 SGD exact

    Then I deposit 5.5 SGD into wallet with product code CASH_WALLET_SAVE for user UID1 and expect a status code of 200

    And I check the balance of the wallet with product code CASH_WALLET_SAVE for user UID1 and the balance should be 5.5 SGD exact

    Then I deposit 5.5 SGD into wallet with product code CASH_WALLET_SPEND for user UID1 and expect a status code of 200

    And I check the balance of the wallet with product code CASH_WALLET_SPEND for user UID1 and the balance should be 7.5 SGD exact

    Given I create below transaction for PHYSICAL card for user profile id and expect a status code of 200
      | user_profile_identifier | transaction_permutation_name | billing_amount | is_foreign_txn |
      | UID1                    | AUTH_CLEAR                   | 7.5            | false          |

    And I check the balance of the wallet with product code CASH_WALLET_SPEND for user UID1 and the balance should be 0 SGD exact

    Then I get the user cash wallets for the user UID1 and expect the account status of CASH_ACCOUNT_STATUS_CREATED

    Then I verify below intent record in present in intents list
      | user_profile_identifier | product_code        | intent_type | intent_status | count | view    |
      | UID1                    | CASH_WALLET_ROUNDUP | ROUNDUP     | DECLINED      | 1     | roundup |
