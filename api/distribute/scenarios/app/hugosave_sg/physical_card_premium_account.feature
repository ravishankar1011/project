Feature: Card Order, Block-Unblock-Disabled, Transactions

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

  Scenario: Order Card -> Activate -> Block/Unblock -> Disable

    Then I get the user cash wallets for the user UID1 and expect the account status of CASH_ACCOUNT_STATUS_CREATED

    Then I order a physical card for UID1 with card name as random_valid_choice and expect a status code of 200 and expect a card status of CARD_STATUS_PENDING

    Then I wait for 10 seconds

    Then I wait for card status as CARD_STATUS_INACTIVE to activate PHYSICAL card for user UID1

    Then I wait for 40 seconds

    Then I activate the PHYSICAL card for the user UID1 with valid token, with status 200

    Then I check card status is CARD_STATUS_ACTIVE for user UID1 for PHYSICAL card

    Then I update the card status of the PHYSICAL card to BLOCK for user UID1 and expect a status code of 200

    Then I check card status is CARD_STATUS_BLOCKED for user UID1 for PHYSICAL card

    Then I update the card status of the PHYSICAL card to UNBLOCK for user UID1 and expect a status code of 200

    Then I check card status is CARD_STATUS_ACTIVE for user UID1 for PHYSICAL card

    Then I update the card status of the PHYSICAL card to DISABLE for user UID1 and expect a status code of 200

    Then I check card status is CARD_STATUS_DISABLED for user UID1 for PHYSICAL card

  Scenario: Replace Card

    Then I get the user cash wallets for the user UID1 and expect the account status of CASH_ACCOUNT_STATUS_CREATED

    Then I order a physical card for UID1 with card name as random_valid_choice and expect a status code of 200 and expect a card status of CARD_STATUS_PENDING

    Then I wait for card status as CARD_STATUS_INACTIVE to activate PHYSICAL card for user UID1

    Then I wait for 40 seconds

    Then I activate the PHYSICAL card for the user UID1 with valid token, with status 200

    Then I check card status is CARD_STATUS_ACTIVE for user UID1 for PHYSICAL card

    Then I replace the PHYSICAL card for user UID1 and expect a card status of CARD_STATUS_PENDING

    Then I check old card status is CARD_STATUS_DISABLED for user UID1 and get new card id

    Then I wait for card status as CARD_STATUS_INACTIVE to activate PHYSICAL card for user UID1

    Then I wait for 40 seconds

    Then I activate the PHYSICAL card for the user UID1 with valid token, with status 200

    Then I check card status is CARD_STATUS_ACTIVE for user UID1 for PHYSICAL card

  Scenario: Card Auto-top-up, top-up, withdraw

    Then I get the user cash wallets for the user UID1 and expect the account status of CASH_ACCOUNT_STATUS_CREATED

    Then I order a physical card for UID1 with card name as random_valid_choice and expect a status code of 200 and expect a card status of CARD_STATUS_PENDING

    Then I wait for card status as CARD_STATUS_INACTIVE to activate PHYSICAL card for user UID1

    Then I wait for 40 seconds

    Then I activate the PHYSICAL card for the user UID1 with valid token, with status 200

    Then I check card status is CARD_STATUS_ACTIVE for user UID1 for PHYSICAL card

    Then I deposit 200 SGD into wallet with product code CASH_WALLET_SAVE for user UID1 and expect a status code of 200

    And I check the balance of the wallet with product code CASH_WALLET_SAVE for user UID1 and the balance should be 200 SGD exact

    Then I deposit 50 SGD into wallet with product code CASH_WALLET_SPEND for user UID1 and expect a status code of 200

    And I check the balance of the wallet with product code CASH_WALLET_SPEND for user UID1 and the balance should be 50 SGD exact

    Given I setup auto topup for below cash wallet
      | user_profile_identifier | cash_wallet_id    | auto_topup_enabled | trigger_amount | topup_amount | is_external | funding_cash_wallet_id |
      | UID1                    | CASH_WALLET_SPEND | true               | 20             | 50           | false       | CASH_WALLET_SAVE       |

    Given I create below transaction for PHYSICAL card for user profile id and expect a status code of 200
      | user_profile_identifier | transaction_permutation_name | billing_amount | is_foreign_txn |
      | UID1                    | AUTH_CLEAR                   | 40             | false          |

    And I check the balance of the wallet with product code CASH_WALLET_SPEND for user UID1 and the balance should be 60 SGD exact

    And I check the balance of the wallet with product code CASH_WALLET_SAVE for user UID1 and the balance should be 100 SGD exact

    Given I create below transaction for PHYSICAL card for user profile id and expect a status code of 200
      | user_profile_identifier | transaction_permutation_name | billing_amount | is_foreign_txn |
      | UID1                    | AUTH_MULTI_CLEAR             | 50.0           | false          |

    And I check the balance of the wallet with product code CASH_WALLET_SPEND for user UID1 and the balance should be 60 SGD exact

    And I check the balance of the wallet with product code CASH_WALLET_SAVE for user UID1 and the balance should be 50 SGD exact

    #exact trigger amount balance
    Given I create below transaction for PHYSICAL card for user profile id and expect a status code of 200
      | user_profile_identifier | transaction_permutation_name | billing_amount | is_foreign_txn |
      | UID1                    | AUTH_CLEAR                   | 40             | false          |

    And I check the balance of the wallet with product code CASH_WALLET_SPEND for user UID1 and the balance should be 20 SGD exact

    And I check the balance of the wallet with product code CASH_WALLET_SAVE for user UID1 and the balance should be 50 SGD exact

    Then I disable auto-top-up of CASH_WALLET_SPEND for user UID1

    Given I create below transaction for PHYSICAL card for user profile id and expect a status code of 200
      | user_profile_identifier | transaction_permutation_name | billing_amount | is_foreign_txn |
      | UID1                    | AUTH_CLEAR                   | 10.0           | false          |

    And I check the balance of the wallet with product code CASH_WALLET_SPEND for user UID1 and the balance should be 10 SGD exact

    And I withdraw 10 SGD from card account of user UID1

  Scenario: Card negative balance claim

    Then I get the user cash wallets for the user UID1 and expect the account status of CASH_ACCOUNT_STATUS_CREATED

    Then I order a physical card for UID1 with card name as random_valid_choice and expect a status code of 200 and expect a card status of CARD_STATUS_PENDING

    Then I wait for card status as CARD_STATUS_INACTIVE to activate PHYSICAL card for user UID1

    Then I wait for 40 seconds

    Then I activate the PHYSICAL card for the user UID1 with valid token, with status 200

    Then I check card status is CARD_STATUS_ACTIVE for user UID1 for PHYSICAL card

    Then I deposit 50 SGD into wallet with product code CASH_WALLET_SAVE for user UID1 and expect a status code of 200

    And I check the balance of the wallet with product code CASH_WALLET_SAVE for user UID1 and the balance should be 50 SGD exact

    Then I deposit 50 SGD into wallet with product code CASH_WALLET_SPEND for user UID1 and expect a status code of 200

    And I check the balance of the wallet with product code CASH_WALLET_SPEND for user UID1 and the balance should be 50 SGD exact

    Given I create below transaction for PHYSICAL card for user profile id and expect a status code of 200
      | user_profile_identifier | transaction_permutation_name | billing_amount | is_foreign_txn |
      | UID1                    | CLEAR                        | 60             | false          |

    And I check the balance of the wallet with product code CASH_WALLET_SPEND for user UID1 and the balance should be -10 SGD exact

    Then I deposit 200 SGD into wallet with product code CASH_WALLET_SAVE for user UID1 and expect a status code of 200

    And I check the balance of the wallet with product code CASH_WALLET_SAVE for user UID1 and the balance should be 190 SGD exact

    And I check the balance of the wallet with product code CASH_WALLET_SPEND for user UID1 and the balance should be 0 SGD approx

  Scenario: Local Transactions - AUTH Cases - Roundups DISABLED

    Then I get the user cash wallets for the user UID1 and expect the account status of CASH_ACCOUNT_STATUS_CREATED

    Then I order a physical card for UID1 with card name as random_valid_choice and expect a status code of 200 and expect a card status of CARD_STATUS_PENDING

    Then I wait for card status as CARD_STATUS_INACTIVE to activate PHYSICAL card for user UID1

    Then I wait for 40 seconds

    Then I activate the PHYSICAL card for the user UID1 with valid token, with status 200

    Then I check card status is CARD_STATUS_ACTIVE for user UID1 for PHYSICAL card

    Given I deposit 50 SGD into wallet with product code CASH_WALLET_SAVE for user UID1 and expect a status code of 200

    And I check the balance of the wallet with product code CASH_WALLET_SAVE for user UID1 and the balance should be 50 SGD exact

    Given I deposit 50 SGD into wallet with product code CASH_WALLET_SPEND for user UID1 and expect a status code of 200

    And I check the balance of the wallet with product code CASH_WALLET_SPEND for user UID1 and the balance should be 50 SGD exact

    #    1. auth
    Given I create below transaction for PHYSICAL card for user profile id and expect a status code of 200
      | user_profile_identifier | transaction_permutation_name | billing_amount | is_foreign_txn |
      | UID1                    | AUTH                         | 10.3           | false          |

    And I check the balance of the wallet with product code CASH_WALLET_SPEND for user UID1 and the balance should be 39 SGD approx

    # 2. AUTH_CLEAR
    Given I create below transaction for PHYSICAL card for user profile id and expect a status code of 200
      | user_profile_identifier | transaction_permutation_name | billing_amount | is_foreign_txn |
      | UID1                    | AUTH_CLEAR                   | 5.5            | false          |

    And I check the balance of the wallet with product code CASH_WALLET_SPEND for user UID1 and the balance should be 34 SGD approx

    # 3. AUTH_PARTIAL_CLEARING
    Given I create below transaction for PHYSICAL card for user profile id and expect a status code of 200
      | user_profile_identifier | transaction_permutation_name | billing_amount | is_foreign_txn |
      | UID1                    | AUTH_PARTIAL_CLEARING        | 1.3            | false          |

    And I check the balance of the wallet with product code CASH_WALLET_SPEND for user UID1 and the balance should be 32 SGD approx

    #4. AUTH_MULTI_CLEARING
    Given I create below transaction for PHYSICAL card for user profile id and expect a status code of 200
      | user_profile_identifier | transaction_permutation_name | billing_amount | is_foreign_txn |
      | UID1                    | AUTH_MULTI_CLEAR             | 12.47          | false          |

    And I check the balance of the wallet with product code CASH_WALLET_SPEND for user UID1 and the balance should be 20 SGD approx

    # 5. AUTH_FR
    Given I create below transaction for PHYSICAL card for user profile id and expect a status code of 200
      | user_profile_identifier | transaction_permutation_name | billing_amount | is_foreign_txn |
      | UID1                    | AUTH_FR                      | 3.37           | false          |

    And I check the balance of the wallet with product code CASH_WALLET_SPEND for user UID1 and the balance should be 20 SGD approx

    #    6. AUTH_PR
    Given I create below transaction for PHYSICAL card for user profile id and expect a status code of 200
      | user_profile_identifier | transaction_permutation_name | billing_amount | is_foreign_txn |
      | UID1                    | AUTH_PR                      | 1.94           | false          |

    And I check the balance of the wallet with product code CASH_WALLET_SPEND for user UID1 and the balance should be 20 SGD approx

    #    7.AUTH_PR_FR ---- balance becomes [balance: 19.46]
    Given I create below transaction for PHYSICAL card for user profile id and expect a status code of 200
      | user_profile_identifier | transaction_permutation_name | billing_amount | is_foreign_txn |
      | UID1                    | AUTH_PR_FR                   | 3.33           | false          |

    And I check the balance of the wallet with product code CASH_WALLET_SPEND for user UID1 and the balance should be 20 SGD approx

    #8. AUTH_PR_CLEAR
    Given I create below transaction for PHYSICAL card for user profile id and expect a status code of 200
      | user_profile_identifier | transaction_permutation_name | billing_amount | is_foreign_txn |
      | UID1                    | AUTH_PR_CLEAR                | 8.19           | false          |

    And I check the balance of the wallet with product code CASH_WALLET_SPEND for user UID1 and the balance should be 15 SGD approx

    # 9. AUTH_PR_MULTI_CLEAR
    Given I create below transaction for PHYSICAL card for user profile id and expect a status code of 200
      | user_profile_identifier | transaction_permutation_name | billing_amount | is_foreign_txn |
      | UID1                    | AUTH_PR_MULTI_CLEAR          | 1.44           | false          |

    And I check the balance of the wallet with product code CASH_WALLET_SPEND for user UID1 and the balance should be 14 SGD approx

    #    9.1
    Given I create below transaction for PHYSICAL card for user profile id and expect a status code of 200
      | user_profile_identifier | transaction_permutation_name | billing_amount | is_foreign_txn |
      | UID1                    | AUTH_PR_MULTI_CLEAR          | 6.99           | false          |

    And I check the balance of the wallet with product code CASH_WALLET_SPEND for user UID1 and the balance should be 10 SGD approx


  Scenario: Local Transactions - Incremental Auth - Roundups DISABLED

    Then I get the user cash wallets for the user UID1 and expect the account status of CASH_ACCOUNT_STATUS_CREATED

    Then I order a physical card for UID1 with card name as random_valid_choice and expect a status code of 200 and expect a card status of CARD_STATUS_PENDING

    Then I wait for card status as CARD_STATUS_INACTIVE to activate PHYSICAL card for user UID1

    Then I wait for 40 seconds

    Then I activate the PHYSICAL card for the user UID1 with valid token, with status 200

    Then I check card status is CARD_STATUS_ACTIVE for user UID1 for PHYSICAL card

    Given I deposit 50 SGD into wallet with product code CASH_WALLET_SAVE for user UID1 and expect a status code of 200

    And I check the balance of the wallet with product code CASH_WALLET_SAVE for user UID1 and the balance should be 50 SGD exact

    Given I deposit 50 SGD into wallet with product code CASH_WALLET_SPEND for user UID1 and expect a status code of 200

    And I check the balance of the wallet with product code CASH_WALLET_SPEND for user UID1 and the balance should be 50 SGD exact

    And I check the balance of the wallet with product code CASH_WALLET_SPEND for user UID1 and the balance should be 50 SGD exact

    And I DISABLE roundups for user UID1

    And I wait for 10 seconds

    #   10 INC_AUTH
    Given I create below transaction for PHYSICAL card for user profile id and expect a status code of 200
      | user_profile_identifier | transaction_permutation_name | billing_amount | is_foreign_txn |
      | UID1                    | INC_AUTH                     | 0.937          | false          |

    And I check the balance of the wallet with product code CASH_WALLET_SPEND for user UID1 and the balance should be 49 SGD approx

    #    11 INC_AUTH_CLEAR
    Given I create below transaction for PHYSICAL card for user profile id and expect a status code of 200
      | user_profile_identifier | transaction_permutation_name | billing_amount | is_foreign_txn |
      | UID1                    | INC_AUTH_CLEAR               | 0.209          | false          |

    And I check the balance of the wallet with product code CASH_WALLET_SPEND for user UID1 and the balance should be 48 SGD approx

    #  12 INC_AUTH_PARTIAL_CLEARING
    Given I create below transaction for PHYSICAL card for user profile id and expect a status code of 200
      | user_profile_identifier | transaction_permutation_name | billing_amount | is_foreign_txn |
      | UID1                    | INC_AUTH_PARTIAL_CLEARING    | 2.51           | false          |

    And I check the balance of the wallet with product code CASH_WALLET_SPEND for user UID1 and the balance should be 46 SGD approx

    # 13 INC_AUTH_MULTI_CLEAR
    Given I create below transaction for PHYSICAL card for user profile id and expect a status code of 200
      | user_profile_identifier | transaction_permutation_name | billing_amount | is_foreign_txn |
      | UID1                    | INC_AUTH_MULTI_CLEAR         | 23.86          | false          |

    And I check the balance of the wallet with product code CASH_WALLET_SPEND for user UID1 and the balance should be 22 SGD approx

    #  14 INC_AUTH_FR
    Given I create below transaction for PHYSICAL card for user profile id and expect a status code of 200
      | user_profile_identifier | transaction_permutation_name | billing_amount | is_foreign_txn |
      | UID1                    | INC_AUTH_FR                  | 3.83           | false          |

    And I check the balance of the wallet with product code CASH_WALLET_SPEND for user UID1 and the balance should be 22 SGD approx

    #  15 INC_AUTH_PR
    Given I create below transaction for PHYSICAL card for user profile id and expect a status code of 200
      | user_profile_identifier | transaction_permutation_name | billing_amount | is_foreign_txn |
      | UID1                    | INC_AUTH_PR                  | 4.83           | false          |

    And I check the balance of the wallet with product code CASH_WALLET_SPEND for user UID1 and the balance should be 20 SGD approx

  #  15 INC_AUTH_PR_FR
    Given I create below transaction for PHYSICAL card for user profile id and expect a status code of 200
      | user_profile_identifier | transaction_permutation_name | billing_amount | is_foreign_txn |
      | UID1                    | INC_AUTH_PR_FR               | 6.19           | false          |

    And I check the balance of the wallet with product code CASH_WALLET_SPEND for user UID1 and the balance should be 20 SGD approx

    #  16 INC_AUTH_PR_CLEAR - not working
    Given I create below transaction for PHYSICAL card for user profile id and expect a status code of 200
      | user_profile_identifier | transaction_permutation_name | billing_amount | is_foreign_txn |
      | UID1                    | INC_AUTH_PR_CLEAR            | 5.67           | false          |

    And I check the balance of the wallet with product code CASH_WALLET_SPEND for user UID1 and the balance should be 17 SGD approx

    #  17 INC_AUTH_PR_MULTI_CLEAR
    Given I create below transaction for PHYSICAL card for user profile id and expect a status code of 200
      | user_profile_identifier | transaction_permutation_name | billing_amount | is_foreign_txn |
      | UID1                    | INC_AUTH_PR_MULTI_CLEAR      | 4.07           | false          |

    And I check the balance of the wallet with product code CASH_WALLET_SPEND for user UID1 and the balance should be 15 SGD approx


  Scenario: Local Transactions - Roundups ENABLED

    Then I get the user cash wallets for the user UID1 and expect the account status of CASH_ACCOUNT_STATUS_CREATED

    Then I order a physical card for UID1 with card name as random_valid_choice and expect a status code of 200 and expect a card status of CARD_STATUS_PENDING

    Then I wait for card status as CARD_STATUS_INACTIVE to activate PHYSICAL card for user UID1

    Then I wait for 40 seconds

    Then I activate the PHYSICAL card for the user UID1 with valid token, with status 200

    Then I check card status is CARD_STATUS_ACTIVE for user UID1 for PHYSICAL card

    Given I deposit 50 SGD into wallet with product code CASH_WALLET_SAVE for user UID1 and expect a status code of 200

    And I check the balance of the wallet with product code CASH_WALLET_SAVE for user UID1 and the balance should be 50 SGD exact

    Given I deposit 50 SGD into wallet with product code CASH_WALLET_SPEND for user UID1 and expect a status code of 200

    And I check the balance of the wallet with product code CASH_WALLET_SPEND for user UID1 and the balance should be 50 SGD exact

    And I ENABLE roundups for user UID1

    # 1. INC_AUTH WITH RU
    Given I create below transaction for PHYSICAL card for user profile id and expect a status code of 200
      | user_profile_identifier | transaction_permutation_name | billing_amount | is_foreign_txn |
      | UID1                    | INC_AUTH                     | 0.937          | false          |

    Then I check the balance of the wallet with product code CASH_WALLET_SPEND for user UID1 and the balance should be 49.06 SGD approx

    Then I check the balance of the wallet with product code CASH_WALLET_ROUNDUP for user UID1 and the balance should be 0 SGD approx

    # 2. AUTH_CLEAR with RU
    Given I create below transaction for PHYSICAL card for user profile id and expect a status code of 200
      | user_profile_identifier | transaction_permutation_name | billing_amount | is_foreign_txn |
      | UID1                    | AUTH_CLEAR                   | 5.5            | false          |

    Then I wait for 30 seconds

    Then I check if the intent with type CARD_TRANSACTION has the status SETTLED and a total of 1 intents exist for the user UID1 in the card view

    And I check the balance of the wallet with product code CASH_WALLET_SPEND for user UID1 and the balance should be 43.06 SGD approx

    And I check the balance of the wallet with product code CASH_WALLET_ROUNDUP for user UID1 and the balance should be 0.5 SGD approx

    # 3. AUTH_PARTIAL_CLEARING with RU
    Given I create below transaction for PHYSICAL card for user profile id and expect a status code of 200
      | user_profile_identifier | transaction_permutation_name | billing_amount | is_foreign_txn |
      | UID1                    | AUTH_PARTIAL_CLEARING        | 1.3            | false          |

    And I check the balance of the wallet with product code CASH_WALLET_SPEND for user UID1 and the balance should be 41.28 SGD approx

    And I check the balance of the wallet with product code CASH_WALLET_ROUNDUP for user UID1 and the balance should be 0.98 SGD approx

    #4. AUTH_MULTI_CLEARING
    Given I create below transaction for PHYSICAL card for user profile id and expect a status code of 200
      | user_profile_identifier | transaction_permutation_name | billing_amount | is_foreign_txn |
      | UID1                    | AUTH_MULTI_CLEAR             | 12.47          | false          |

    Then I wait for 20 seconds

    Then I check if the intent with type CARD_TRANSACTION has the status SETTLED and a total of 4 intents exist for the user UID1 in the card view

    And I check the balance of the wallet with product code CASH_WALLET_SPEND for user UID1 and the balance should be 29.25 SGD approx

    And I check the balance of the wallet with product code CASH_WALLET_ROUNDUP for user UID1 and the balance should be 1.24 SGD approx

    # 5. AUTH_FR
    Given I create below transaction for PHYSICAL card for user profile id and expect a status code of 200
      | user_profile_identifier | transaction_permutation_name | billing_amount | is_foreign_txn |
      | UID1                    | AUTH_FR                      | 3.37           | false          |

    Then I wait for 20 seconds

    Then I check if the intent with type CARD_TRANSACTION has the status REVERTED and a total of 1 intents exist for the user UID1 in the card view

    And I check the balance of the wallet with product code CASH_WALLET_SPEND for user UID1 and the balance should be 29.25 SGD approx

    And I check the balance of the wallet with product code CASH_WALLET_ROUNDUP for user UID1 and the balance should be 1.51 SGD approx

    #    6. AUTH_PR
    Given I create below transaction for PHYSICAL card for user profile id and expect a status code of 200
      | user_profile_identifier | transaction_permutation_name | billing_amount | is_foreign_txn |
      | UID1                    | AUTH_PR                      | 1.94           | false          |

    Then I check if the intent with type CARD_TRANSACTION has the status REVERTED and a total of 1 intents exist for the user UID1 in the card view

    Then I check if the intent with type CARD_TRANSACTION has the status SETTLED and a total of 4 intents exist for the user UID1 in the card view

    And I check the balance of the wallet with product code CASH_WALLET_SPEND for user UID1 and the balance should be 27.82 SGD approx

    And I check the balance of the wallet with product code CASH_WALLET_ROUNDUP for user UID1 and the balance should be 1.51 SGD approx

    #    7.AUTH_PR_FR ---- balance becomes [balance: 19.46]
    Given I create below transaction for PHYSICAL card for user profile id and expect a status code of 200
      | user_profile_identifier | transaction_permutation_name | billing_amount | is_foreign_txn |
      | UID1                    | AUTH_PR_FR                   | 3.33           | false          |

    Then I check if the intent with type CARD_TRANSACTION has the status REVERTED and a total of 2 intents exist for the user UID1 in the card view

    Then I check if the intent with type CARD_TRANSACTION has the status SETTLED and a total of 4 intents exist for the user UID1 in the card view

    And I check the balance of the wallet with product code CASH_WALLET_SPEND for user UID1 and the balance should be 27.82 SGD approx

    And I check the balance of the wallet with product code CASH_WALLET_ROUNDUP for user UID1 and the balance should be 1.51 SGD approx
      # 8. AUTH_PR_CLEAR  -
    Given I create below transaction for PHYSICAL card for user profile id and expect a status code of 200
      | user_profile_identifier | transaction_permutation_name | billing_amount | is_foreign_txn |
      | UID1                    | AUTH_PR_CLEAR                | 8.19           | false          |

    Then I wait for 20 seconds

    Then I check if the intent with type CARD_TRANSACTION has the status SETTLED and a total of 5 intents exist for the user UID1 in the card view

    And I check the balance of the wallet with product code CASH_WALLET_SPEND for user UID1 and the balance should be 22.91 SGD approx

    And I check the balance of the wallet with product code CASH_WALLET_ROUNDUP for user UID1 and the balance should be 1.6 SGD approx

    #  9 INC_AUTH_PR_MULTI_CLEAR
    Given I create below transaction for PHYSICAL card for user profile id and expect a status code of 200
      | user_profile_identifier | transaction_permutation_name | billing_amount | is_foreign_txn |
      | UID1                    | INC_AUTH_PR_MULTI_CLEAR      | 4.07           | false          |

    Then I wait for 20 seconds

    Then I check if the intent with type CARD_TRANSACTION has the status SETTLED and a total of 7 intents exist for the user UID1 in the card view

    And I check the balance of the wallet with product code CASH_WALLET_SPEND for user UID1 and the balance should be 19.3 SGD approx

    And I check the balance of the wallet with product code CASH_WALLET_ROUNDUP for user UID1 and the balance should be 2.97 SGD approx

    Then I DISABLE roundups for user UID1

    Then I wait for 10 seconds

    And I check the balance of the wallet with product code CASH_WALLET_SAVE for user UID1 and the balance should be 2.97 SGD approx

    Then I deposit 2.97 SGD into wallet with product code CASH_WALLET_SPEND for user UID1 and expect a status code of 200

    #  9 auth_clear with full balance
    Given I create below transaction for PHYSICAL card for user profile id and expect a status code of 200
      | user_profile_identifier | transaction_permutation_name | billing_amount | is_foreign_txn |
      | UID1                    | AUTH_CLEAR                   | 22.28          | false          |

    Then I wait for 20 seconds

    Then I check if the intent with type CARD_TRANSACTION has the status SETTLED and a total of 8 intents exist for the user UID1 in the card view

    And I check the balance of the wallet with product code CASH_WALLET_SPEND for user UID1 and the balance should be 0 SGD approx

    #  10 refund without round-up
    Given I create below transaction for PHYSICAL card for user profile id and expect a status code of 200
      | user_profile_identifier | transaction_permutation_name | billing_amount | is_foreign_txn |
      | UID1                    | REFUND_CLEAR                 | 22.28          | false          |

    And I check the balance of the wallet with product code CASH_WALLET_SPEND for user UID1 and the balance should be 22.28 SGD approx

    #  11 refund without round-up
    Given I create below transaction for PHYSICAL card for user profile id and expect a status code of 200
      | user_profile_identifier | transaction_permutation_name | billing_amount | is_foreign_txn |
      | UID1                    | REFUND_AUTH_REFUND_CLEAR     | 22.28          | false          |

    And I check the balance of the wallet with product code CASH_WALLET_SPEND for user UID1 and the balance should be 44.56 SGD approx

        #  12 refund without round-up
    Given I create below transaction for PHYSICAL card for user profile id and expect a status code of 200
      | user_profile_identifier | transaction_permutation_name | billing_amount | is_foreign_txn |
      | UID1                    | REFUND_AUTH                  | 2.1            | false          |

    And I check the balance of the wallet with product code CASH_WALLET_SPEND for user UID1 and the balance should be 44.56 SGD approx

    Then I ENABLE roundups for user UID1

        #  13 refund without round-up
    Given I create below transaction for PHYSICAL card for user profile id and expect a status code of 200
      | user_profile_identifier | transaction_permutation_name | billing_amount | is_foreign_txn |
      | UID1                    | REFUND_AUTH                  | 2.1            | false          |

    And I check the balance of the wallet with product code CASH_WALLET_SPEND for user UID1 and the balance should be 44.56 SGD approx

    And I check the balance of the wallet with product code CASH_WALLET_ROUNDUP for user UID1 and the balance should be 0 SGD approx

#  14 refund without round-up
    Given I create below transaction for PHYSICAL card for user profile id and expect a status code of 200
      | user_profile_identifier | transaction_permutation_name | billing_amount | is_foreign_txn |
      | UID1                    | REFUND_CLEAR                 | 22.28          | false          |

    And I check the balance of the wallet with product code CASH_WALLET_SPEND for user UID1 and the balance should be 66.84 SGD approx

    And I check the balance of the wallet with product code CASH_WALLET_ROUNDUP for user UID1 and the balance should be 0 SGD approx

  Scenario: Foreign Transactions - Roundups ENABLED

    Then I get the user cash wallets for the user UID1 and expect the account status of CASH_ACCOUNT_STATUS_CREATED

    Then I order a physical card for UID1 with card name as random_valid_choice and expect a status code of 200 and expect a card status of CARD_STATUS_PENDING

    Then I wait for card status as CARD_STATUS_INACTIVE to activate PHYSICAL card for user UID1

    Then I wait for 40 seconds

    Then I activate the PHYSICAL card for the user UID1 with valid token, with status 200

    Then I check card status is CARD_STATUS_ACTIVE for user UID1 for PHYSICAL card

    Then I deposit 750 SGD into wallet with product code CASH_WALLET_SAVE for user UID1 and expect a status code of 200

    And I check the balance of the wallet with product code CASH_WALLET_SAVE for user UID1 and the balance should be 750 SGD exact

    Then I deposit 750 SGD into wallet with product code CASH_WALLET_SPEND for user UID1 and expect a status code of 200

    And I check the balance of the wallet with product code CASH_WALLET_SPEND for user UID1 and the balance should be 750 SGD exact

    And I ENABLE roundups for user UID1

    #    1. auth
    Given I create below transaction for PHYSICAL card for user profile id and expect a status code of 200
      | user_profile_identifier | transaction_permutation_name | billing_amount | is_foreign_txn |
      | UID1                    | AUTH                         | 9.86           | true           |

    And I check the balance of the wallet with product code CASH_WALLET_SPEND for user UID1 and the balance should be 740.04 SGD approx

      #0.1 and the balance should be txn fee for foreign
    And I check the balance of the wallet with product code CASH_WALLET_ROUNDUP for user UID1 and the balance should be 0 SGD approx

    # 2. AUTH_CLEAR with RU
    Given I create below transaction for PHYSICAL card for user profile id and expect a status code of 200
      | user_profile_identifier | transaction_permutation_name | billing_amount | is_foreign_txn |
      | UID1                    | AUTH_CLEAR                   | 5.5            | true           |

    Then I wait for 20 seconds

    Then I check if the intent with type CARD_TRANSACTION has the status SETTLED and a total of 1 intents exist for the user UID1 in the card view

    And I check the balance of the wallet with product code CASH_WALLET_SPEND for user UID1 and the balance should be 734.04 SGD approx

    And I check the balance of the wallet with product code CASH_WALLET_ROUNDUP for user UID1 and the balance should be 0.5 SGD exact

    # 3. AUTH_PARTIAL_CLEARING with RU
    Given I create below transaction for PHYSICAL card for user profile id and expect a status code of 200
      | user_profile_identifier | transaction_permutation_name | billing_amount | is_foreign_txn |
      | UID1                    | AUTH_PARTIAL_CLEARING        | 1.3            | true           |

    Then I wait for 20 seconds

    Then I check if the intent with type CARD_TRANSACTION has the status SETTLED and a total of 2 intents exist for the user UID1 in the card view

    And I check the balance of the wallet with product code CASH_WALLET_SPEND for user UID1 and the balance should be 732.25 SGD approx

    And I check the balance of the wallet with product code CASH_WALLET_ROUNDUP for user UID1 and the balance should be 0.98 SGD approx

    #4. AUTH_MULTI_CLEARING
    Given I create below transaction for PHYSICAL card for user profile id and expect a status code of 200
      | user_profile_identifier | transaction_permutation_name | billing_amount | is_foreign_txn |
      | UID1                    | AUTH_MULTI_CLEAR             | 12.47          | true           |

    Then I wait for 20 seconds

    Then I check if the intent with type CARD_TRANSACTION has the status SETTLED and a total of 4 intents exist for the user UID1 in the card view

    And I check the balance of the wallet with product code CASH_WALLET_SPEND for user UID1 and the balance should be 719.14 SGD approx

    And I check the balance of the wallet with product code CASH_WALLET_ROUNDUP for user UID1 and the balance should be 1.24 SGD approx

    # 5. AUTH_FR
    Given I create below transaction for PHYSICAL card for user profile id and expect a status code of 200
      | user_profile_identifier | transaction_permutation_name | billing_amount | is_foreign_txn |
      | UID1                    | AUTH_FR                      | 3.37           | true           |

    Then I wait for 20 seconds

    Then I check if the intent with type CARD_TRANSACTION has the status REVERTED and a total of 1 intents exist for the user UID1 in the card view

    And I check the balance of the wallet with product code CASH_WALLET_SPEND for user UID1 and the balance should be 720.76 SGD approx

    And I check the balance of the wallet with product code CASH_WALLET_ROUNDUP for user UID1 and the balance should be 1.51 SGD approx

    #    6. AUTH_PR
    Given I create below transaction for PHYSICAL card for user profile id and expect a status code of 200
      | user_profile_identifier | transaction_permutation_name | billing_amount | is_foreign_txn |
      | UID1                    | AUTH_PR                      | 1.94           | true           |

    Then I wait for 20 seconds

    Then I check if the intent with type CARD_TRANSACTION has the status SETTLED and a total of 4 intents exist for the user UID1 in the card view

    Then I check if the intent with type CARD_TRANSACTION has the status REVERTED and a total of 2 intents exist for the user UID1 in the card view

    And I check the balance of the wallet with product code CASH_WALLET_SPEND for user UID1 and the balance should be 719.14 SGD approx

    And I check the balance of the wallet with product code CASH_WALLET_ROUNDUP for user UID1 and the balance should be 1.51 SGD approx

    #    7.AUTH_PR_FR
    Given I create below transaction for PHYSICAL card for user profile id and expect a status code of 200
      | user_profile_identifier | transaction_permutation_name | billing_amount | is_foreign_txn |
      | UID1                    | AUTH_PR_FR                   | 3.33           | true           |

    Then I wait for 20 seconds

    Then I check if the intent with type CARD_TRANSACTION has the status SETTLED and a total of 4 intents exist for the user UID1 in the card view

    Then I check if the intent with type CARD_TRANSACTION has the status REVERTED and a total of 3 intents exist for the user UID1 in the card view

    And I check the balance of the wallet with product code CASH_WALLET_SPEND for user UID1 and the balance should be 718.14 SGD approx

    And I check the balance of the wallet with product code CASH_WALLET_ROUNDUP for user UID1 and the balance should be 1.51 SGD approx

    # 8. AUTH_PR_CLEAR  -
    Given I create below transaction for PHYSICAL card for user profile id and expect a status code of 200
      | user_profile_identifier | transaction_permutation_name | billing_amount | is_foreign_txn |
      | UID1                    | AUTH_PR_CLEAR                | 8.19           | true           |

    Then I wait for 20 seconds

    Then I check if the intent with type CARD_TRANSACTION has the status SETTLED and a total of 5 intents exist for the user UID1 in the card view

    Then I check if the intent with type CARD_TRANSACTION has the status REVERTED and a total of 4 intents exist for the user UID1 in the card view

    And I check the balance of the wallet with product code CASH_WALLET_SPEND for user UID1 and the balance should be 713.14 SGD approx

    And I check the balance of the wallet with product code CASH_WALLET_ROUNDUP for user UID1 and the balance should be 1.59 SGD approx

    #  9 INC_AUTH_PR_MULTI_CLEAR
    Given I create below transaction for PHYSICAL card for user profile id and expect a status code of 200
      | user_profile_identifier | transaction_permutation_name | billing_amount | is_foreign_txn |
      | UID1                    | INC_AUTH_PR_MULTI_CLEAR      | 4.07           | true           |

    Then I wait for 20 seconds

    Then I check if the intent with type CARD_TRANSACTION has the status SETTLED and a total of 7 intents exist for the user UID1 in the card view

    Then I check if the intent with type CARD_TRANSACTION has the status REVERTED and a total of 5 intents exist for the user UID1 in the card view

    And I check the balance of the wallet with product code CASH_WALLET_SPEND for user UID1 and the balance should be 710.12 SGD approx

    And I check the balance of the wallet with product code CASH_WALLET_ROUNDUP for user UID1 and the balance should be 2.97 SGD approx

        #  13 refund_AUTH round-up
    Given I create below transaction for PHYSICAL card for user profile id and expect a status code of 200
      | user_profile_identifier | transaction_permutation_name | billing_amount | is_foreign_txn |
      | UID1                    | REFUND_AUTH                  | 2.1            | true           |

    Then I wait for 20 seconds

    And I check the balance of the wallet with product code CASH_WALLET_SPEND for user UID1 and the balance should be 710.12 SGD approx

    And I check the balance of the wallet with product code CASH_WALLET_ROUNDUP for user UID1 and the balance should be 2.97 SGD approx

    #  14 refund_CLEAR  round-up
    Given I create below transaction for PHYSICAL card for user profile id and expect a status code of 200
      | user_profile_identifier | transaction_permutation_name | billing_amount | is_foreign_txn |
      | UID1                    | REFUND_CLEAR                 | 22.28          | true           |

    Then I wait for 20 seconds

    Then I check if the intent with type CARD_TRANSACTION has the status SETTLED and a total of 8 intents exist for the user UID1 in the card view

    Then I check if the intent with type CARD_TRANSACTION has the status REVERTED and a total of 6 intents exist for the user UID1 in the card view

    And I check the balance of the wallet with product code CASH_WALLET_SPEND for user UID1 and the balance should be 732.4 SGD approx

    And I check the balance of the wallet with product code CASH_WALLET_ROUNDUP for user UID1 and the balance should be 2.97 SGD approx

    #  15 REFUND_AUTH_REFUND_CLEAR  round-up
    Given I create below transaction for PHYSICAL card for user profile id and expect a status code of 200
      | user_profile_identifier | transaction_permutation_name | billing_amount | is_foreign_txn |
      | UID1                    | REFUND_AUTH_REFUND_CLEAR     | 22.28          | true           |

    Then I wait for 20 seconds

    Then I check if the intent with type CARD_TRANSACTION has the status SETTLED and a total of 9 intents exist for the user UID1 in the card view

    Then I check if the intent with type CARD_TRANSACTION has the status REVERTED and a total of 7 intents exist for the user UID1 in the card view

    And I check the balance of the wallet with product code CASH_WALLET_SPEND for user UID1 and the balance should be 754.68 SGD approx

    And I check the balance of the wallet with product code CASH_WALLET_ROUNDUP for user UID1 and the balance should be 2.97 SGD approx

    And I DISABLE roundups for user UID1

    And I check the balance of the wallet with product code CASH_WALLET_SPEND for user UID1 and the balance should be 757.65 SGD approx

    Given I create below transaction for PHYSICAL card for user profile id and expect a status code of 200
      | user_profile_identifier | transaction_permutation_name | billing_amount | is_foreign_txn |
      | UID1                    | AUTH_CLEAR                   | 657.65         | true           |

    Then I wait for 20 seconds

    Then I check if the intent with type CARD_TRANSACTION has the status SETTLED and a total of 10 intents exist for the user UID1 in the card view

    And I check the balance of the wallet with product code CASH_WALLET_SPEND for user UID1 and the balance should be 100 SGD approx

  Scenario: Negative Scenarios - Invalid Billing Amounts - Balance should not be deducted for user

    Then I get the user cash wallets for the user UID1 and expect the account status of CASH_ACCOUNT_STATUS_CREATED

    Then I order a physical card for UID1 with card name as random_valid_choice and expect a status code of 200 and expect a card status of CARD_STATUS_PENDING

    Then I wait for card status as CARD_STATUS_INACTIVE to activate PHYSICAL card for user UID1

    Then I wait for 40 seconds

    Then I activate the PHYSICAL card for the user UID1 with valid token, with status 200

    Then I check card status is CARD_STATUS_ACTIVE for user UID1 for PHYSICAL card

    Then I deposit 100 SGD into wallet with product code CASH_WALLET_SAVE for user UID1 and expect a status code of 200

    And I check the balance of the wallet with product code CASH_WALLET_SAVE for user UID1 and the balance should be 100 SGD exact

    Then I deposit 100 SGD into wallet with product code CASH_WALLET_SPEND for user UID1 and expect a status code of 200

    And I check the balance of the wallet with product code CASH_WALLET_SPEND for user UID1 and the balance should be 100 SGD exact

    #    1. auth
#    Given I create below transaction for user profile id and expect a status code of HSA_9000
    Given I create below transaction for PHYSICAL card for user profile id and expect a status code of HSA_9000
      | user_profile_identifier | transaction_permutation_name | billing_amount | is_foreign_txn |
      | UID1                    | AUTH                         | 0              | false         |

    And I check the balance of the wallet with product code CASH_WALLET_SPEND for user UID1 and the balance should be 100 SGD approx

    # 2. AUTH_CLEAR with RU
    Given I create below transaction for PHYSICAL card for user profile id and expect a status code of HSA_9000
      | user_profile_identifier | transaction_permutation_name | billing_amount   | is_foreign_txn |
      | UID1                    | AUTH_CLEAR                   | 0                | true           |
      | UID1                    | AUTH_CLEAR                   | -2948.2          | true           |
      | UID1                    | AUTH_CLEAR                   | someGarbageValue | false          |

    And I check the balance of the wallet with product code CASH_WALLET_SPEND for user UID1 and the balance should be 100 SGD approx

    # 3. AUTH_PARTIAL_CLEARING with RU
    Given I create below transaction for PHYSICAL card for user profile id and expect a status code of HSA_9000
      | user_profile_identifier | transaction_permutation_name | billing_amount   | is_foreign_txn |
      | UID1                    | AUTH_PARTIAL_CLEARING        | 0                | false          |
      | UID1                    | AUTH_PARTIAL_CLEARING        | -2948.2          | true           |
      | UID1                    | AUTH_PARTIAL_CLEARING        | someGarbageValue | false          |

    And I check the balance of the wallet with product code CASH_WALLET_SPEND for user UID1 and the balance should be 100 SGD approx

    #4. AUTH_MULTI_CLEARING
    Given I create below transaction for PHYSICAL card for user profile id and expect a status code of HSA_9000
      | user_profile_identifier | transaction_permutation_name | billing_amount   | is_foreign_txn |
      | UID1                    | AUTH_MULTI_CLEAR             | 0                | true           |
      | UID1                    | AUTH_MULTI_CLEAR             | -2948.2          | true           |
      | UID1                    | AUTH_MULTI_CLEAR             | someGarbageValue | false          |

    And I check the balance of the wallet with product code CASH_WALLET_SPEND for user UID1 and the balance should be 100 SGD approx

    # 5. AUTH_FR
    Given I create below transaction for PHYSICAL card for user profile id and expect a status code of HSA_9000
      | user_profile_identifier | transaction_permutation_name | billing_amount   | is_foreign_txn |
      | UID1                    | AUTH_FR                      | 0                | false          |
      | UID1                    | AUTH_FR                      | -2948.2          | true           |
      | UID1                    | AUTH_FR                      | someGarbageValue | false          |

    And I check the balance of the wallet with product code CASH_WALLET_SPEND for user UID1 and the balance should be 100 SGD approx

    #    6. AUTH_PR
    Given I create below transaction for PHYSICAL card for user profile id and expect a status code of HSA_9000
      | user_profile_identifier | transaction_permutation_name | billing_amount   | is_foreign_txn |
      | UID1                    | AUTH_PR                      | 0                | false          |
      | UID1                    | AUTH_PR                      | -0.2             | true           |
      | UID1                    | AUTH_PR                      | someGarbageValue | false          |

    And I check the balance of the wallet with product code CASH_WALLET_SPEND for user UID1 and the balance should be 100 SGD approx

      #    7.AUTH_PR_FR
    Given I create below transaction for PHYSICAL card for user profile id and expect a status code of HSA_9000
      | user_profile_identifier | transaction_permutation_name | billing_amount   | is_foreign_txn |
      | UID1                    | AUTH_PR_FR                   | 0                | false          |
      | UID1                    | AUTH_PR_FR                   | -2948.2          | true           |
      | UID1                    | AUTH_PR_FR                   | someGarbageValue | false          |

    And I check the balance of the wallet with product code CASH_WALLET_SPEND for user UID1 and the balance should be 100 SGD approx

      # 8. AUTH_PR_CLEAR  -
    Given I create below transaction for PHYSICAL card for user profile id and expect a status code of HSA_9000
      | user_profile_identifier | transaction_permutation_name | billing_amount   | is_foreign_txn |
      | UID1                    | AUTH_PR_CLEAR                | 0                | false          |
      | UID1                    | AUTH_PR_CLEAR                | -282141124.2     | true           |
      | UID1                    | AUTH_PR_CLEAR                | someGarbageValue | false          |

    And I check the balance of the wallet with product code CASH_WALLET_SPEND for user UID1 and the balance should be 100 SGD approx

      #  9 INC_AUTH_PR_MULTI_CLEAR
    Given I create below transaction for PHYSICAL card for user profile id and expect a status code of HSA_9000
      | user_profile_identifier | transaction_permutation_name | billing_amount   | is_foreign_txn |
      | UID1                    | INC_AUTH_PR_MULTI_CLEAR      | 0                | false          |
      | UID1                    | INC_AUTH_PR_MULTI_CLEAR      | -28.2            | true           |
      | UID1                    | INC_AUTH_PR_MULTI_CLEAR      | someGarbageValue | false          |

    And I check the balance of the wallet with product code CASH_WALLET_SPEND for user UID1 and the balance should be 100 SGD approx

      #  13 refund_AUTH
    Given I create below transaction for PHYSICAL card for user profile id and expect a status code of HSA_9000
      | user_profile_identifier | transaction_permutation_name | billing_amount   | is_foreign_txn |
      | UID1                    | REFUND_AUTH                  | 0                | false          |
      | UID1                    | REFUND_AUTH                  | -02              | true           |
      | UID1                    | REFUND_AUTH                  | someGarbageValue | false          |

    And I check the balance of the wallet with product code CASH_WALLET_SPEND for user UID1 and the balance should be 100 SGD approx

      #  14 refund_CLEAR
    Given I create below transaction for PHYSICAL card for user profile id and expect a status code of HSA_9000
      | user_profile_identifier | transaction_permutation_name | billing_amount   | is_foreign_txn |
      | UID1                    | REFUND_CLEAR                 | 0                | false          |
      | UID1                    | REFUND_CLEAR                 | -48.2            | true           |
      | UID1                    | REFUND_CLEAR                 | someGarbageValue | false          |

    And I check the balance of the wallet with product code CASH_WALLET_SPEND for user UID1 and the balance should be 100 SGD approx

    Given I create below transaction for PHYSICAL card for user profile id and expect a status code of HSA_9000
      | user_profile_identifier | transaction_permutation_name | billing_amount   | is_foreign_txn |
#      | UID1                    | REFUND_AUTH_REFUND_CLEAR     | -21.48.2         | true           |
      | UID1                    | REFUND_AUTH_REFUND_CLEAR     | 0                | false          |
      | UID1                    | REFUND_AUTH_REFUND_CLEAR     | someGarbageValue | false          |

    And I check the balance of the wallet with product code CASH_WALLET_SPEND for user UID1 and the balance should be 100 SGD approx

    Given I create below transaction for PHYSICAL card for user profile id and expect a status code of E9409
      | user_profile_identifier | transaction_permutation_name | billing_amount   | is_foreign_txn |
      | UID1                    | REFUND_AUTH_REFUND_CLEAR     | -21.48.2         | true           |

    And I check the balance of the wallet with product code CASH_WALLET_SPEND for user UID1 and the balance should be 100 SGD approx

  Scenario: Card - Failure Scenarios

    Then I get the user cash wallets for the user UID1 and expect the account status of CASH_ACCOUNT_STATUS_CREATED

    Then I order a physical card for UID1 with card name as random_valid_choice and expect a status code of 200 and expect a card status of CARD_STATUS_PENDING

    Then I wait for card status as CARD_STATUS_INACTIVE to activate PHYSICAL card for user UID1

    Then I wait for 40 seconds

    Then I activate the PHYSICAL card for the user UID1 with valid token, with status HSA_9102

    Then Invalid card scenario, activate_invalid_card_id, for user UID1 with status HSA_9105

    Then I check card status is CARD_STATUS_INACTIVE for user UID1 for PHYSICAL card

    Then I wait for card status as CARD_STATUS_INACTIVE to activate PHYSICAL card for user UID1

    Then I wait for 40 seconds

    Then I activate the PHYSICAL card for the user UID1 with valid token, with status 200

    Then I check card status is CARD_STATUS_ACTIVE for user UID1 for PHYSICAL card

    Then I update the card status of the PHYSICAL card to INVALID_ACTION for user UID1 and expect a status code of HSA_9179

    Then Invalid card scenario, get_details_invalid_card_id, for user UID1 with status HSA_9105

    Then Invalid card scenario, get_secure_invalid_card_id, for user UID1 with status HSA_9105

    Then Invalid card scenario, update_status_invalid_card_id, for user UID1 with status HSA_9105
