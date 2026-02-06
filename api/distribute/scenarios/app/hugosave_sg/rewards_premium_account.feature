Feature: Reward Gold

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

  Scenario: Reward gold on account creation

    Then I get the unlocked rewards for user UID1

    Then I claim the reward for user UID1

    Then I check the balance of PM_GOLD_VAULT Map of user UID1 to be ACCOUNT_CREATION_REWARD

  Scenario: Reward gold on buying 50 SGD of gold

    And I check if GOLD_VAULT is created for user UID1

    Then I get the user cash wallets for the user UID1 and expect the account status of CASH_ACCOUNT_STATUS_CREATED

    Then I deposit 100 SGD into wallet with product code CASH_WALLET_SAVE for user UID1 and expect a status code of 200

    And I check the balance of the wallet with product code CASH_WALLET_SAVE for user UID1 and the balance should be 100 SGD exact

    Given I invest in PM_GOLD_VAULT vault map without rate and expect a status of PENDING
      | user_profile_identifier | transaction_amount | investment_amount | fee_amount | status_code |
      | UID1                    | 50                 | 50                | 0          | 200         |

    Then I check the balance of PM_GOLD_VAULT Map of user UID1 to be 50

    And I check the balance of the wallet with product code CASH_WALLET_SAVE for user UID1 and the balance should be 50 SGD approx

    Then I get the unlocked rewards for user UID1

    Then I claim the reward for user UID1

    Then I check the balance of PM_GOLD_VAULT Map of user UID1 to be GOLD_REWARD_VALUE

  Scenario: Reward on activating Physical Card

    Then I get the user cash wallets for the user UID1 and expect the account status of CASH_ACCOUNT_STATUS_CREATED

    Then I order a physical card for UID1 with card name as random_valid_choice and expect a status code of 200 and expect a card status of CARD_STATUS_PENDING

    Then I wait for card status as CARD_STATUS_INACTIVE to activate PHYSICAL card for user UID1

    Then I wait for 40 seconds

    Then I activate the PHYSICAL card for the user UID1 with valid token, with status 200

    Then I check card status is CARD_STATUS_ACTIVE for user UID1 for PHYSICAL card

    Then I get the unlocked rewards for user UID1

    Then I claim the reward for user UID1

    Then I check the balance of PM_GOLD_VAULT Map of user UID1 to be ACCOUNT_CREATION_REWARD

  Scenario: Reward on referring a user.

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

    Then I get the unlocked rewards for user UID1

    Then I claim the reward for user UID1

    Then I check the balance of PM_GOLD_VAULT Map of user UID1 to be ACCOUNT_CREATION_REWARD

    Then I get the unlocked rewards for user UID2

    Then I claim the reward for user UID2

    Then I check the balance of PM_GOLD_VAULT Map of user UID2 to be ACCOUNT_CREATION_REWARD

