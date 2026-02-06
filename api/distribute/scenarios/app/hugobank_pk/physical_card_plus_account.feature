Feature: Cards Integration tests for PLUS account

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

    Given I add a new Home Address to order a Card for user UID1 and expect a status code of 200

    Then I check if the Home Address is added successfully for the user UID1

  Scenario: Order -> Activate -> Block/Unblock -> DISABLE Physical VISA Card

    Then I initiate the initial user authorisation to ORDER_CARD for user UID1 and expect a status of USER_AUTHORISATION_SUCCESS

    Then I initiate the final user authorisation to ORDER_CARD and expect a user authorisation status as USER_AUTHORISATION_INITIATED for user UID1

    And I initiate the PASSCODE journey within the PASSCODE_STEP for user UID1 to authorise the user and expect a status JOURNEY_INITIATED

    Then I process the PASSCODE journey within the PASSCODE_STEP for user UID1 to authorise the user and expect a status JOURNEY_PROCESSED

    And I submit the PASSCODE journey within the PASSCODE_STEP for user UID1 to authorise the user and expect a status JOURNEY_SUCCESSFUL

    Then I submit the final user authorisation for ORDER_CARD of user UID1 and expect a status USER_AUTHORISATION_SUBMITTED

    And I get the final user authorisation token for ORDER_CARD of user UID1 and expect a status USER_AUTHORISATION_SUCCESS

    Then I get the user cash wallets for the user UID1 and expect the account status of CASH_ACCOUNT_STATUS_CREATED

    Then I order a physical visa card for UID1 with card name as random_valid_choice and expect a status code of 200 and expect a card status of CARD_STATUS_PENDING

    Then I initiate the initial user authorisation to ACTIVATE_CARD for user UID1 and expect a status of USER_AUTHORISATION_SUCCESS

    Then I initiate the final user authorisation to ACTIVATE_CARD and expect a user authorisation status as USER_AUTHORISATION_INITIATED for user UID1

    And I initiate the PASSCODE journey within the PASSCODE_STEP for user UID1 to authorise the user and expect a status JOURNEY_INITIATED

    Then I process the PASSCODE journey within the PASSCODE_STEP for user UID1 to authorise the user and expect a status JOURNEY_PROCESSED

    And I submit the PASSCODE journey within the PASSCODE_STEP for user UID1 to authorise the user and expect a status JOURNEY_SUCCESSFUL

    Then I submit the final user authorisation for ACTIVATE_CARD of user UID1 and expect a status USER_AUTHORISATION_SUBMITTED

    And I get the final user authorisation token for ACTIVATE_CARD of user UID1 and expect a status USER_AUTHORISATION_SUCCESS

    Then I wait for card status as CARD_STATUS_UPGRADED to activate PHYSICAL card for user UID1

    Then I wait for 40 seconds

    Then I activate the PHYSICAL card for the user UID1 with valid token, with status 200

    Then I check card status is CARD_STATUS_ACTIVE for user UID1 for PHYSICAL card

    Then I initiate the initial user authorisation to UPDATE_CARD_STATUS for user UID1 and expect a status of USER_AUTHORISATION_SUCCESS

    Then I initiate the final user authorisation to UPDATE_CARD_STATUS and expect a user authorisation status as USER_AUTHORISATION_INITIATED for user UID1

    And I initiate the PASSCODE journey within the PASSCODE_STEP for user UID1 to authorise the user and expect a status JOURNEY_INITIATED

    Then I process the PASSCODE journey within the PASSCODE_STEP for user UID1 to authorise the user and expect a status JOURNEY_PROCESSED

    And I submit the PASSCODE journey within the PASSCODE_STEP for user UID1 to authorise the user and expect a status JOURNEY_SUCCESSFUL

    Then I submit the final user authorisation for UPDATE_CARD_STATUS of user UID1 and expect a status USER_AUTHORISATION_SUBMITTED

    And I get the final user authorisation token for UPDATE_CARD_STATUS of user UID1 and expect a status USER_AUTHORISATION_SUCCESS

    Then I update the card status of the PHYSICAL card to BLOCK for user UID1 and expect a status code of 200

    Then I check card status is CARD_STATUS_BLOCKED for user UID1 for PHYSICAL card

    Then I initiate the initial user authorisation to UPDATE_CARD_STATUS for user UID1 and expect a status of USER_AUTHORISATION_SUCCESS

    Then I initiate the final user authorisation to UPDATE_CARD_STATUS and expect a user authorisation status as USER_AUTHORISATION_INITIATED for user UID1

    And I initiate the PASSCODE journey within the PASSCODE_STEP for user UID1 to authorise the user and expect a status JOURNEY_INITIATED

    Then I process the PASSCODE journey within the PASSCODE_STEP for user UID1 to authorise the user and expect a status JOURNEY_PROCESSED

    And I submit the PASSCODE journey within the PASSCODE_STEP for user UID1 to authorise the user and expect a status JOURNEY_SUCCESSFUL

    Then I submit the final user authorisation for UPDATE_CARD_STATUS of user UID1 and expect a status USER_AUTHORISATION_SUBMITTED

    And I get the final user authorisation token for UPDATE_CARD_STATUS of user UID1 and expect a status USER_AUTHORISATION_SUCCESS

    Then I update the card status of the PHYSICAL card to UNBLOCK for user UID1 and expect a status code of 200

    Then I check card status is CARD_STATUS_ACTIVE for user UID1 for PHYSICAL card

    Then I initiate the initial user authorisation to UPDATE_CARD_STATUS for user UID1 and expect a status of USER_AUTHORISATION_SUCCESS

    Then I initiate the final user authorisation to UPDATE_CARD_STATUS and expect a user authorisation status as USER_AUTHORISATION_INITIATED for user UID1

    And I initiate the PASSCODE journey within the PASSCODE_STEP for user UID1 to authorise the user and expect a status JOURNEY_INITIATED

    Then I process the PASSCODE journey within the PASSCODE_STEP for user UID1 to authorise the user and expect a status JOURNEY_PROCESSED

    And I submit the PASSCODE journey within the PASSCODE_STEP for user UID1 to authorise the user and expect a status JOURNEY_SUCCESSFUL

    Then I submit the final user authorisation for UPDATE_CARD_STATUS of user UID1 and expect a status USER_AUTHORISATION_SUBMITTED

    And I get the final user authorisation token for UPDATE_CARD_STATUS of user UID1 and expect a status USER_AUTHORISATION_SUCCESS

    Then I update the card status of the PHYSICAL card to DISABLE for user UID1 and expect a status code of 200

    Then I check card status is CARD_STATUS_DISABLED for user UID1 for PHYSICAL card

  Scenario: Order -> Activate -> Block/Unblock -> DISABLE Physical PAYPAK Card

    Then I initiate the initial user authorisation to ORDER_CARD for user UID1 and expect a status of USER_AUTHORISATION_SUCCESS

    Then I initiate the final user authorisation to ORDER_CARD and expect a user authorisation status as USER_AUTHORISATION_INITIATED for user UID1

    And I initiate the PASSCODE journey within the PASSCODE_STEP for user UID1 to authorise the user and expect a status JOURNEY_INITIATED

    Then I process the PASSCODE journey within the PASSCODE_STEP for user UID1 to authorise the user and expect a status JOURNEY_PROCESSED

    And I submit the PASSCODE journey within the PASSCODE_STEP for user UID1 to authorise the user and expect a status JOURNEY_SUCCESSFUL

    Then I submit the final user authorisation for ORDER_CARD of user UID1 and expect a status USER_AUTHORISATION_SUBMITTED

    And I get the final user authorisation token for ORDER_CARD of user UID1 and expect a status USER_AUTHORISATION_SUCCESS

    Then I get the user cash wallets for the user UID1 and expect the account status of CASH_ACCOUNT_STATUS_CREATED

    Then I order a physical card for UID1 with card name as random_valid_choice and expect a status code of 200 and expect a card status of CARD_STATUS_PENDING

    Then I initiate the initial user authorisation to ACTIVATE_CARD for user UID1 and expect a status of USER_AUTHORISATION_SUCCESS

    Then I initiate the final user authorisation to ACTIVATE_CARD and expect a user authorisation status as USER_AUTHORISATION_INITIATED for user UID1

    And I initiate the PASSCODE journey within the PASSCODE_STEP for user UID1 to authorise the user and expect a status JOURNEY_INITIATED

    Then I process the PASSCODE journey within the PASSCODE_STEP for user UID1 to authorise the user and expect a status JOURNEY_PROCESSED

    And I submit the PASSCODE journey within the PASSCODE_STEP for user UID1 to authorise the user and expect a status JOURNEY_SUCCESSFUL

    Then I submit the final user authorisation for ACTIVATE_CARD of user UID1 and expect a status USER_AUTHORISATION_SUBMITTED

    And I get the final user authorisation token for ACTIVATE_CARD of user UID1 and expect a status USER_AUTHORISATION_SUCCESS

    Then I wait for card status as CARD_STATUS_INACTIVE to activate PHYSICAL card for user UID1

    Then I wait for 40 seconds

    Then I activate the PHYSICAL card for the user UID1 with valid token, with status 200

    Then I check card status is CARD_STATUS_ACTIVE for user UID1 for PHYSICAL card

    Then I initiate the initial user authorisation to UPDATE_CARD_STATUS for user UID1 and expect a status of USER_AUTHORISATION_SUCCESS

    Then I initiate the final user authorisation to UPDATE_CARD_STATUS and expect a user authorisation status as USER_AUTHORISATION_INITIATED for user UID1

    And I initiate the PASSCODE journey within the PASSCODE_STEP for user UID1 to authorise the user and expect a status JOURNEY_INITIATED

    Then I process the PASSCODE journey within the PASSCODE_STEP for user UID1 to authorise the user and expect a status JOURNEY_PROCESSED

    And I submit the PASSCODE journey within the PASSCODE_STEP for user UID1 to authorise the user and expect a status JOURNEY_SUCCESSFUL

    Then I submit the final user authorisation for UPDATE_CARD_STATUS of user UID1 and expect a status USER_AUTHORISATION_SUBMITTED

    And I get the final user authorisation token for UPDATE_CARD_STATUS of user UID1 and expect a status USER_AUTHORISATION_SUCCESS

    Then I update the card status of the PHYSICAL card to BLOCK for user UID1 and expect a status code of 200

    Then I check card status is CARD_STATUS_BLOCKED for user UID1 for PHYSICAL card

    Then I initiate the initial user authorisation to UPDATE_CARD_STATUS for user UID1 and expect a status of USER_AUTHORISATION_SUCCESS

    Then I initiate the final user authorisation to UPDATE_CARD_STATUS and expect a user authorisation status as USER_AUTHORISATION_INITIATED for user UID1

    And I initiate the PASSCODE journey within the PASSCODE_STEP for user UID1 to authorise the user and expect a status JOURNEY_INITIATED

    Then I process the PASSCODE journey within the PASSCODE_STEP for user UID1 to authorise the user and expect a status JOURNEY_PROCESSED

    And I submit the PASSCODE journey within the PASSCODE_STEP for user UID1 to authorise the user and expect a status JOURNEY_SUCCESSFUL

    Then I submit the final user authorisation for UPDATE_CARD_STATUS of user UID1 and expect a status USER_AUTHORISATION_SUBMITTED

    And I get the final user authorisation token for UPDATE_CARD_STATUS of user UID1 and expect a status USER_AUTHORISATION_SUCCESS

    Then I update the card status of the PHYSICAL card to UNBLOCK for user UID1 and expect a status code of 200

    Then I check card status is CARD_STATUS_ACTIVE for user UID1 for PHYSICAL card

    Then I initiate the initial user authorisation to UPDATE_CARD_STATUS for user UID1 and expect a status of USER_AUTHORISATION_SUCCESS

    Then I initiate the final user authorisation to UPDATE_CARD_STATUS and expect a user authorisation status as USER_AUTHORISATION_INITIATED for user UID1

    And I initiate the PASSCODE journey within the PASSCODE_STEP for user UID1 to authorise the user and expect a status JOURNEY_INITIATED

    Then I process the PASSCODE journey within the PASSCODE_STEP for user UID1 to authorise the user and expect a status JOURNEY_PROCESSED

    And I submit the PASSCODE journey within the PASSCODE_STEP for user UID1 to authorise the user and expect a status JOURNEY_SUCCESSFUL

    Then I submit the final user authorisation for UPDATE_CARD_STATUS of user UID1 and expect a status USER_AUTHORISATION_SUBMITTED

    And I get the final user authorisation token for UPDATE_CARD_STATUS of user UID1 and expect a status USER_AUTHORISATION_SUCCESS

    Then I update the card status of the PHYSICAL card to DISABLE for user UID1 and expect a status code of 200

    Then I check card status is CARD_STATUS_DISABLED for user UID1 for PHYSICAL card

  Scenario: Physical PAYPAK Card transactions with default limits and updated limits for all channels

    Then I initiate the initial user authorisation to ORDER_CARD for user UID1 and expect a status of USER_AUTHORISATION_SUCCESS

    Then I initiate the final user authorisation to ORDER_CARD and expect a user authorisation status as USER_AUTHORISATION_INITIATED for user UID1

    And I initiate the PASSCODE journey within the PASSCODE_STEP for user UID1 to authorise the user and expect a status JOURNEY_INITIATED

    Then I process the PASSCODE journey within the PASSCODE_STEP for user UID1 to authorise the user and expect a status JOURNEY_PROCESSED

    And I submit the PASSCODE journey within the PASSCODE_STEP for user UID1 to authorise the user and expect a status JOURNEY_SUCCESSFUL

    Then I submit the final user authorisation for ORDER_CARD of user UID1 and expect a status USER_AUTHORISATION_SUBMITTED

    And I get the final user authorisation token for ORDER_CARD of user UID1 and expect a status USER_AUTHORISATION_SUCCESS

    Then I get the user cash wallets for the user UID1 and expect the account status of CASH_ACCOUNT_STATUS_CREATED

    Then I order a physical card for UID1 with card name as random_valid_choice and expect a status code of 200 and expect a card status of CARD_STATUS_PENDING

    Then I initiate the initial user authorisation to ACTIVATE_CARD for user UID1 and expect a status of USER_AUTHORISATION_SUCCESS

    Then I initiate the final user authorisation to ACTIVATE_CARD and expect a user authorisation status as USER_AUTHORISATION_INITIATED for user UID1

    And I initiate the PASSCODE journey within the PASSCODE_STEP for user UID1 to authorise the user and expect a status JOURNEY_INITIATED

    Then I process the PASSCODE journey within the PASSCODE_STEP for user UID1 to authorise the user and expect a status JOURNEY_PROCESSED

    And I submit the PASSCODE journey within the PASSCODE_STEP for user UID1 to authorise the user and expect a status JOURNEY_SUCCESSFUL

    Then I submit the final user authorisation for ACTIVATE_CARD of user UID1 and expect a status USER_AUTHORISATION_SUBMITTED

    And I get the final user authorisation token for ACTIVATE_CARD of user UID1 and expect a status USER_AUTHORISATION_SUCCESS

    Then I wait for card status as CARD_STATUS_INACTIVE to activate PHYSICAL card for user UID1

    Then I wait for 40 seconds

    Then I activate the PHYSICAL card for the user UID1 with valid token, with status 200

    Then I check card status is CARD_STATUS_ACTIVE for user UID1 for PHYSICAL card

    Then I deposit 100500 PKR into wallet with product code CASH_WALLET_CURRENT for user UID1 and expect a status code of 200

    And I check the balance of the wallet with product code CASH_WALLET_CURRENT for user UID1 and the balance should be 100500 PKR exact

    Given I create below transaction for PHYSICAL card for user profile id and expect a status code of 200
      | user_profile_identifier | transaction_permutation_name | billing_amount | is_foreign_txn | channel    |
      | UID1                    | AUTH_CLEAR                       | 100500         | false          | E_COMMERCE |

    And I check the balance of the wallet with product code CASH_WALLET_CURRENT for user UID1 and the balance should be 100500 PKR exact

    Then I initiate the initial user authorisation to UPDATE_CARD_LIMITS for user UID1 and expect a status of USER_AUTHORISATION_SUCCESS

    Then I initiate the final user authorisation to UPDATE_CARD_LIMITS and expect a user authorisation status as USER_AUTHORISATION_INITIATED for user UID1

    And I initiate the PASSCODE journey within the PASSCODE_STEP for user UID1 to authorise the user and expect a status JOURNEY_INITIATED

    Then I process the PASSCODE journey within the PASSCODE_STEP for user UID1 to authorise the user and expect a status JOURNEY_PROCESSED

    And I submit the PASSCODE journey within the PASSCODE_STEP for user UID1 to authorise the user and expect a status JOURNEY_SUCCESSFUL

    Then I submit the final user authorisation for UPDATE_CARD_LIMITS of user UID1 and expect a status USER_AUTHORISATION_SUBMITTED

    And I get the final user authorisation token for UPDATE_CARD_LIMITS of user UID1 and expect a status USER_AUTHORISATION_SUCCESS

    And I update the Paypak Physical Card limit of channel E_COMMERCE to 50000 PKR for user UID1 and expect a status code of 200

    Then I check if the Paypak Physical Card limit for the E_COMMERCE channel is set to 50000 PKR for user UID1

    Given I create below transaction for PHYSICAL card for user profile id and expect a status code of 200
      | user_profile_identifier | transaction_permutation_name | billing_amount | is_foreign_txn | channel    |
      | UID1                    | AUTH_CLEAR                       | 50500          | false          | E_COMMERCE |

    And I check the balance of the wallet with product code CASH_WALLET_CURRENT for user UID1 and the balance should be 100500 PKR exact

    Given I create below transaction for PHYSICAL card for user profile id and expect a status code of 200
      | user_profile_identifier | transaction_permutation_name | billing_amount | is_foreign_txn | channel    |
      | UID1                    | AUTH_CLEAR                       | 50000          | false          | E_COMMERCE |

    And I check the balance of the wallet with product code CASH_WALLET_CURRENT for user UID1 and the balance should be 50500 PKR exact

    Then I initiate the initial user authorisation to UPDATE_CARD_LIMITS for user UID1 and expect a status of USER_AUTHORISATION_SUCCESS

    Then I initiate the final user authorisation to UPDATE_CARD_LIMITS and expect a user authorisation status as USER_AUTHORISATION_INITIATED for user UID1

    And I initiate the PASSCODE journey within the PASSCODE_STEP for user UID1 to authorise the user and expect a status JOURNEY_INITIATED

    Then I process the PASSCODE journey within the PASSCODE_STEP for user UID1 to authorise the user and expect a status JOURNEY_PROCESSED

    And I submit the PASSCODE journey within the PASSCODE_STEP for user UID1 to authorise the user and expect a status JOURNEY_SUCCESSFUL

    Then I submit the final user authorisation for UPDATE_CARD_LIMITS of user UID1 and expect a status USER_AUTHORISATION_SUBMITTED

    And I get the final user authorisation token for UPDATE_CARD_LIMITS of user UID1 and expect a status USER_AUTHORISATION_SUCCESS

    And I update the Paypak Physical Card limit of channel E_COMMERCE to 80000 PKR for user UID1 and expect a status code of 200

    Then I check if the Paypak Physical Card limit for the E_COMMERCE channel is set to 80000 PKR for user UID1

    Given I create below transaction for PHYSICAL card for user profile id and expect a status code of 200
      | user_profile_identifier | transaction_permutation_name | billing_amount | is_foreign_txn | channel    |
      | UID1                    | AUTH_CLEAR                       | 30000          | false          | E_COMMERCE |

    And I check the balance of the wallet with product code CASH_WALLET_CURRENT for user UID1 and the balance should be 20500 PKR exact

    Then I deposit 30000 PKR into wallet with product code CASH_WALLET_CURRENT for user UID1 and expect a status code of 200

    And I check the balance of the wallet with product code CASH_WALLET_CURRENT for user UID1 and the balance should be 50500 PKR exact

    Given I create below transaction for PHYSICAL card for user profile id and expect a status code of 200
      | user_profile_identifier | transaction_permutation_name | billing_amount | is_foreign_txn | channel    |
      | UID1                    | AUTH_CLEAR                   | 50500              | false          | E_COMMERCE |

    And I check the balance of the wallet with product code CASH_WALLET_CURRENT for user UID1 and the balance should be 50500 PKR exact

    Then I initiate the initial user authorisation to UPDATE_CARD_LIMITS for user UID1 and expect a status of USER_AUTHORISATION_SUCCESS

    Then I initiate the final user authorisation to UPDATE_CARD_LIMITS and expect a user authorisation status as USER_AUTHORISATION_INITIATED for user UID1

    And I initiate the PASSCODE journey within the PASSCODE_STEP for user UID1 to authorise the user and expect a status JOURNEY_INITIATED

    Then I process the PASSCODE journey within the PASSCODE_STEP for user UID1 to authorise the user and expect a status JOURNEY_PROCESSED

    And I submit the PASSCODE journey within the PASSCODE_STEP for user UID1 to authorise the user and expect a status JOURNEY_SUCCESSFUL

    Then I submit the final user authorisation for UPDATE_CARD_LIMITS of user UID1 and expect a status USER_AUTHORISATION_SUBMITTED

    And I get the final user authorisation token for UPDATE_CARD_LIMITS of user UID1 and expect a status USER_AUTHORISATION_SUCCESS

    And I update the Paypak Physical Card limit of channel ATM to 30000 PKR for user UID1 and expect a status code of 200

    Then I check if the Paypak Physical Card limit for the ATM channel is set to 30000 PKR for user UID1

    Given I create below transaction for PHYSICAL card for user profile id and expect a status code of 200
      | user_profile_identifier | transaction_permutation_name | billing_amount | is_foreign_txn | channel |
      | UID1                    | AUTH_CLEAR                       | 30500          | false          | ATM     |

    And I check the balance of the wallet with product code CASH_WALLET_CURRENT for user UID1 and the balance should be 50500 PKR exact

    Given I create below transaction for PHYSICAL card for user profile id and expect a status code of 200
      | user_profile_identifier | transaction_permutation_name | billing_amount | is_foreign_txn | channel |
      | UID1                    | AUTH_CLEAR                       | 30000          | false          | ATM     |

    And I check the balance of the wallet with product code CASH_WALLET_CURRENT for user UID1 and the balance should be 20500 PKR exact

    Then I initiate the initial user authorisation to UPDATE_CARD_LIMITS for user UID1 and expect a status of USER_AUTHORISATION_SUCCESS

    Then I initiate the final user authorisation to UPDATE_CARD_LIMITS and expect a user authorisation status as USER_AUTHORISATION_INITIATED for user UID1

    And I initiate the PASSCODE journey within the PASSCODE_STEP for user UID1 to authorise the user and expect a status JOURNEY_INITIATED

    Then I process the PASSCODE journey within the PASSCODE_STEP for user UID1 to authorise the user and expect a status JOURNEY_PROCESSED

    And I submit the PASSCODE journey within the PASSCODE_STEP for user UID1 to authorise the user and expect a status JOURNEY_SUCCESSFUL

    Then I submit the final user authorisation for UPDATE_CARD_LIMITS of user UID1 and expect a status USER_AUTHORISATION_SUBMITTED

    And I get the final user authorisation token for UPDATE_CARD_LIMITS of user UID1 and expect a status USER_AUTHORISATION_SUCCESS

    And I update the Paypak Physical Card limit of channel ATM to 40000 PKR for user UID1 and expect a status code of 200

    Then I check if the Paypak Physical Card limit for the ATM channel is set to 40000 PKR for user UID1

    Given I create below transaction for PHYSICAL card for user profile id and expect a status code of 200
      | user_profile_identifier | transaction_permutation_name | billing_amount | is_foreign_txn | channel |
      | UID1                    | AUTH_CLEAR                   | 10000          | false          | ATM       |

    And I check the balance of the wallet with product code CASH_WALLET_CURRENT for user UID1 and the balance should be 10500 PKR exact

    Then I deposit 90000 PKR into wallet with product code CASH_WALLET_CURRENT for user UID1 and expect a status code of 200

    And I check the balance of the wallet with product code CASH_WALLET_CURRENT for user UID1 and the balance should be 100500 PKR exact

    Given I create below transaction for PHYSICAL card for user profile id and expect a status code of 200
      | user_profile_identifier | transaction_permutation_name | billing_amount | is_foreign_txn | channel |
      | UID1                    | AUTH_CLEAR                   | 100500         | false          | POS       |

    And I check the balance of the wallet with product code CASH_WALLET_CURRENT for user UID1 and the balance should be 100500 PKR exact

    Then I initiate the initial user authorisation to UPDATE_CARD_LIMITS for user UID1 and expect a status of USER_AUTHORISATION_SUCCESS

    Then I initiate the final user authorisation to UPDATE_CARD_LIMITS and expect a user authorisation status as USER_AUTHORISATION_INITIATED for user UID1

    And I initiate the PASSCODE journey within the PASSCODE_STEP for user UID1 to authorise the user and expect a status JOURNEY_INITIATED

    Then I process the PASSCODE journey within the PASSCODE_STEP for user UID1 to authorise the user and expect a status JOURNEY_PROCESSED

    And I submit the PASSCODE journey within the PASSCODE_STEP for user UID1 to authorise the user and expect a status JOURNEY_SUCCESSFUL

    Then I submit the final user authorisation for UPDATE_CARD_LIMITS of user UID1 and expect a status USER_AUTHORISATION_SUBMITTED

    And I get the final user authorisation token for UPDATE_CARD_LIMITS of user UID1 and expect a status USER_AUTHORISATION_SUCCESS

    And I update the Paypak Physical Card limit of channel POS to 50000 PKR for user UID1 and expect a status code of 200

    Then I check if the Paypak Physical Card limit for the POS channel is set to 50000 PKR for user UID1

    Given I create below transaction for PHYSICAL card for user profile id and expect a status code of 200
      | user_profile_identifier | transaction_permutation_name | billing_amount | is_foreign_txn | channel |
      | UID1                    | AUTH_CLEAR                       | 50500          | false          | POS     |

    And I check the balance of the wallet with product code CASH_WALLET_CURRENT for user UID1 and the balance should be 100500 PKR exact

    Given I create below transaction for PHYSICAL card for user profile id and expect a status code of 200
      | user_profile_identifier | transaction_permutation_name | billing_amount | is_foreign_txn | channel |
      | UID1                    | AUTH_CLEAR                   | 50000          | false          | POS       |

    And I check the balance of the wallet with product code CASH_WALLET_CURRENT for user UID1 and the balance should be 50500 PKR exact

    Then I initiate the initial user authorisation to UPDATE_CARD_LIMITS for user UID1 and expect a status of USER_AUTHORISATION_SUCCESS

    Then I initiate the final user authorisation to UPDATE_CARD_LIMITS and expect a user authorisation status as USER_AUTHORISATION_INITIATED for user UID1

    And I initiate the PASSCODE journey within the PASSCODE_STEP for user UID1 to authorise the user and expect a status JOURNEY_INITIATED

    Then I process the PASSCODE journey within the PASSCODE_STEP for user UID1 to authorise the user and expect a status JOURNEY_PROCESSED

    And I submit the PASSCODE journey within the PASSCODE_STEP for user UID1 to authorise the user and expect a status JOURNEY_SUCCESSFUL

    Then I submit the final user authorisation for UPDATE_CARD_LIMITS of user UID1 and expect a status USER_AUTHORISATION_SUBMITTED

    And I get the final user authorisation token for UPDATE_CARD_LIMITS of user UID1 and expect a status USER_AUTHORISATION_SUCCESS

    And I update the Paypak Physical Card limit of channel POS to 80000 PKR for user UID1 and expect a status code of 200

    Then I check if the Paypak Physical Card limit for the POS channel is set to 80000 PKR for user UID1

    Given I create below transaction for PHYSICAL card for user profile id and expect a status code of 200
      | user_profile_identifier | transaction_permutation_name | billing_amount | is_foreign_txn | channel |
      | UID1                    | AUTH_CLEAR                       | 30000          | false          | POS     |

    And I check the balance of the wallet with product code CASH_WALLET_CURRENT for user UID1 and the balance should be 20500 PKR exact

  Scenario: Visa Physical Card transactions with default limits and updated limits for all channels

    Then I initiate the initial user authorisation to ORDER_CARD for user UID1 and expect a status of USER_AUTHORISATION_SUCCESS

    Then I initiate the final user authorisation to ORDER_CARD and expect a user authorisation status as USER_AUTHORISATION_INITIATED for user UID1

    And I initiate the PASSCODE journey within the PASSCODE_STEP for user UID1 to authorise the user and expect a status JOURNEY_INITIATED

    Then I process the PASSCODE journey within the PASSCODE_STEP for user UID1 to authorise the user and expect a status JOURNEY_PROCESSED

    And I submit the PASSCODE journey within the PASSCODE_STEP for user UID1 to authorise the user and expect a status JOURNEY_SUCCESSFUL

    Then I submit the final user authorisation for ORDER_CARD of user UID1 and expect a status USER_AUTHORISATION_SUBMITTED

    And I get the final user authorisation token for ORDER_CARD of user UID1 and expect a status USER_AUTHORISATION_SUCCESS

    Then I get the user cash wallets for the user UID1 and expect the account status of CASH_ACCOUNT_STATUS_CREATED

    Then I order a physical visa card for UID1 with card name as random_valid_choice and expect a status code of 200 and expect a card status of CARD_STATUS_PENDING

    Then I initiate the initial user authorisation to ACTIVATE_CARD for user UID1 and expect a status of USER_AUTHORISATION_SUCCESS

    Then I initiate the final user authorisation to ACTIVATE_CARD and expect a user authorisation status as USER_AUTHORISATION_INITIATED for user UID1

    And I initiate the PASSCODE journey within the PASSCODE_STEP for user UID1 to authorise the user and expect a status JOURNEY_INITIATED

    Then I process the PASSCODE journey within the PASSCODE_STEP for user UID1 to authorise the user and expect a status JOURNEY_PROCESSED

    And I submit the PASSCODE journey within the PASSCODE_STEP for user UID1 to authorise the user and expect a status JOURNEY_SUCCESSFUL

    Then I submit the final user authorisation for ACTIVATE_CARD of user UID1 and expect a status USER_AUTHORISATION_SUBMITTED

    And I get the final user authorisation token for ACTIVATE_CARD of user UID1 and expect a status USER_AUTHORISATION_SUCCESS

    Then I wait for card status as CARD_STATUS_UPGRADED to activate PHYSICAL card for user UID1

    Then I wait for 40 seconds

    Then I activate the PHYSICAL card for the user UID1 with valid token, with status 200

    Then I check card status is CARD_STATUS_ACTIVE for user UID1 for PHYSICAL card

    Then I deposit 200500 PKR into wallet with product code CASH_WALLET_CURRENT for user UID1 and expect a status code of 200

    And I check the balance of the wallet with product code CASH_WALLET_CURRENT for user UID1 and the balance should be 200500 PKR exact

    Given I create below transaction for PHYSICAL card for user profile id and expect a status code of 200
      | user_profile_identifier | transaction_permutation_name | billing_amount | is_foreign_txn | channel    |
      | UID1                    | AUTH_CLEAR                   | 200500         | false          | E_COMMERCE |

    And I check the balance of the wallet with product code CASH_WALLET_CURRENT for user UID1 and the balance should be 200500 PKR exact

    Then I initiate the initial user authorisation to UPDATE_CARD_LIMITS for user UID1 and expect a status of USER_AUTHORISATION_SUCCESS

    Then I initiate the final user authorisation to UPDATE_CARD_LIMITS and expect a user authorisation status as USER_AUTHORISATION_INITIATED for user UID1

    And I initiate the PASSCODE journey within the PASSCODE_STEP for user UID1 to authorise the user and expect a status JOURNEY_INITIATED

    Then I process the PASSCODE journey within the PASSCODE_STEP for user UID1 to authorise the user and expect a status JOURNEY_PROCESSED

    And I submit the PASSCODE journey within the PASSCODE_STEP for user UID1 to authorise the user and expect a status JOURNEY_SUCCESSFUL

    Then I submit the final user authorisation for UPDATE_CARD_LIMITS of user UID1 and expect a status USER_AUTHORISATION_SUBMITTED

    And I get the final user authorisation token for UPDATE_CARD_LIMITS of user UID1 and expect a status USER_AUTHORISATION_SUCCESS

    And I update the Visa Physical Card limit of channel E_COMMERCE to 100000 PKR for user UID1 and expect a status code of 200

    Then I check if the Visa Physical Card limit for the E_COMMERCE channel is set to 100000 PKR for user UID1

    Given I create below transaction for PHYSICAL card for user profile id and expect a status code of 200
      | user_profile_identifier | transaction_permutation_name | billing_amount | is_foreign_txn | channel    |
      | UID1                    | AUTH_CLEAR                   | 100500         | false          | E_COMMERCE |

    And I check the balance of the wallet with product code CASH_WALLET_CURRENT for user UID1 and the balance should be 200500 PKR exact

    Given I create below transaction for PHYSICAL card for user profile id and expect a status code of 200
      | user_profile_identifier | transaction_permutation_name | billing_amount | is_foreign_txn | channel    |
      | UID1                    | AUTH_CLEAR                   | 100000         | false          | E_COMMERCE |

    And I check the balance of the wallet with product code CASH_WALLET_CURRENT for user UID1 and the balance should be 100500 PKR exact

    Then I initiate the initial user authorisation to UPDATE_CARD_LIMITS for user UID1 and expect a status of USER_AUTHORISATION_SUCCESS

    Then I initiate the final user authorisation to UPDATE_CARD_LIMITS and expect a user authorisation status as USER_AUTHORISATION_INITIATED for user UID1

    And I initiate the PASSCODE journey within the PASSCODE_STEP for user UID1 to authorise the user and expect a status JOURNEY_INITIATED

    Then I process the PASSCODE journey within the PASSCODE_STEP for user UID1 to authorise the user and expect a status JOURNEY_PROCESSED

    And I submit the PASSCODE journey within the PASSCODE_STEP for user UID1 to authorise the user and expect a status JOURNEY_SUCCESSFUL

    Then I submit the final user authorisation for UPDATE_CARD_LIMITS of user UID1 and expect a status USER_AUTHORISATION_SUBMITTED

    And I get the final user authorisation token for UPDATE_CARD_LIMITS of user UID1 and expect a status USER_AUTHORISATION_SUCCESS

    And I update the Visa Physical Card limit of channel E_COMMERCE to 150000 PKR for user UID1 and expect a status code of 200

    Then I check if the Visa Physical Card limit for the E_COMMERCE channel is set to 150000 PKR for user UID1

    Given I create below transaction for PHYSICAL card for user profile id and expect a status code of 200
      | user_profile_identifier | transaction_permutation_name | billing_amount | is_foreign_txn | channel    |
      | UID1                    | AUTH_CLEAR                   | 50000          | false          | E_COMMERCE |

    And I check the balance of the wallet with product code CASH_WALLET_CURRENT for user UID1 and the balance should be 50500 PKR exact

    Then I deposit 150000 PKR into wallet with product code CASH_WALLET_CURRENT for user UID1 and expect a status code of 200

    And I check the balance of the wallet with product code CASH_WALLET_CURRENT for user UID1 and the balance should be 200500 PKR exact

    Given I create below transaction for PHYSICAL card for user profile id and expect a status code of 200
      | user_profile_identifier | transaction_permutation_name | billing_amount | is_foreign_txn | channel |
      | UID1                    | AUTH_CLEAR                   | 100500          | false          | ATM     |

    And I check the balance of the wallet with product code CASH_WALLET_CURRENT for user UID1 and the balance should be 200500 PKR exact

    Then I initiate the initial user authorisation to UPDATE_CARD_LIMITS for user UID1 and expect a status of USER_AUTHORISATION_SUCCESS

    Then I initiate the final user authorisation to UPDATE_CARD_LIMITS and expect a user authorisation status as USER_AUTHORISATION_INITIATED for user UID1

    And I initiate the PASSCODE journey within the PASSCODE_STEP for user UID1 to authorise the user and expect a status JOURNEY_INITIATED

    Then I process the PASSCODE journey within the PASSCODE_STEP for user UID1 to authorise the user and expect a status JOURNEY_PROCESSED

    And I submit the PASSCODE journey within the PASSCODE_STEP for user UID1 to authorise the user and expect a status JOURNEY_SUCCESSFUL

    Then I submit the final user authorisation for UPDATE_CARD_LIMITS of user UID1 and expect a status USER_AUTHORISATION_SUBMITTED

    And I get the final user authorisation token for UPDATE_CARD_LIMITS of user UID1 and expect a status USER_AUTHORISATION_SUCCESS

    And I update the Visa Physical Card limit of channel ATM to 50000 PKR for user UID1 and expect a status code of 200

    Then I check if the Visa Physical Card limit for the ATM channel is set to 50000 PKR for user UID1

    Given I create below transaction for PHYSICAL card for user profile id and expect a status code of 200
      | user_profile_identifier | transaction_permutation_name | billing_amount | is_foreign_txn | channel |
      | UID1                    | AUTH_CLEAR                   | 50500          | false          | ATM     |

    And I check the balance of the wallet with product code CASH_WALLET_CURRENT for user UID1 and the balance should be 200500 PKR exact

    Given I create below transaction for PHYSICAL card for user profile id and expect a status code of 200
      | user_profile_identifier | transaction_permutation_name | billing_amount | is_foreign_txn | channel |
      | UID1                    | AUTH_CLEAR                   | 50000          | false          | ATM     |

    And I check the balance of the wallet with product code CASH_WALLET_CURRENT for user UID1 and the balance should be 150500 PKR exact

    Then I initiate the initial user authorisation to UPDATE_CARD_LIMITS for user UID1 and expect a status of USER_AUTHORISATION_SUCCESS

    Then I initiate the final user authorisation to UPDATE_CARD_LIMITS and expect a user authorisation status as USER_AUTHORISATION_INITIATED for user UID1

    And I initiate the PASSCODE journey within the PASSCODE_STEP for user UID1 to authorise the user and expect a status JOURNEY_INITIATED

    Then I process the PASSCODE journey within the PASSCODE_STEP for user UID1 to authorise the user and expect a status JOURNEY_PROCESSED

    And I submit the PASSCODE journey within the PASSCODE_STEP for user UID1 to authorise the user and expect a status JOURNEY_SUCCESSFUL

    Then I submit the final user authorisation for UPDATE_CARD_LIMITS of user UID1 and expect a status USER_AUTHORISATION_SUBMITTED

    And I get the final user authorisation token for UPDATE_CARD_LIMITS of user UID1 and expect a status USER_AUTHORISATION_SUCCESS

    And I update the Visa Physical Card limit of channel ATM to 80000 PKR for user UID1 and expect a status code of 200

    Then I check if the Visa Physical Card limit for the ATM channel is set to 80000 PKR for user UID1

    Given I create below transaction for PHYSICAL card for user profile id and expect a status code of 200
      | user_profile_identifier | transaction_permutation_name | billing_amount | is_foreign_txn | channel |
      | UID1                    | AUTH_CLEAR                   | 30000          | false          | ATM     |

    And I check the balance of the wallet with product code CASH_WALLET_CURRENT for user UID1 and the balance should be 120500 PKR exact

    Then I deposit 80000 PKR into wallet with product code CASH_WALLET_CURRENT for user UID1 and expect a status code of 200

    And I check the balance of the wallet with product code CASH_WALLET_CURRENT for user UID1 and the balance should be 200500 PKR exact

    Given I create below transaction for PHYSICAL card for user profile id and expect a status code of 200
      | user_profile_identifier | transaction_permutation_name | billing_amount | is_foreign_txn | channel |
      | UID1                    | AUTH_CLEAR                   | 200500         | false          | POS     |

    And I check the balance of the wallet with product code CASH_WALLET_CURRENT for user UID1 and the balance should be 200500 PKR exact

    Then I initiate the initial user authorisation to UPDATE_CARD_LIMITS for user UID1 and expect a status of USER_AUTHORISATION_SUCCESS

    Then I initiate the final user authorisation to UPDATE_CARD_LIMITS and expect a user authorisation status as USER_AUTHORISATION_INITIATED for user UID1

    And I initiate the PASSCODE journey within the PASSCODE_STEP for user UID1 to authorise the user and expect a status JOURNEY_INITIATED

    Then I process the PASSCODE journey within the PASSCODE_STEP for user UID1 to authorise the user and expect a status JOURNEY_PROCESSED

    And I submit the PASSCODE journey within the PASSCODE_STEP for user UID1 to authorise the user and expect a status JOURNEY_SUCCESSFUL

    Then I submit the final user authorisation for UPDATE_CARD_LIMITS of user UID1 and expect a status USER_AUTHORISATION_SUBMITTED

    And I get the final user authorisation token for UPDATE_CARD_LIMITS of user UID1 and expect a status USER_AUTHORISATION_SUCCESS

    And I update the Visa Physical Card limit of channel POS to 100000 PKR for user UID1 and expect a status code of 200

    Then I check if the Visa Physical Card limit for the POS channel is set to 100000 PKR for user UID1

    Given I create below transaction for PHYSICAL card for user profile id and expect a status code of 200
      | user_profile_identifier | transaction_permutation_name | billing_amount | is_foreign_txn | channel |
      | UID1                    | AUTH_CLEAR                   | 100500         | false          | POS     |

    And I check the balance of the wallet with product code CASH_WALLET_CURRENT for user UID1 and the balance should be 200500 PKR exact

    Given I create below transaction for PHYSICAL card for user profile id and expect a status code of 200
      | user_profile_identifier | transaction_permutation_name | billing_amount | is_foreign_txn | channel |
      | UID1                    | AUTH_CLEAR                   | 100000         | false          | POS     |

    And I check the balance of the wallet with product code CASH_WALLET_CURRENT for user UID1 and the balance should be 100500 PKR exact

    Then I initiate the initial user authorisation to UPDATE_CARD_LIMITS for user UID1 and expect a status of USER_AUTHORISATION_SUCCESS

    Then I initiate the final user authorisation to UPDATE_CARD_LIMITS and expect a user authorisation status as USER_AUTHORISATION_INITIATED for user UID1

    And I initiate the PASSCODE journey within the PASSCODE_STEP for user UID1 to authorise the user and expect a status JOURNEY_INITIATED

    Then I process the PASSCODE journey within the PASSCODE_STEP for user UID1 to authorise the user and expect a status JOURNEY_PROCESSED

    And I submit the PASSCODE journey within the PASSCODE_STEP for user UID1 to authorise the user and expect a status JOURNEY_SUCCESSFUL

    Then I submit the final user authorisation for UPDATE_CARD_LIMITS of user UID1 and expect a status USER_AUTHORISATION_SUBMITTED

    And I get the final user authorisation token for UPDATE_CARD_LIMITS of user UID1 and expect a status USER_AUTHORISATION_SUCCESS

    And I update the Visa Physical Card limit of channel POS to 150000 PKR for user UID1 and expect a status code of 200

    Then I check if the Visa Physical Card limit for the POS channel is set to 150000 PKR for user UID1

    Given I create below transaction for PHYSICAL card for user profile id and expect a status code of 200
      | user_profile_identifier | transaction_permutation_name | billing_amount | is_foreign_txn | channel |
      | UID1                    | AUTH_CLEAR                   | 50000          | false          | POS     |

    And I check the balance of the wallet with product code CASH_WALLET_CURRENT for user UID1 and the balance should be 50500 PKR exact

  Scenario: Blocking channels in physical PAYPAK card

    Then I initiate the initial user authorisation to ORDER_CARD for user UID1 and expect a status of USER_AUTHORISATION_SUCCESS

    Then I initiate the final user authorisation to ORDER_CARD and expect a user authorisation status as USER_AUTHORISATION_INITIATED for user UID1

    And I initiate the PASSCODE journey within the PASSCODE_STEP for user UID1 to authorise the user and expect a status JOURNEY_INITIATED

    Then I process the PASSCODE journey within the PASSCODE_STEP for user UID1 to authorise the user and expect a status JOURNEY_PROCESSED

    And I submit the PASSCODE journey within the PASSCODE_STEP for user UID1 to authorise the user and expect a status JOURNEY_SUCCESSFUL

    Then I submit the final user authorisation for ORDER_CARD of user UID1 and expect a status USER_AUTHORISATION_SUBMITTED

    And I get the final user authorisation token for ORDER_CARD of user UID1 and expect a status USER_AUTHORISATION_SUCCESS

    Then I get the user cash wallets for the user UID1 and expect the account status of CASH_ACCOUNT_STATUS_CREATED

    Then I order a physical card for UID1 with card name as random_valid_choice and expect a status code of 200 and expect a card status of CARD_STATUS_PENDING

    Then I initiate the initial user authorisation to ACTIVATE_CARD for user UID1 and expect a status of USER_AUTHORISATION_SUCCESS

    Then I initiate the final user authorisation to ACTIVATE_CARD and expect a user authorisation status as USER_AUTHORISATION_INITIATED for user UID1

    And I initiate the PASSCODE journey within the PASSCODE_STEP for user UID1 to authorise the user and expect a status JOURNEY_INITIATED

    Then I process the PASSCODE journey within the PASSCODE_STEP for user UID1 to authorise the user and expect a status JOURNEY_PROCESSED

    And I submit the PASSCODE journey within the PASSCODE_STEP for user UID1 to authorise the user and expect a status JOURNEY_SUCCESSFUL

    Then I submit the final user authorisation for ACTIVATE_CARD of user UID1 and expect a status USER_AUTHORISATION_SUBMITTED

    And I get the final user authorisation token for ACTIVATE_CARD of user UID1 and expect a status USER_AUTHORISATION_SUCCESS

    Then I wait for card status as CARD_STATUS_INACTIVE to activate PHYSICAL card for user UID1

    Then I wait for 40 seconds

    Then I activate the PHYSICAL card for the user UID1 with valid token, with status 200

    Then I check card status is CARD_STATUS_ACTIVE for user UID1 for PHYSICAL card

    Then I deposit 10000 PKR into wallet with product code CASH_WALLET_CURRENT for user UID1 and expect a status code of 200

    And I check the balance of the wallet with product code CASH_WALLET_CURRENT for user UID1 and the balance should be 10000 PKR exact

    Then I initiate the initial user authorisation to UPDATE_CARD_SETTINGS for user UID1 and expect a status of USER_AUTHORISATION_SUCCESS

    Then I initiate the final user authorisation to UPDATE_CARD_SETTINGS and expect a user authorisation status as USER_AUTHORISATION_INITIATED for user UID1

    And I initiate the PASSCODE journey within the PASSCODE_STEP for user UID1 to authorise the user and expect a status JOURNEY_INITIATED

    Then I process the PASSCODE journey within the PASSCODE_STEP for user UID1 to authorise the user and expect a status JOURNEY_PROCESSED

    And I submit the PASSCODE journey within the PASSCODE_STEP for user UID1 to authorise the user and expect a status JOURNEY_SUCCESSFUL

    Then I submit the final user authorisation for UPDATE_CARD_SETTINGS of user UID1 and expect a status USER_AUTHORISATION_SUBMITTED

    And I get the final user authorisation token for UPDATE_CARD_SETTINGS of user UID1 and expect a status USER_AUTHORISATION_SUCCESS

    Then I block the Paypak Physical Card channel E_COMMERCE for user UID1

    And I check the status of Paypak Physical Card channel E_COMMERCE to be DISABLED for user UID1

    Given I create below transaction for PHYSICAL card for user profile id and expect a status code of 200
      | user_profile_identifier | transaction_permutation_name | billing_amount | is_foreign_txn | channel    |
      | UID1                    | AUTH_CLEAR                   | 10000          | false          | E_COMMERCE |

    And I check the balance of the wallet with product code CASH_WALLET_CURRENT for user UID1 and the balance should be 10000 PKR exact

    Then I unblock the Paypak Physical Card channel E_COMMERCE for user UID1

    And I check the status of Paypak Physical Card channel E_COMMERCE to be ENABLED for user UID1

    Given I create below transaction for PHYSICAL card for user profile id and expect a status code of 200
      | user_profile_identifier | transaction_permutation_name | billing_amount | is_foreign_txn | channel    |
      | UID1                    | AUTH_CLEAR                   | 10000          | false          | E_COMMERCE |

    And I check the balance of the wallet with product code CASH_WALLET_CURRENT for user UID1 and the balance should be 0 PKR exact


  Scenario: Card negative balance claim

    Then I initiate the initial user authorisation to ORDER_CARD for user UID1 and expect a status of USER_AUTHORISATION_SUCCESS

    Then I initiate the final user authorisation to ORDER_CARD and expect a user authorisation status as USER_AUTHORISATION_INITIATED for user UID1

    And I initiate the PASSCODE journey within the PASSCODE_STEP for user UID1 to authorise the user and expect a status JOURNEY_INITIATED

    Then I process the PASSCODE journey within the PASSCODE_STEP for user UID1 to authorise the user and expect a status JOURNEY_PROCESSED

    And I submit the PASSCODE journey within the PASSCODE_STEP for user UID1 to authorise the user and expect a status JOURNEY_SUCCESSFUL

    Then I submit the final user authorisation for ORDER_CARD of user UID1 and expect a status USER_AUTHORISATION_SUBMITTED

    And I get the final user authorisation token for ORDER_CARD of user UID1 and expect a status USER_AUTHORISATION_SUCCESS

    Then I get the user cash wallets for the user UID1 and expect the account status of CASH_ACCOUNT_STATUS_CREATED

    Then I order a physical card for UID1 with card name as random_valid_choice and expect a status code of 200 and expect a card status of CARD_STATUS_PENDING

    Then I initiate the initial user authorisation to ACTIVATE_CARD for user UID1 and expect a status of USER_AUTHORISATION_SUCCESS

    Then I initiate the final user authorisation to ACTIVATE_CARD and expect a user authorisation status as USER_AUTHORISATION_INITIATED for user UID1

    And I initiate the PASSCODE journey within the PASSCODE_STEP for user UID1 to authorise the user and expect a status JOURNEY_INITIATED

    Then I process the PASSCODE journey within the PASSCODE_STEP for user UID1 to authorise the user and expect a status JOURNEY_PROCESSED

    And I submit the PASSCODE journey within the PASSCODE_STEP for user UID1 to authorise the user and expect a status JOURNEY_SUCCESSFUL

    Then I submit the final user authorisation for ACTIVATE_CARD of user UID1 and expect a status USER_AUTHORISATION_SUBMITTED

    And I get the final user authorisation token for ACTIVATE_CARD of user UID1 and expect a status USER_AUTHORISATION_SUCCESS

    Then I wait for card status as CARD_STATUS_INACTIVE to activate PHYSICAL card for user UID1

    Then I wait for 40 seconds

    Then I activate the PHYSICAL card for the user UID1 with valid token, with status 200

    Then I check card status is CARD_STATUS_ACTIVE for user UID1 for PHYSICAL card

    Then I deposit 50 PKR into wallet with product code CASH_WALLET_CURRENT for user UID1 and expect a status code of 200

    Given I create below transaction for PHYSICAL card for user profile id and expect a status code of 200
      | user_profile_identifier | transaction_permutation_name | billing_amount | is_foreign_txn | channel    |
      | UID1                    | CLEAR                        | 60             | false          | E_COMMERCE |

    And I check the balance of the wallet with product code CASH_WALLET_CURRENT for user UID1 and the balance should be -10 PKR exact

    Then I deposit 200 PKR into wallet with product code CASH_WALLET_CURRENT for user UID1 and expect a status code of 200

    And I check the balance of the wallet with product code CASH_WALLET_CURRENT for user UID1 and the balance should be 190 PKR exact

  Scenario: Local Transactions - AUTH Cases - Roundups DISABLED - PHYSICAL VISA CARD

    Then I initiate the initial user authorisation to ORDER_CARD for user UID1 and expect a status of USER_AUTHORISATION_SUCCESS

    Then I initiate the final user authorisation to ORDER_CARD and expect a user authorisation status as USER_AUTHORISATION_INITIATED for user UID1

    And I initiate the PASSCODE journey within the PASSCODE_STEP for user UID1 to authorise the user and expect a status JOURNEY_INITIATED

    Then I process the PASSCODE journey within the PASSCODE_STEP for user UID1 to authorise the user and expect a status JOURNEY_PROCESSED

    And I submit the PASSCODE journey within the PASSCODE_STEP for user UID1 to authorise the user and expect a status JOURNEY_SUCCESSFUL

    Then I submit the final user authorisation for ORDER_CARD of user UID1 and expect a status USER_AUTHORISATION_SUBMITTED

    And I get the final user authorisation token for ORDER_CARD of user UID1 and expect a status USER_AUTHORISATION_SUCCESS

    Then I get the user cash wallets for the user UID1 and expect the account status of CASH_ACCOUNT_STATUS_CREATED

    Then I order a physical card for UID1 with card name as random_valid_choice and expect a status code of 200 and expect a card status of CARD_STATUS_PENDING

    Then I initiate the initial user authorisation to ACTIVATE_CARD for user UID1 and expect a status of USER_AUTHORISATION_SUCCESS

    Then I initiate the final user authorisation to ACTIVATE_CARD and expect a user authorisation status as USER_AUTHORISATION_INITIATED for user UID1

    And I initiate the PASSCODE journey within the PASSCODE_STEP for user UID1 to authorise the user and expect a status JOURNEY_INITIATED

    Then I process the PASSCODE journey within the PASSCODE_STEP for user UID1 to authorise the user and expect a status JOURNEY_PROCESSED

    And I submit the PASSCODE journey within the PASSCODE_STEP for user UID1 to authorise the user and expect a status JOURNEY_SUCCESSFUL

    Then I submit the final user authorisation for ACTIVATE_CARD of user UID1 and expect a status USER_AUTHORISATION_SUBMITTED

    And I get the final user authorisation token for ACTIVATE_CARD of user UID1 and expect a status USER_AUTHORISATION_SUCCESS

    Then I wait for card status as CARD_STATUS_INACTIVE to activate PHYSICAL card for user UID1

    Then I wait for 40 seconds

    Then I activate the PHYSICAL card for the user UID1 with valid token, with status 200

    Then I check card status is CARD_STATUS_ACTIVE for user UID1 for PHYSICAL card

    And I DISABLE roundups for user UID1

    Then I deposit 50 PKR into wallet with product code CASH_WALLET_CURRENT for user UID1 and expect a status code of 200

    And I check the balance of the wallet with product code CASH_WALLET_CURRENT for user UID1 and the balance should be 50 PKR exact

#    1. auth
    Given I create below transaction for PHYSICAL card for user profile id and expect a status code of 200
      | user_profile_identifier | transaction_permutation_name | billing_amount | is_foreign_txn | channel    |
      | UID1                    | AUTH                         | 10.3           | false          | E_COMMERCE |

    And I check the balance of the wallet with product code CASH_WALLET_CURRENT for user UID1 and the balance should be 39 PKR approx

# 2. AUTH_CLEAR
    Given I create below transaction for PHYSICAL card for user profile id and expect a status code of 200
      | user_profile_identifier | transaction_permutation_name | billing_amount | is_foreign_txn | channel    |
      | UID1                    | AUTH_CLEAR                   | 5.5            | false          | E_COMMERCE |

    And I check the balance of the wallet with product code CASH_WALLET_CURRENT for user UID1 and the balance should be 34 PKR approx

# 3. AUTH_PARTIAL_CLEARING
    Given I create below transaction for PHYSICAL card for user profile id and expect a status code of 200
      | user_profile_identifier | transaction_permutation_name | billing_amount | is_foreign_txn | channel    |
      | UID1                    | AUTH_PARTIAL_CLEARING        | 1.3            | false          | E_COMMERCE |

    And I check the balance of the wallet with product code CASH_WALLET_CURRENT for user UID1 and the balance should be 32 PKR approx

#4. AUTH_MULTI_CLEARING
    Given I create below transaction for PHYSICAL card for user profile id and expect a status code of 200
      | user_profile_identifier | transaction_permutation_name | billing_amount | is_foreign_txn | channel    |
      | UID1                    | AUTH_MULTI_CLEAR             | 12.47          | false          | E_COMMERCE |

    And I check the balance of the wallet with product code CASH_WALLET_CURRENT for user UID1 and the balance should be 20 PKR approx

# 5. AUTH_FR
    Given I create below transaction for PHYSICAL card for user profile id and expect a status code of 200
      | user_profile_identifier | transaction_permutation_name | billing_amount | is_foreign_txn | channel    |
      | UID1                    | AUTH_FR                      | 3.37           | false          | E_COMMERCE |

    And I check the balance of the wallet with product code CASH_WALLET_CURRENT for user UID1 and the balance should be 20 PKR approx

#    6. AUTH_PR
    Given I create below transaction for PHYSICAL card for user profile id and expect a status code of 200
      | user_profile_identifier | transaction_permutation_name | billing_amount | is_foreign_txn | channel    |
      | UID1                    | AUTH_PR                      | 1.94           | false          | E_COMMERCE |

    And I check the balance of the wallet with product code CASH_WALLET_CURRENT for user UID1 and the balance should be 20 PKR approx

#    7.AUTH_PR_FR ---- balance becomes [balance: 19.46]
    Given I create below transaction for PHYSICAL card for user profile id and expect a status code of 200
      | user_profile_identifier | transaction_permutation_name | billing_amount | is_foreign_txn | channel    |
      | UID1                    | AUTH_PR_FR                   | 3.33           | false          | E_COMMERCE |

    And I check the balance of the wallet with product code CASH_WALLET_CURRENT for user UID1 and the balance should be 20 PKR approx

#8. AUTH_PR_CLEAR
    Given I create below transaction for PHYSICAL card for user profile id and expect a status code of 200
      | user_profile_identifier | transaction_permutation_name | billing_amount | is_foreign_txn | channel    |
      | UID1                    | AUTH_PR_CLEAR                | 8.19           | false          | E_COMMERCE |

    And I check the balance of the wallet with product code CASH_WALLET_CURRENT for user UID1 and the balance should be 15 PKR approx

# 9. AUTH_PR_MULTI_CLEAR
    Given I create below transaction for PHYSICAL card for user profile id and expect a status code of 200
      | user_profile_identifier | transaction_permutation_name | billing_amount | is_foreign_txn | channel    |
      | UID1                    | AUTH_PR_MULTI_CLEAR          | 1.44           | false          | E_COMMERCE |

    And I check the balance of the wallet with product code CASH_WALLET_CURRENT for user UID1 and the balance should be 14 PKR approx

#    9.1
    Given I create below transaction for PHYSICAL card for user profile id and expect a status code of 200
      | user_profile_identifier | transaction_permutation_name | billing_amount | is_foreign_txn | channel    |
      | UID1                    | AUTH_PR_MULTI_CLEAR          | 6.99           | false          | E_COMMERCE |

    And I check the balance of the wallet with product code CASH_WALLET_CURRENT for user UID1 and the balance should be 10 PKR approx


  Scenario: Local Transactions - Incremental Auth - Roundups DISABLED for PHYSICAL VISA CARD

    Then I initiate the initial user authorisation to ORDER_CARD for user UID1 and expect a status of USER_AUTHORISATION_SUCCESS

    Then I initiate the final user authorisation to ORDER_CARD and expect a user authorisation status as USER_AUTHORISATION_INITIATED for user UID1

    And I initiate the PASSCODE journey within the PASSCODE_STEP for user UID1 to authorise the user and expect a status JOURNEY_INITIATED

    Then I process the PASSCODE journey within the PASSCODE_STEP for user UID1 to authorise the user and expect a status JOURNEY_PROCESSED

    And I submit the PASSCODE journey within the PASSCODE_STEP for user UID1 to authorise the user and expect a status JOURNEY_SUCCESSFUL

    Then I submit the final user authorisation for ORDER_CARD of user UID1 and expect a status USER_AUTHORISATION_SUBMITTED

    And I get the final user authorisation token for ORDER_CARD of user UID1 and expect a status USER_AUTHORISATION_SUCCESS

    Then I get the user cash wallets for the user UID1 and expect the account status of CASH_ACCOUNT_STATUS_CREATED

    Then I order a physical card for UID1 with card name as random_valid_choice and expect a status code of 200 and expect a card status of CARD_STATUS_PENDING

    Then I initiate the initial user authorisation to ACTIVATE_CARD for user UID1 and expect a status of USER_AUTHORISATION_SUCCESS

    Then I initiate the final user authorisation to ACTIVATE_CARD and expect a user authorisation status as USER_AUTHORISATION_INITIATED for user UID1

    And I initiate the PASSCODE journey within the PASSCODE_STEP for user UID1 to authorise the user and expect a status JOURNEY_INITIATED

    Then I process the PASSCODE journey within the PASSCODE_STEP for user UID1 to authorise the user and expect a status JOURNEY_PROCESSED

    And I submit the PASSCODE journey within the PASSCODE_STEP for user UID1 to authorise the user and expect a status JOURNEY_SUCCESSFUL

    Then I submit the final user authorisation for ACTIVATE_CARD of user UID1 and expect a status USER_AUTHORISATION_SUBMITTED

    And I get the final user authorisation token for ACTIVATE_CARD of user UID1 and expect a status USER_AUTHORISATION_SUCCESS

    Then I wait for card status as CARD_STATUS_INACTIVE to activate PHYSICAL card for user UID1

    Then I wait for 40 seconds

    Then I activate the PHYSICAL card for the user UID1 with valid token, with status 200

    Then I check card status is CARD_STATUS_ACTIVE for user UID1 for PHYSICAL card

    Then I deposit 50 PKR into wallet with product code CASH_WALLET_CURRENT for user UID1 and expect a status code of 200

    And I check the balance of the wallet with product code CASH_WALLET_CURRENT for user UID1 and the balance should be 50 PKR exact

    And I DISABLE roundups for user UID1

  #   10 INC_AUTH
    Given I create below transaction for PHYSICAL card for user profile id and expect a status code of 200
      | user_profile_identifier | transaction_permutation_name | billing_amount | is_foreign_txn | channel    |
      | UID1                    | INC_AUTH                     | 0.937          | false          | E_COMMERCE |

    And I check the balance of the wallet with product code CASH_WALLET_CURRENT for user UID1 and the balance should be 49 PKR approx

#    11 INC_AUTH_CLEAR
    Given I create below transaction for PHYSICAL card for user profile id and expect a status code of 200
      | user_profile_identifier | transaction_permutation_name | billing_amount | is_foreign_txn | channel    |
      | UID1                    | INC_AUTH_CLEAR               | 0.209          | false          | E_COMMERCE |

    And I check the balance of the wallet with product code CASH_WALLET_CURRENT for user UID1 and the balance should be 48 PKR approx

#  12 INC_AUTH_PARTIAL_CLEARING
    Given I create below transaction for PHYSICAL card for user profile id and expect a status code of 200
      | user_profile_identifier | transaction_permutation_name | billing_amount | is_foreign_txn | channel    |
      | UID1                    | INC_AUTH_PARTIAL_CLEARING    | 2.51           | false          | E_COMMERCE |

    And I check the balance of the wallet with product code CASH_WALLET_CURRENT for user UID1 and the balance should be 46 PKR approx

# 13 INC_AUTH_MULTI_CLEAR
    Given I create below transaction for PHYSICAL card for user profile id and expect a status code of 200
      | user_profile_identifier | transaction_permutation_name | billing_amount | is_foreign_txn | channel    |
      | UID1                    | INC_AUTH_MULTI_CLEAR         | 23.86          | false          | E_COMMERCE |

    And I check the balance of the wallet with product code CASH_WALLET_CURRENT for user UID1 and the balance should be 22 PKR approx

#  14 INC_AUTH_FR
    Given I create below transaction for PHYSICAL card for user profile id and expect a status code of 200
      | user_profile_identifier | transaction_permutation_name | billing_amount | is_foreign_txn | channel    |
      | UID1                    | INC_AUTH_FR                  | 3.83           | false          | E_COMMERCE |

    And I check the balance of the wallet with product code CASH_WALLET_CURRENT for user UID1 and the balance should be 22 PKR approx

#  15 INC_AUTH_PR
    Given I create below transaction for PHYSICAL card for user profile id and expect a status code of 200
      | user_profile_identifier | transaction_permutation_name | billing_amount | is_foreign_txn | channel    |
      | UID1                    | INC_AUTH_PR                  | 4.83           | false          | E_COMMERCE |

    And I check the balance of the wallet with product code CASH_WALLET_CURRENT for user UID1 and the balance should be 20 PKR approx

  #  15 INC_AUTH_PR_FR
    Given I create below transaction for PHYSICAL card for user profile id and expect a status code of 200
      | user_profile_identifier | transaction_permutation_name | billing_amount | is_foreign_txn | channel    |
      | UID1                    | INC_AUTH_PR_FR               | 6.19           | false          | E_COMMERCE |

    And I check the balance of the wallet with product code CASH_WALLET_CURRENT for user UID1 and the balance should be 20 PKR approx

#  16 INC_AUTH_PR_CLEAR - not working
    Given I create below transaction for PHYSICAL card for user profile id and expect a status code of 200
      | user_profile_identifier | transaction_permutation_name | billing_amount | is_foreign_txn | channel    |
      | UID1                    | INC_AUTH_PR_CLEAR            | 5.67           | false          | E_COMMERCE |

    And I check the balance of the wallet with product code CASH_WALLET_CURRENT for user UID1 and the balance should be 17 PKR approx

#  17 INC_AUTH_PR_MULTI_CLEAR
    Given I create below transaction for PHYSICAL card for user profile id and expect a status code of 200
      | user_profile_identifier | transaction_permutation_name | billing_amount | is_foreign_txn | channel    |
      | UID1                    | INC_AUTH_PR_MULTI_CLEAR      | 4.07           | false          | E_COMMERCE |

    And I check the balance of the wallet with product code CASH_WALLET_CURRENT for user UID1 and the balance should be 15 PKR approx

  Scenario: Negative Scenarios - Invalid Billing Amounts - Balance should not be deducted for user for VISA Physical Card.

    Then I initiate the initial user authorisation to ORDER_CARD for user UID1 and expect a status of USER_AUTHORISATION_SUCCESS

    Then I initiate the final user authorisation to ORDER_CARD and expect a user authorisation status as USER_AUTHORISATION_INITIATED for user UID1

    And I initiate the PASSCODE journey within the PASSCODE_STEP for user UID1 to authorise the user and expect a status JOURNEY_INITIATED

    Then I process the PASSCODE journey within the PASSCODE_STEP for user UID1 to authorise the user and expect a status JOURNEY_PROCESSED

    And I submit the PASSCODE journey within the PASSCODE_STEP for user UID1 to authorise the user and expect a status JOURNEY_SUCCESSFUL

    Then I submit the final user authorisation for ORDER_CARD of user UID1 and expect a status USER_AUTHORISATION_SUBMITTED

    And I get the final user authorisation token for ORDER_CARD of user UID1 and expect a status USER_AUTHORISATION_SUCCESS

    Then I get the user cash wallets for the user UID1 and expect the account status of CASH_ACCOUNT_STATUS_CREATED

    Then I order a physical card for UID1 with card name as random_valid_choice and expect a status code of 200 and expect a card status of CARD_STATUS_PENDING

    Then I initiate the initial user authorisation to ACTIVATE_CARD for user UID1 and expect a status of USER_AUTHORISATION_SUCCESS

    Then I initiate the final user authorisation to ACTIVATE_CARD and expect a user authorisation status as USER_AUTHORISATION_INITIATED for user UID1

    And I initiate the PASSCODE journey within the PASSCODE_STEP for user UID1 to authorise the user and expect a status JOURNEY_INITIATED

    Then I process the PASSCODE journey within the PASSCODE_STEP for user UID1 to authorise the user and expect a status JOURNEY_PROCESSED

    And I submit the PASSCODE journey within the PASSCODE_STEP for user UID1 to authorise the user and expect a status JOURNEY_SUCCESSFUL

    Then I submit the final user authorisation for ACTIVATE_CARD of user UID1 and expect a status USER_AUTHORISATION_SUBMITTED

    And I get the final user authorisation token for ACTIVATE_CARD of user UID1 and expect a status USER_AUTHORISATION_SUCCESS

    Then I wait for card status as CARD_STATUS_INACTIVE to activate PHYSICAL card for user UID1

    Then I wait for 40 seconds

    Then I activate the PHYSICAL card for the user UID1 with valid token, with status 200

    Then I check card status is CARD_STATUS_ACTIVE for user UID1 for PHYSICAL card

    Then I deposit 100 PKR into wallet with product code CASH_WALLET_CURRENT for user UID1 and expect a status code of 200

    And I check the balance of the wallet with product code CASH_WALLET_CURRENT for user UID1 and the balance should be 100 PKR exact

#    1. auth
    Given I create below transaction for PHYSICAL card for user profile id and expect a status code of HSA_9000
      | user_profile_identifier | transaction_permutation_name | billing_amount | is_foreign_txn |
      | UID1                    | AUTH                         | 0              | false          |

    And I check the balance of the wallet with product code CASH_WALLET_CURRENT for user UID1 and the balance should be 100 PKR approx

# 2. AUTH_CLEAR with RU
    Given I create below transaction for PHYSICAL card for user profile id and expect a status code of HSA_9000
      | user_profile_identifier | transaction_permutation_name | billing_amount   | is_foreign_txn |
      | UID1                    | AUTH_CLEAR                   | 0                | true           |
      | UID1                    | AUTH_CLEAR                   | -2948.2          | true           |
      | UID1                    | AUTH_CLEAR                   | someGarbageValue | false          |

    And I check the balance of the wallet with product code CASH_WALLET_CURRENT for user UID1 and the balance should be 100 PKR approx

# 3. AUTH_PARTIAL_CLEARING with RU
    Given I create below transaction for PHYSICAL card for user profile id and expect a status code of HSA_9000
      | user_profile_identifier | transaction_permutation_name | billing_amount   | is_foreign_txn |
      | UID1                    | AUTH_PARTIAL_CLEARING        | 0                | false          |
      | UID1                    | AUTH_PARTIAL_CLEARING        | -2948.2          | true           |
      | UID1                    | AUTH_PARTIAL_CLEARING        | someGarbageValue | false          |

    And I check the balance of the wallet with product code CASH_WALLET_CURRENT for user UID1 and the balance should be 100 PKR approx

  #4. AUTH_MULTI_CLEARING
    Given I create below transaction for PHYSICAL card for user profile id and expect a status code of HSA_9000
      | user_profile_identifier | transaction_permutation_name | billing_amount   | is_foreign_txn |
      | UID1                    | AUTH_MULTI_CLEAR             | 0                | true           |
      | UID1                    | AUTH_MULTI_CLEAR             | -2948.2          | true           |
      | UID1                    | AUTH_MULTI_CLEAR             | someGarbageValue | false          |

    And I check the balance of the wallet with product code CASH_WALLET_CURRENT for user UID1 and the balance should be 100 PKR approx

# 5. AUTH_FR
    Given I create below transaction for PHYSICAL card for user profile id and expect a status code of HSA_9000
      | user_profile_identifier | transaction_permutation_name | billing_amount   | is_foreign_txn |
      | UID1                    | AUTH_FR                      | 0                | false          |
      | UID1                    | AUTH_FR                      | -2948.2          | true           |
      | UID1                    | AUTH_FR                      | someGarbageValue | false          |

    And I check the balance of the wallet with product code CASH_WALLET_CURRENT for user UID1 and the balance should be 100 PKR approx

#    6. AUTH_PR
    Given I create below transaction for PHYSICAL card for user profile id and expect a status code of HSA_9000
      | user_profile_identifier | transaction_permutation_name | billing_amount   | is_foreign_txn |
      | UID1                    | AUTH_PR                      | 0                | false          |
      | UID1                    | AUTH_PR                      | -0.2             | true           |
      | UID1                    | AUTH_PR                      | someGarbageValue | false          |

    And I check the balance of the wallet with product code CASH_WALLET_CURRENT for user UID1 and the balance should be 100 PKR approx

      #    7.AUTH_PR_FR
    Given I create below transaction for PHYSICAL card for user profile id and expect a status code of HSA_9000
      | user_profile_identifier | transaction_permutation_name | billing_amount   | is_foreign_txn |
      | UID1                    | AUTH_PR_FR                   | 0                | false          |
      | UID1                    | AUTH_PR_FR                   | -2948.2          | true           |
      | UID1                    | AUTH_PR_FR                   | someGarbageValue | false          |

    And I check the balance of the wallet with product code CASH_WALLET_CURRENT for user UID1 and the balance should be 100 PKR approx

      # 8. AUTH_PR_CLEAR  -
    Given I create below transaction for PHYSICAL card for user profile id and expect a status code of HSA_9000
      | user_profile_identifier | transaction_permutation_name | billing_amount   | is_foreign_txn |
      | UID1                    | AUTH_PR_CLEAR                | 0                | false          |
      | UID1                    | AUTH_PR_CLEAR                | -282141124.2     | true           |
      | UID1                    | AUTH_PR_CLEAR                | someGarbageValue | false          |

    And I check the balance of the wallet with product code CASH_WALLET_CURRENT for user UID1 and the balance should be 100 PKR approx

      #  9 INC_AUTH_PR_MULTI_CLEAR
    Given I create below transaction for PHYSICAL card for user profile id and expect a status code of HSA_9000
      | user_profile_identifier | transaction_permutation_name | billing_amount   | is_foreign_txn |
      | UID1                    | INC_AUTH_PR_MULTI_CLEAR      | 0                | false          |
      | UID1                    | INC_AUTH_PR_MULTI_CLEAR      | -28.2            | true           |
      | UID1                    | INC_AUTH_PR_MULTI_CLEAR      | someGarbageValue | false          |

    And I check the balance of the wallet with product code CASH_WALLET_CURRENT for user UID1 and the balance should be 100 PKR approx

      #  13 refund_AUTH
    Given I create below transaction for PHYSICAL card for user profile id and expect a status code of HSA_9000
      | user_profile_identifier | transaction_permutation_name | billing_amount   | is_foreign_txn |
      | UID1                    | REFUND_AUTH                  | 0                | false          |
      | UID1                    | REFUND_AUTH                  | -02              | true           |
      | UID1                    | REFUND_AUTH                  | someGarbageValue | false          |

    And I check the balance of the wallet with product code CASH_WALLET_CURRENT for user UID1 and the balance should be 100 PKR approx

      #  14 refund_CLEAR
    Given I create below transaction for PHYSICAL card for user profile id and expect a status code of HSA_9000
      | user_profile_identifier | transaction_permutation_name | billing_amount   | is_foreign_txn |
      | UID1                    | REFUND_CLEAR                 | 0                | false          |
      | UID1                    | REFUND_CLEAR                 | -48.2            | true           |
      | UID1                    | REFUND_CLEAR                 | someGarbageValue | false          |

    And I check the balance of the wallet with product code CASH_WALLET_CURRENT for user UID1 and the balance should be 100 PKR approx

    Given I create below transaction for PHYSICAL card for user profile id and expect a status code of HSA_9000
      | user_profile_identifier | transaction_permutation_name | billing_amount   | is_foreign_txn |
#      | UID1                    | REFUND_AUTH_REFUND_CLEAR     | -21.48.2         | true           |
      | UID1                    | REFUND_AUTH_REFUND_CLEAR     | 0                | false          |
      | UID1                    | REFUND_AUTH_REFUND_CLEAR     | someGarbageValue | false          |

    And I check the balance of the wallet with product code CASH_WALLET_CURRENT for user UID1 and the balance should be 100 PKR approx

    Given I create below transaction for PHYSICAL card for user profile id and expect a status code of E9409
      | user_profile_identifier | transaction_permutation_name | billing_amount   | is_foreign_txn |
      | UID1                    | REFUND_AUTH_REFUND_CLEAR     | -21.48.2         | true           |

    And I check the balance of the wallet with product code CASH_WALLET_CURRENT for user UID1 and the balance should be 100 PKR approx


  Scenario: Physical Card - Failure Scenarios

    Then I initiate the initial user authorisation to ORDER_CARD for user UID1 and expect a status of USER_AUTHORISATION_SUCCESS

    Then I initiate the final user authorisation to ORDER_CARD and expect a user authorisation status as USER_AUTHORISATION_INITIATED for user UID1

    And I initiate the PASSCODE journey within the PASSCODE_STEP for user UID1 to authorise the user and expect a status JOURNEY_INITIATED

    Then I process the PASSCODE journey within the PASSCODE_STEP for user UID1 to authorise the user and expect a status JOURNEY_PROCESSED

    And I submit the PASSCODE journey within the PASSCODE_STEP for user UID1 to authorise the user and expect a status JOURNEY_SUCCESSFUL

    Then I submit the final user authorisation for ORDER_CARD of user UID1 and expect a status USER_AUTHORISATION_SUBMITTED

    And I get the final user authorisation token for ORDER_CARD of user UID1 and expect a status USER_AUTHORISATION_SUCCESS

    Then I get the user cash wallets for the user UID1 and expect the account status of CASH_ACCOUNT_STATUS_CREATED

    Then I order a physical card for UID1 with card name as random_valid_choice and expect a status code of 200 and expect a card status of CARD_STATUS_PENDING

    Then I initiate the initial user authorisation to ACTIVATE_CARD for user UID1 and expect a status of USER_AUTHORISATION_SUCCESS

    Then I initiate the final user authorisation to ACTIVATE_CARD and expect a user authorisation status as USER_AUTHORISATION_INITIATED for user UID1

    And I initiate the PASSCODE journey within the PASSCODE_STEP for user UID1 to authorise the user and expect a status JOURNEY_INITIATED

    Then I process the PASSCODE journey within the PASSCODE_STEP for user UID1 to authorise the user and expect a status JOURNEY_PROCESSED

    And I submit the PASSCODE journey within the PASSCODE_STEP for user UID1 to authorise the user and expect a status JOURNEY_SUCCESSFUL

    Then I submit the final user authorisation for ACTIVATE_CARD of user UID1 and expect a status USER_AUTHORISATION_SUBMITTED

    And I get the final user authorisation token for ACTIVATE_CARD of user UID1 and expect a status USER_AUTHORISATION_SUCCESS

    Then I wait for card status as CARD_STATUS_INACTIVE to activate PHYSICAL card for user UID1

    Then I wait for 40 seconds

    Then I activate the PHYSICAL card for the user UID1 with invalid token, with status HSA_9102

    Then I initiate the final user authorisation to ACTIVATE_CARD and expect a user authorisation status as USER_AUTHORISATION_INITIATED for user UID1

    And I initiate the PASSCODE journey within the PASSCODE_STEP for user UID1 to authorise the user and expect a status JOURNEY_INITIATED

    Then I process the PASSCODE journey within the PASSCODE_STEP for user UID1 to authorise the user and expect a status JOURNEY_PROCESSED

    And I submit the PASSCODE journey within the PASSCODE_STEP for user UID1 to authorise the user and expect a status JOURNEY_SUCCESSFUL

    Then I submit the final user authorisation for ACTIVATE_CARD of user UID1 and expect a status USER_AUTHORISATION_SUBMITTED

    And I get the final user authorisation token for ACTIVATE_CARD of user UID1 and expect a status USER_AUTHORISATION_SUCCESS

    Then Invalid card scenario, activate_invalid_card_id, for user UID1 with status HSA_9105

    Then I check card status is CARD_STATUS_INACTIVE for user UID1 for PHYSICAL card

    Then I initiate the initial user authorisation to ACTIVATE_CARD for user UID1 and expect a status of USER_AUTHORISATION_SUCCESS

    Then I initiate the final user authorisation to ACTIVATE_CARD and expect a user authorisation status as USER_AUTHORISATION_INITIATED for user UID1

    And I initiate the PASSCODE journey within the PASSCODE_STEP for user UID1 to authorise the user and expect a status JOURNEY_INITIATED

    Then I process the PASSCODE journey within the PASSCODE_STEP for user UID1 to authorise the user and expect a status JOURNEY_PROCESSED

    And I submit the PASSCODE journey within the PASSCODE_STEP for user UID1 to authorise the user and expect a status JOURNEY_SUCCESSFUL

    Then I submit the final user authorisation for ACTIVATE_CARD of user UID1 and expect a status USER_AUTHORISATION_SUBMITTED

    And I get the final user authorisation token for ACTIVATE_CARD of user UID1 and expect a status USER_AUTHORISATION_SUCCESS

    Then I wait for card status as CARD_STATUS_INACTIVE to activate PHYSICAL card for user UID1

    Then I wait for 40 seconds

    Then I activate the PHYSICAL card for the user UID1 with valid token, with status 200

    Then I check card status is CARD_STATUS_ACTIVE for user UID1 for PHYSICAL card

    Then I initiate the initial user authorisation to UPDATE_CARD_STATUS for user UID1 and expect a status of USER_AUTHORISATION_SUCCESS

    Then I initiate the final user authorisation to UPDATE_CARD_STATUS and expect a user authorisation status as USER_AUTHORISATION_INITIATED for user UID1

    And I initiate the PASSCODE journey within the PASSCODE_STEP for user UID1 to authorise the user and expect a status JOURNEY_INITIATED

    Then I process the PASSCODE journey within the PASSCODE_STEP for user UID1 to authorise the user and expect a status JOURNEY_PROCESSED

    And I submit the PASSCODE journey within the PASSCODE_STEP for user UID1 to authorise the user and expect a status JOURNEY_SUCCESSFUL

    Then I submit the final user authorisation for UPDATE_CARD_STATUS of user UID1 and expect a status USER_AUTHORISATION_SUBMITTED

    And I get the final user authorisation token for UPDATE_CARD_STATUS of user UID1 and expect a status USER_AUTHORISATION_SUCCESS

    Then I update the card status of the PHYSICAL card to INVALID_ACTION for user UID1 and expect a status code of HSA_9179

    Then Invalid card scenario, get_details_invalid_card_id, for user UID1 with status HSA_9105

    Then I initiate the initial user authorisation to UPDATE_CARD_STATUS for user UID1 and expect a status of USER_AUTHORISATION_SUCCESS

    Then I initiate the final user authorisation to UPDATE_CARD_STATUS and expect a user authorisation status as USER_AUTHORISATION_INITIATED for user UID1

    And I initiate the PASSCODE journey within the PASSCODE_STEP for user UID1 to authorise the user and expect a status JOURNEY_INITIATED

    Then I process the PASSCODE journey within the PASSCODE_STEP for user UID1 to authorise the user and expect a status JOURNEY_PROCESSED

    And I submit the PASSCODE journey within the PASSCODE_STEP for user UID1 to authorise the user and expect a status JOURNEY_SUCCESSFUL

    Then I submit the final user authorisation for UPDATE_CARD_STATUS of user UID1 and expect a status USER_AUTHORISATION_SUBMITTED

    And I get the final user authorisation token for UPDATE_CARD_STATUS of user UID1 and expect a status USER_AUTHORISATION_SUCCESS

    Then Invalid card scenario, update_status_invalid_card_id, for user UID1 with status HSA_9105
