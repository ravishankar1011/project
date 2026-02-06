Feature: Roundups scenarios for a PLUS account

  Background: Create a HUGOBANK PLUS accounts to test roundup scenarios

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

  Scenario: Create a new virtual card for a user, Check for Roundup updates, sweep to the main cash account

    Given I initiate the initial user authorisation to ORDER_CARD for user UID1 and expect a status of USER_AUTHORISATION_SUCCESS

    Then I initiate the final user authorisation to ORDER_CARD and expect a user authorisation status as USER_AUTHORISATION_INITIATED for user UID1

    And I initiate the PASSCODE journey within the PASSCODE_STEP for user UID1 to authorise the user and expect a status JOURNEY_INITIATED

    Then I process the PASSCODE journey within the PASSCODE_STEP for user UID1 to authorise the user and expect a status JOURNEY_PROCESSED

    And I submit the PASSCODE journey within the PASSCODE_STEP for user UID1 to authorise the user and expect a status JOURNEY_SUCCESSFUL

    Then I submit the final user authorisation for ORDER_CARD of user UID1 and expect a status USER_AUTHORISATION_SUBMITTED

    And I get the final user authorisation token for ORDER_CARD of user UID1 and expect a status USER_AUTHORISATION_SUCCESS

    Then I get the user cash wallets for the user UID1 and expect the account status of CASH_ACCOUNT_STATUS_CREATED

    Then I order a virtual card for UID1 with card name as random_valid_choice and expect a status code of 200 and expect a card status of CARD_STATUS_PENDING

    Then I wait for card status as CARD_STATUS_ACTIVE to activate VIRTUAL card for user UID1

    Then I check card status is CARD_STATUS_ACTIVE for user UID1 for VIRTUAL card

    Then I deposit 60000 PKR into wallet with product code CASH_WALLET_CURRENT for user UID1 and expect a status code of 200

    And I check the balance of the wallet with product code CASH_WALLET_CURRENT for user UID1 and the balance should be 60000 PKR exact

    Given I ENABLE roundups for user UID1

    Then I trigger roundups for the new VIRTUAL card user UID1 and expect trigger initialisation status as True

    Given I create below transaction for VIRTUAL card for user profile id and expect a status code of 200
      | user_profile_identifier | transaction_permutation_name | billing_amount | is_foreign_txn |
      | UID1                    | AUTH_CLEAR                   | 9              | false          |

    And I check the balance of the wallet with product code CASH_WALLET_ROUNDUP for user UID1 and the balance should be 91 PKR exact

    And I check the balance of the wallet with product code CASH_WALLET_CURRENT for user UID1 and the balance should be 59900 PKR exact

    # sweep steps
    Then I transfer 50 PKR from roundups account to the CASH_WALLET_CURRENT for user UID1 and expect a status code of 200

    And I check the balance of the wallet with product code CASH_WALLET_ROUNDUP for user UID1 and the balance should be 41 SGD exact

    And I check the balance of the wallet with product code CASH_WALLET_CURRENT for user UID1 and the balance should be 59950 PKR exact

  Scenario: Create a new virtual card for a user, Check for Roundup updates, sweep to a user created map

    Given I initiate the initial user authorisation to ORDER_CARD for user UID1 and expect a status of USER_AUTHORISATION_SUCCESS

    Then I initiate the final user authorisation to ORDER_CARD and expect a user authorisation status as USER_AUTHORISATION_INITIATED for user UID1

    And I initiate the PASSCODE journey within the PASSCODE_STEP for user UID1 to authorise the user and expect a status JOURNEY_INITIATED

    Then I process the PASSCODE journey within the PASSCODE_STEP for user UID1 to authorise the user and expect a status JOURNEY_PROCESSED

    And I submit the PASSCODE journey within the PASSCODE_STEP for user UID1 to authorise the user and expect a status JOURNEY_SUCCESSFUL

    Then I submit the final user authorisation for ORDER_CARD of user UID1 and expect a status USER_AUTHORISATION_SUBMITTED

    And I get the final user authorisation token for ORDER_CARD of user UID1 and expect a status USER_AUTHORISATION_SUCCESS

    Then I get the user cash wallets for the user UID1 and expect the account status of CASH_ACCOUNT_STATUS_CREATED

    Then I order a virtual card for UID1 with card name as random_valid_choice and expect a status code of 200 and expect a card status of CARD_STATUS_PENDING

    Then I wait for card status as CARD_STATUS_ACTIVE to activate VIRTUAL card for user UID1

    Then I check card status is CARD_STATUS_ACTIVE for user UID1 for VIRTUAL card

    Then I deposit 60000 PKR into wallet with product code CASH_WALLET_CURRENT for user UID1 and expect a status code of 200

    And I check the balance of the wallet with product code CASH_WALLET_CURRENT for user UID1 and the balance should be 60000 PKR exact

    Given I ENABLE roundups for user UID1

    Then I trigger roundups for the new VIRTUAL card user UID1 and expect trigger initialisation status as True

    Given I create below transaction for VIRTUAL card for user profile id and expect a status code of 200
      | user_profile_identifier | transaction_permutation_name | billing_amount | is_foreign_txn |
      | UID1                    | AUTH_CLEAR                   | 9              | false          |

    And I check the balance of the wallet with product code CASH_WALLET_ROUNDUP for user UID1 and the balance should be 91 PKR exact

    And I check the balance of the wallet with product code CASH_WALLET_CURRENT for user UID1 and the balance should be 59900 PKR exact

    # sweep steps
    Given I create a Map MPID1 and expect a status of MAP_CREATED
      | user_profile_identifier | name   | asset_allocation_details                  | allocation_type | goal_date  | goal_amount |
      | UID1                    | random | [{"asset_id": "CASH" ,"percentage": 100}] | FIXED           | 03-06-2024 | 100         |

    Then I check if the map MPID1 is created for user UID1 and expect a status of MAP_CREATED

    Then I save map MPID1 for the Roundup Sweep for the user UID1

    Then I trigger schedule SCHEDULE_ROUNDUP for user UID1 and expect a status code of 200

    And I check the balance of the wallet with product code CASH_WALLET_ROUNDUP for user UID1 and the balance should be 0 PKR exact

    Then I check the balance of map MPID1 of user UID1 to be 91 PKR

  Scenario: Create a new physical card for a user, Check for Roundup updates, sweep to the main cash account

    Given I add a new Home Address to order a Card for user UID1 and expect a status code of 200

    Then I check if the Home Address is added successfully for the user UID1

    Given I initiate the initial user authorisation to ORDER_CARD for user UID1 and expect a status of USER_AUTHORISATION_SUCCESS

    Then I initiate the final user authorisation to ORDER_CARD and expect a user authorisation status as USER_AUTHORISATION_INITIATED for user UID1

    And I initiate the PASSCODE journey within the PASSCODE_STEP for user UID1 to authorise the user and expect a status JOURNEY_INITIATED

    Then I process the PASSCODE journey within the PASSCODE_STEP for user UID1 to authorise the user and expect a status JOURNEY_PROCESSED

    And I submit the PASSCODE journey within the PASSCODE_STEP for user UID1 to authorise the user and expect a status JOURNEY_SUCCESSFUL

    Then I submit the final user authorisation for ORDER_CARD of user UID1 and expect a status USER_AUTHORISATION_SUBMITTED

    And I get the final user authorisation token for ORDER_CARD of user UID1 and expect a status USER_AUTHORISATION_SUCCESS

    Then I get the user cash wallets for the user UID1 and expect the account status of CASH_ACCOUNT_STATUS_CREATED

    Then I order a physical card for UID1 with card name as random_valid_choice and expect a status code of 200 and expect a card status of CARD_STATUS_PENDING

    Given I initiate the initial user authorisation to ACTIVATE_CARD for user UID1 and expect a status of USER_AUTHORISATION_SUCCESS

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

    Then I deposit 60000 PKR into wallet with product code CASH_WALLET_CURRENT for user UID1 and expect a status code of 200

    And I check the balance of the wallet with product code CASH_WALLET_CURRENT for user UID1 and the balance should be 60000 PKR exact

    Given I ENABLE roundups for user UID1

    Then I trigger roundups for the new PHYSICAL card user UID1 and expect trigger initialisation status as True

    Given I create below transaction for PHYSICAL card for user profile id and expect a status code of 200
      | user_profile_identifier | transaction_permutation_name | billing_amount | is_foreign_txn |
      | UID1                    | AUTH_CLEAR                   | 9              | false          |

    And I check the balance of the wallet with product code CASH_WALLET_ROUNDUP for user UID1 and the balance should be 91 PKR exact

    And I check the balance of the wallet with product code CASH_WALLET_CURRENT for user UID1 and the balance should be 59900 PKR exact

    Then I transfer 50 PKR from roundups account to the CASH_WALLET_CURRENT for user UID1 and expect a status code of 200

    And I check the balance of the wallet with product code CASH_WALLET_ROUNDUP for user UID1 and the balance should be 41 SGD exact

    And I check the balance of the wallet with product code CASH_WALLET_CURRENT for user UID1 and the balance should be 59950 PKR exact

  Scenario: Create a new physical card for a user, Check for Roundup updates, sweep to a user created map

    Given I add a new Home Address to order a Card for user UID1 and expect a status code of 200

    Then I check if the Home Address is added successfully for the user UID1

    Given I initiate the initial user authorisation to ORDER_CARD for user UID1 and expect a status of USER_AUTHORISATION_SUCCESS

    Then I initiate the final user authorisation to ORDER_CARD and expect a user authorisation status as USER_AUTHORISATION_INITIATED for user UID1

    And I initiate the PASSCODE journey within the PASSCODE_STEP for user UID1 to authorise the user and expect a status JOURNEY_INITIATED

    Then I process the PASSCODE journey within the PASSCODE_STEP for user UID1 to authorise the user and expect a status JOURNEY_PROCESSED

    And I submit the PASSCODE journey within the PASSCODE_STEP for user UID1 to authorise the user and expect a status JOURNEY_SUCCESSFUL

    Then I submit the final user authorisation for ACTIVATE_CARD of user UID1 and expect a status USER_AUTHORISATION_SUBMITTED

    And I get the final user authorisation token for ACTIVATE_CARD of user UID1 and expect a status USER_AUTHORISATION_SUCCESS

    Then I get the user cash wallets for the user UID1 and expect the account status of CASH_ACCOUNT_STATUS_CREATED

    Then I order a physical card for UID1 with card name as random_valid_choice and expect a status code of 200 and expect a card status of CARD_STATUS_PENDING

    Given I initiate the initial user authorisation to ACTIVATE_CARD for user UID1 and expect a status of USER_AUTHORISATION_SUCCESS

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

    Then I deposit 60000 PKR into wallet with product code CASH_WALLET_CURRENT for user UID1 and expect a status code of 200

    And I check the balance of the wallet with product code CASH_WALLET_CURRENT for user UID1 and the balance should be 60000 PKR exact

    Given I ENABLE roundups for user UID1

    Then I trigger roundups for the new PHYSICAL card user UID1 and expect trigger initialisation status as True

    Given I create below transaction for PHYSICAL card for user profile id and expect a status code of 200
      | user_profile_identifier | transaction_permutation_name | billing_amount | is_foreign_txn |
      | UID1                    | AUTH_CLEAR                   | 9            | false          |

    And I check the balance of the wallet with product code CASH_WALLET_ROUNDUP for user UID1 and the balance should be 91 PKR exact

    And I check the balance of the wallet with product code CASH_WALLET_CURRENT for user UID1 and the balance should be 59900 PKR exact

    Then I transfer 50 PKR from roundups account to the CASH_WALLET_CURRENT for user UID1 and expect a status code of 200

    And I check the balance of the wallet with product code CASH_WALLET_ROUNDUP for user UID1 and the balance should be 41 SGD exact

    And I check the balance of the wallet with product code CASH_WALLET_CURRENT for user UID1 and the balance should be 59950 PKR exact

     # sweep steps
    Given I create a Map MPID1 and expect a status of MAP_CREATED
      | user_profile_identifier | name   | asset_allocation_details                  | allocation_type | goal_date  | goal_amount |
      | UID1                    | random | [{"asset_id": "CASH" ,"percentage": 100}] | FIXED           | 03-06-2024 | 100         |

    Then I check if the map MPID1 is created for user UID1 and expect a status of MAP_CREATED

    Then I save map MPID1 for the Roundup Sweep for the user UID1

    Then I trigger schedule SCHEDULE_ROUNDUP for user UID1 and expect a status code of 200

    And I check the balance of the wallet with product code CASH_WALLET_ROUNDUP for user UID1 and the balance should be 0 PKR exact

    Then I check the balance of map MPID1 of user UID1 to be 41 PKR

  Scenario: Disable the Roundups and check the amount deposits back to the main account

    Given I add a new Home Address to order a Card for user UID1 and expect a status code of 200

    Then I check if the Home Address is added successfully for the user UID1

    Given I initiate the initial user authorisation to ORDER_CARD for user UID1 and expect a status of USER_AUTHORISATION_SUCCESS

    Then I initiate the final user authorisation to ORDER_CARD and expect a user authorisation status as USER_AUTHORISATION_INITIATED for user UID1

    And I initiate the PASSCODE journey within the PASSCODE_STEP for user UID1 to authorise the user and expect a status JOURNEY_INITIATED

    Then I process the PASSCODE journey within the PASSCODE_STEP for user UID1 to authorise the user and expect a status JOURNEY_PROCESSED

    And I submit the PASSCODE journey within the PASSCODE_STEP for user UID1 to authorise the user and expect a status JOURNEY_SUCCESSFUL

    Then I submit the final user authorisation for ORDER_CARD of user UID1 and expect a status USER_AUTHORISATION_SUBMITTED

    And I get the final user authorisation token for ORDER_CARD of user UID1 and expect a status USER_AUTHORISATION_SUCCESS

    Then I get the user cash wallets for the user UID1 and expect the account status of CASH_ACCOUNT_STATUS_CREATED

    Then I order a physical card for UID1 with card name as random_valid_choice and expect a status code of 200 and expect a card status of CARD_STATUS_PENDING

    Given I initiate the initial user authorisation to ACTIVATE_CARD for user UID1 and expect a status of USER_AUTHORISATION_SUCCESS

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

    Then I deposit 1000 PKR into wallet with product code CASH_WALLET_CURRENT for user UID1 and expect a status code of 200

    And I check the balance of the wallet with product code CASH_WALLET_CURRENT for user UID1 and the balance should be 1000 PKR exact

    Given I ENABLE roundups for user UID1

    Then I trigger roundups for the new PHYSICAL card user UID1 and expect trigger initialisation status as True

    Given I create below transaction for PHYSICAL card for user profile id and expect a status code of 200
      | user_profile_identifier | transaction_permutation_name | billing_amount | is_foreign_txn |
      | UID1                    | AUTH_CLEAR                   | 9            | false          |

    And I check the balance of the wallet with product code CASH_WALLET_ROUNDUP for user UID1 and the balance should be 91 PKR exact

    And I check the balance of the wallet with product code CASH_WALLET_CURRENT for user UID1 and the balance should be 900 PKR exact

    Given I DISABLE roundups for user UID1

    And I check the balance of the wallet with product code CASH_WALLET_ROUNDUP for user UID1 and the balance should be 0 PKR exact

    And I check the balance of the wallet with product code CASH_WALLET_CURRENT for user UID1 and the balance should be 991 PKR exact

  Scenario: Do a card transaction (assume main account having amount less than 100) and verify the roundup balance remains the same

    Given I add a new Home Address to order a Card for user UID1 and expect a status code of 200

    Then I check if the Home Address is added successfully for the user UID1

    Given I initiate the initial user authorisation to ORDER_CARD for user UID1 and expect a status of USER_AUTHORISATION_SUCCESS

    Then I initiate the final user authorisation to ORDER_CARD and expect a user authorisation status as USER_AUTHORISATION_INITIATED for user UID1

    And I initiate the PASSCODE journey within the PASSCODE_STEP for user UID1 to authorise the user and expect a status JOURNEY_INITIATED

    Then I process the PASSCODE journey within the PASSCODE_STEP for user UID1 to authorise the user and expect a status JOURNEY_PROCESSED

    And I submit the PASSCODE journey within the PASSCODE_STEP for user UID1 to authorise the user and expect a status JOURNEY_SUCCESSFUL

    Then I submit the final user authorisation for ORDER_CARD of user UID1 and expect a status USER_AUTHORISATION_SUBMITTED

    And I get the final user authorisation token for ORDER_CARD of user UID1 and expect a status USER_AUTHORISATION_SUCCESS

    Then I get the user cash wallets for the user UID1 and expect the account status of CASH_ACCOUNT_STATUS_CREATED

    Then I order a physical card for UID1 with card name as random_valid_choice and expect a status code of 200 and expect a card status of CARD_STATUS_PENDING

    Given I initiate the initial user authorisation to ACTIVATE_CARD for user UID1 and expect a status of USER_AUTHORISATION_SUCCESS

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

    Then I deposit 90 PKR into wallet with product code CASH_WALLET_CURRENT for user UID1 and expect a status code of 200

    And I check the balance of the wallet with product code CASH_WALLET_CURRENT for user UID1 and the balance should be 90 PKR exact

    Given I ENABLE roundups for user UID1

    Then I trigger roundups for the new PHYSICAL card user UID1 and expect trigger initialisation status as True

    Given I create below transaction for PHYSICAL card for user profile id and expect a status code of 200
      | user_profile_identifier | transaction_permutation_name | billing_amount | is_foreign_txn |
      | UID1                    | AUTH_CLEAR                   | 10            | false          |

    And I check the balance of the wallet with product code CASH_WALLET_ROUNDUP for user UID1 and the balance should be 0 PKR exact

    And I check the balance of the wallet with product code CASH_WALLET_CURRENT for user UID1 and the balance should be 80 PKR exact
