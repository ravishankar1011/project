Feature: Credit_card feature

  Background: Create 1 HUGOBANK PLUS account to test

    Given The user UID1 provides a valid user name on device_1 to initiate onboarding and the expected status is VERIFICATION_INITIATED
      | user_name | user_name_type | ph_prefix |
      | random    | PHONE_NUMBER   | +373      |

    Then The user UID1 submits OTP to proceed with verification and expects a status code of 200 and a status of VERIFICATION_SUCCESS

    Given User opens a new HUGOBANK user account and expect the status code 200
      | user_profile_identifier | email          | legal_name | name   | account_type |
      | UID1                    | test@gmail.com | John Doe   | Johnny | PERSONAL     |

    Then User UID1 initiates the initial onboarding and expects a status of INITIATED

    Then User UID1 initiates the initial onboarding journey HUGOBANK_VERISYS within the ID_VERIFICATION_STEP and expects a status of JOURNEY_INITIATED

    Then Update HUGOBANK_VERISYS journey within the ID_VERIFICATION_STEP for user UID1 as pass

    Then Process the initial onboarding journey HUGOBANK_VERISYS within the ID_VERIFICATION_STEP for user UID1 and expect a status of JOURNEY_PROCESSED

    Then User UID1 checks the status of the initial onboarding journey HUGOBANK_VERISYS within the ID_VERIFICATION_STEP and the status should be JOURNEY_PROCESSED

    Then User UID1 submits the initial onboarding journey HUGOBANK_VERISYS within the ID_VERIFICATION_STEP and expects the journey status to be JOURNEY_SUBMITTED

    Then User UID1 checks the status of the initial onboarding journey HUGOBANK_VERISYS within the ID_VERIFICATION_STEP and the status should be JOURNEY_SUCCESSFUL

    Then User UID1 initiates the initial onboarding journey HUGOBANK_BIO_VERISYS within the BIOMETRIC_VERIFICATION_STEP and expects a status of JOURNEY_INITIATED

    Then Update HUGOBANK_BIO_VERISYS journey within the BIOMETRIC_VERIFICATION_STEP for user UID1 as pass

    Then Process the initial onboarding journey HUGOBANK_BIO_VERISYS within the BIOMETRIC_VERIFICATION_STEP for user UID1 and expect a status of JOURNEY_PROCESSED

    Then User UID1 checks the status of the initial onboarding journey HUGOBANK_BIO_VERISYS within the BIOMETRIC_VERIFICATION_STEP and the status should be JOURNEY_PROCESSED

    Then User UID1 submits the initial onboarding journey HUGOBANK_BIO_VERISYS within the BIOMETRIC_VERIFICATION_STEP and expects the journey status to be JOURNEY_SUBMITTED

    Then User UID1 submits the initial onboarding, the onboarding status should be IN_PROGRESS and the account level should be L1

    And User UID1 checks the status of initial onboarding and expects an onboarding status of COMPLETED

    And The user profile of user UID1 should be PROFILE_IN_PROGRESS

    Then The authorisation status of device_1 for user UID1 should be DEVICE_AUTHORISATION_SUCCESS

    And Create a binding signature for the user UID1 to bind the device_1 and the device binding status should be ACTIVE

    Then User UID1 should have authorised device device_1

    And User profile of user UID1 should be PROFILE_ACTIVE and the account level should be L1

    When User UID1 initiates the progress onboarding to upgrade the account to L2 and expects an onboarding status of INITIATED

    Then User UID1 initiates the progress onboarding journey HUGOBANK_VERIFY_INCOME within the INCOME_VERIFICATION_STEP and expects a status of JOURNEY_INITIATED

    Then User UID1 uploads document1 for salaryDetails for the HUGOBANK_VERIFY_INCOME journey as the fundsProof

    Then User UID1 uploads document2 for salaryDetails for the HUGOBANK_VERIFY_INCOME journey as the fundsProof

    Then User UID1 uploads document3 for salaryDetails for the HUGOBANK_VERIFY_INCOME journey as the fundsProof

    Then User UID1 uploads document1 for salaryDetails for the HUGOBANK_VERIFY_INCOME journey as the employmentProof

    Then User UID1 uploads document2 for salaryDetails for the HUGOBANK_VERIFY_INCOME journey as the employmentProof

    Then User UID1 uploads document3 for salaryDetails for the HUGOBANK_VERIFY_INCOME journey as the employmentProof

    Then Process the progress onboarding journey HUGOBANK_VERIFY_INCOME within the INCOME_VERIFICATION_STEP for user UID1 and expect a status of JOURNEY_HOLD

    Then Portal operator updates the HUGOBANK_VERIFY_INCOME journey within the INCOME_VERIFICATION_STEP as ACCEPT if operator action status is OPERATOR_ACTION_REQUIRED for user UID1

    Then User UID1 submits the progress onboarding, the onboarding status should be IN_PROGRESS and the account level should be L2

    Given Portal operator updates the onboarding status as ACCEPT if operator action status is OPERATOR_ACTION_REQUIRED for user UID1 to upgrade the account to level L2

    And User UID1 checks the progress onboarding status and the onboardingStatus status should be COMPLETED

    And The user profile of user UID1 should be PROFILE_ACTIVE

    And User profile of user UID1 should be PROFILE_ACTIVE and the account level should be L2

    Then Get the user cash wallets for the user UID1 and expect the account status of CASH_ACCOUNT_STATUS_CREATED

    Then User UID1 deposits 70000 PKR into wallet with product code CASH_WALLET_CURRENT and expects a status code of 200

    And Verify the balance of the wallet with product code CASH_WALLET_CURRENT for user UID1 and the balance should be 70000 PKR exact


  Scenario: Credit card order -> Transactions without activation -> Activation -> Transactions after activation

    Then I fetch credit card constants for HUGOBANK

    And I validate credit card eligibility using balance of the wallet with product code CASH_WALLET_CURRENT for user UID1
      | credit_limit  |
      | 20000         |

    Then User UID1 initiates the initial user authorisation to ORDER_CARD and expects 200 as the status code and a status of USER_AUTHORISATION_SUCCESS

    Then User UID1 initiates the final user authorisation to ORDER_CARD and expects a user authorisation status of USER_AUTHORISATION_INITIATED

    And User UID1 initiates the PASSCODE journey within the PASSCODE_STEP for authorisation and expects a status of JOURNEY_INITIATED

    Then Process the PASSCODE journey within the PASSCODE_STEP for user UID1 to authorise the user and expect a status JOURNEY_PROCESSED

    And User UID1 submits the PASSCODE journey within the PASSCODE_STEP for authorisation and expects a status of JOURNEY_SUCCESSFUL

    Then User UID1 submits the final user authorisation for ORDER_CARD and expects a status of USER_AUTHORISATION_SUBMITTED

    And Get the final user authorisation token for ORDER_CARD of user UID1 and expect a status USER_AUTHORISATION_SUCCESS

    Then I order a Physical Visa Credit Card as CREDIT_CARD for UID1 with card name as random_valid_choice and expect a status code of 200 and expect a card status of CARD_STATUS_PENDING
      | credit_limit  |
      | 20000         |

#--------------------------------Activation and other steps------------------------------------------------------

    Then I fetch credit account list for user UID1
    #------------------------------------Transaction without activation------------------------------------------------

    Given User performs the below transaction with CREDIT_CARD and expects a status code of 200
      | user_profile_identifier | transaction_permutation_name | billing_amount | is_foreign_txn | channel    |
      | UID1                    | AUTH_CLEAR                   | 500            | false          | POS        |

    And I check the available credits for user UID1 and available credit should be 19500 approx

    Given User performs the below transaction with CREDIT_CARD and expects a status code of 200
      | user_profile_identifier | transaction_permutation_name | billing_amount | is_foreign_txn | channel    |
      | UID1                    | AUTH_CLEAR                   | 500            | false          | E_COMMERCE |

    And I check the available credits for user UID1 and available credit should be 19000 approx

#    # ATM transaction — should fail
    Given User performs the below transaction with CREDIT_CARD and expects a status code of HSA_9121
      | user_profile_identifier | transaction_permutation_name | billing_amount | is_foreign_txn | channel    |
      | UID1                    | AUTH_CLEAR                   | 500            | false          | ATM        |

    And I check the available credits for user UID1 and available credit should be 19000 approx

#-------------------------------------Transaction after activation------------------------------------------------

    Then User UID1 initiates the initial user authorisation to ACTIVATE_CARD and expects 200 as the status code and a status of USER_AUTHORISATION_SUCCESS

    Then User UID1 initiates the final user authorisation to ACTIVATE_CARD and expects a user authorisation status of USER_AUTHORISATION_INITIATED

    And User UID1 initiates the PASSCODE journey within the PASSCODE_STEP for authorisation and expects a status of JOURNEY_INITIATED

    Then Process the PASSCODE journey within the PASSCODE_STEP for user UID1 to authorise the user and expect a status JOURNEY_PROCESSED

    And User UID1 submits the PASSCODE journey within the PASSCODE_STEP for authorisation and expects a status of JOURNEY_SUCCESSFUL

    Then User UID1 submits the final user authorisation for ACTIVATE_CARD and expects a status of USER_AUTHORISATION_SUBMITTED

    And Get the final user authorisation token for ACTIVATE_CARD of user UID1 and expect a status USER_AUTHORISATION_SUCCESS

    Then I wait for 40 seconds

    Then I wait for credit card status as CARD_STATUS_UPGRADED to activate PHYSICAL card for user UID1

    Then I wait for 10 seconds

    Then User UID1 activates the CREDIT_CARD with valid token, with status 200

    Then User UID1 checks card status is CARD_STATUS_ACTIVE for CREDIT_CARD

    Given User performs the below transaction with CREDIT_CARD and expects a status code of 200
      | user_profile_identifier | transaction_permutation_name | billing_amount | is_foreign_txn | channel    |
      | UID1                    | AUTH_CLEAR                   | 500            | false          | POS        |

    And I check the available credits for user UID1 and available credit should be 18500 approx

    Given User performs the below transaction with CREDIT_CARD and expects a status code of 200
      | user_profile_identifier | transaction_permutation_name | billing_amount | is_foreign_txn | channel    |
      | UID1                    | AUTH_CLEAR                   | 500            | false          | E_COMMERCE |

    And I check the available credits for user UID1 and available credit should be 18000 approx

    Given User performs the below transaction with CREDIT_CARD and expects a status code of 200
      | user_profile_identifier | transaction_permutation_name | billing_amount | is_foreign_txn | channel    |
      | UID1                    | AUTH_CLEAR                   | 500            | false          | ATM        |

    And I check the available credits for user UID1 and available credit should be 16350 approx


  Scenario: Credit card order -> Activate -> Block -> Unblock -> Disable
#---------------------Ordering card----------------------------------------------------
    Then I fetch credit card constants for HUGOBANK

    And I validate credit card eligibility using balance of the wallet with product code CASH_WALLET_CURRENT for user UID1
      | credit_limit  |
      | 20000         |

    Then User UID1 initiates the initial user authorisation to ORDER_CARD and expects 200 as the status code and a status of USER_AUTHORISATION_SUCCESS

    Then User UID1 initiates the final user authorisation to ORDER_CARD and expects a user authorisation status of USER_AUTHORISATION_INITIATED

    And User UID1 initiates the PASSCODE journey within the PASSCODE_STEP for authorisation and expects a status of JOURNEY_INITIATED

    Then Process the PASSCODE journey within the PASSCODE_STEP for user UID1 to authorise the user and expect a status JOURNEY_PROCESSED

    And User UID1 submits the PASSCODE journey within the PASSCODE_STEP for authorisation and expects a status of JOURNEY_SUCCESSFUL

    Then User UID1 submits the final user authorisation for ORDER_CARD and expects a status of USER_AUTHORISATION_SUBMITTED

    And Get the final user authorisation token for ORDER_CARD of user UID1 and expect a status USER_AUTHORISATION_SUCCESS

    Then I order a Physical Visa Credit Card as CREDIT_CARD for UID1 with card name as random_valid_choice and expect a status code of 200 and expect a card status of CARD_STATUS_PENDING
      | credit_limit  |
      | 20000         |

#---------------------Activating card----------------------------------------------------

    Then User UID1 initiates the initial user authorisation to ACTIVATE_CARD and expects 200 as the status code and a status of USER_AUTHORISATION_SUCCESS

    Then User UID1 initiates the final user authorisation to ACTIVATE_CARD and expects a user authorisation status of USER_AUTHORISATION_INITIATED

    And User UID1 initiates the PASSCODE journey within the PASSCODE_STEP for authorisation and expects a status of JOURNEY_INITIATED

    Then Process the PASSCODE journey within the PASSCODE_STEP for user UID1 to authorise the user and expect a status JOURNEY_PROCESSED

    And User UID1 submits the PASSCODE journey within the PASSCODE_STEP for authorisation and expects a status of JOURNEY_SUCCESSFUL

    Then User UID1 submits the final user authorisation for ACTIVATE_CARD and expects a status of USER_AUTHORISATION_SUBMITTED

    And Get the final user authorisation token for ACTIVATE_CARD of user UID1 and expect a status USER_AUTHORISATION_SUCCESS

    Then I wait for 40 seconds

    Then I wait for credit card status as CARD_STATUS_UPGRADED to activate PHYSICAL card for user UID1

    Then I wait for 10 seconds

    Then User UID1 activates the CREDIT_CARD with valid token, with status 200

    Then User UID1 checks card status is CARD_STATUS_ACTIVE for CREDIT_CARD

#---------------------Blocking card----------------------------------------------------
    Then User UID1 initiates the initial user authorisation to UPDATE_CARD_STATUS and expects 200 as the status code and a status of USER_AUTHORISATION_SUCCESS

    Then User UID1 initiates the final user authorisation to UPDATE_CARD_STATUS and expects a user authorisation status of USER_AUTHORISATION_INITIATED

    And User UID1 initiates the PASSCODE journey within the PASSCODE_STEP for authorisation and expects a status of JOURNEY_INITIATED

    Then Process the PASSCODE journey within the PASSCODE_STEP for user UID1 to authorise the user and expect a status JOURNEY_PROCESSED

    And User UID1 submits the PASSCODE journey within the PASSCODE_STEP for authorisation and expects a status of JOURNEY_SUCCESSFUL

    Then User UID1 submits the final user authorisation for UPDATE_CARD_STATUS and expects a status of USER_AUTHORISATION_SUBMITTED

    And Get the final user authorisation token for UPDATE_CARD_STATUS of user UID1 and expect a status USER_AUTHORISATION_SUCCESS

    Then I wait for 40 seconds

    Then User UID1 updates the card status of the CREDIT_CARD to BLOCK and expects a status code of 200

    Then I wait for 10 seconds

    Then User UID1 checks card status is CARD_STATUS_BLOCKED for CREDIT_CARD

#---------------------Un-Blocking card----------------------------------------------------
    Then User UID1 initiates the initial user authorisation to UPDATE_CARD_STATUS and expects 200 as the status code and a status of USER_AUTHORISATION_SUCCESS

    Then User UID1 initiates the final user authorisation to UPDATE_CARD_STATUS and expects a user authorisation status of USER_AUTHORISATION_INITIATED

    And User UID1 initiates the PASSCODE journey within the PASSCODE_STEP for authorisation and expects a status of JOURNEY_INITIATED

    Then Process the PASSCODE journey within the PASSCODE_STEP for user UID1 to authorise the user and expect a status JOURNEY_PROCESSED

    And User UID1 submits the PASSCODE journey within the PASSCODE_STEP for authorisation and expects a status of JOURNEY_SUCCESSFUL

    Then User UID1 submits the final user authorisation for UPDATE_CARD_STATUS and expects a status of USER_AUTHORISATION_SUBMITTED

    And Get the final user authorisation token for UPDATE_CARD_STATUS of user UID1 and expect a status USER_AUTHORISATION_SUCCESS

    Then I wait for 40 seconds

    Then User UID1 updates the card status of the CREDIT_CARD to UNBLOCK and expects a status code of 200

    Then I wait for 10 seconds

    Then User UID1 checks card status is CARD_STATUS_ACTIVE for CREDIT_CARD

#---------------------Disable card----------------------------------------------------
    Then User UID1 initiates the initial user authorisation to UPDATE_CARD_STATUS and expects 200 as the status code and a status of USER_AUTHORISATION_SUCCESS

    Then User UID1 initiates the final user authorisation to UPDATE_CARD_STATUS and expects a user authorisation status of USER_AUTHORISATION_INITIATED

    And User UID1 initiates the PASSCODE journey within the PASSCODE_STEP for authorisation and expects a status of JOURNEY_INITIATED

    Then Process the PASSCODE journey within the PASSCODE_STEP for user UID1 to authorise the user and expect a status JOURNEY_PROCESSED

    And User UID1 submits the PASSCODE journey within the PASSCODE_STEP for authorisation and expects a status of JOURNEY_SUCCESSFUL

    Then User UID1 submits the final user authorisation for UPDATE_CARD_STATUS and expects a status of USER_AUTHORISATION_SUBMITTED

    And Get the final user authorisation token for UPDATE_CARD_STATUS of user UID1 and expect a status USER_AUTHORISATION_SUCCESS

    Then I wait for 40 seconds

    Then User UID1 updates the card status of the CREDIT_CARD to DISABLE and expects a status code of 200

    Then I wait for 10 seconds

    Then User UID1 checks card status is CARD_STATUS_DISABLED for CREDIT_CARD


  Scenario: User views credit card PIN successfully
#------------------------Ordering and activating card----------------------------
    Then I fetch credit card constants for HUGOBANK

    And I validate credit card eligibility using balance of the wallet with product code CASH_WALLET_CURRENT for user UID1
      | credit_limit  |
      | 20000         |

    Then User UID1 initiates the initial user authorisation to ORDER_CARD and expects 200 as the status code and a status of USER_AUTHORISATION_SUCCESS

    Then User UID1 initiates the final user authorisation to ORDER_CARD and expects a user authorisation status of USER_AUTHORISATION_INITIATED

    And User UID1 initiates the PASSCODE journey within the PASSCODE_STEP for authorisation and expects a status of JOURNEY_INITIATED

    Then Process the PASSCODE journey within the PASSCODE_STEP for user UID1 to authorise the user and expect a status JOURNEY_PROCESSED

    And User UID1 submits the PASSCODE journey within the PASSCODE_STEP for authorisation and expects a status of JOURNEY_SUCCESSFUL

    Then User UID1 submits the final user authorisation for ORDER_CARD and expects a status of USER_AUTHORISATION_SUBMITTED

    And Get the final user authorisation token for ORDER_CARD of user UID1 and expect a status USER_AUTHORISATION_SUCCESS

    Then I order a Physical Visa Credit Card as CREDIT_CARD for UID1 with card name as random_valid_choice and expect a status code of 200 and expect a card status of CARD_STATUS_PENDING
      | credit_limit  |
      | 20000         |

#---------------------Activating card----------------------------------------------------
    Then User UID1 initiates the initial user authorisation to ACTIVATE_CARD and expects 200 as the status code and a status of USER_AUTHORISATION_SUCCESS

    Then User UID1 initiates the final user authorisation to ACTIVATE_CARD and expects a user authorisation status of USER_AUTHORISATION_INITIATED

    And User UID1 initiates the PASSCODE journey within the PASSCODE_STEP for authorisation and expects a status of JOURNEY_INITIATED

    Then Process the PASSCODE journey within the PASSCODE_STEP for user UID1 to authorise the user and expect a status JOURNEY_PROCESSED

    And User UID1 submits the PASSCODE journey within the PASSCODE_STEP for authorisation and expects a status of JOURNEY_SUCCESSFUL

    Then User UID1 submits the final user authorisation for ACTIVATE_CARD and expects a status of USER_AUTHORISATION_SUBMITTED

    And Get the final user authorisation token for ACTIVATE_CARD of user UID1 and expect a status USER_AUTHORISATION_SUCCESS

    Then I wait for 40 seconds

    Then I wait for credit card status as CARD_STATUS_UPGRADED to activate PHYSICAL card for user UID1

    Then I wait for 10 seconds

    Then User UID1 activates the CREDIT_CARD with valid token, with status 200

    Then User UID1 checks card status is CARD_STATUS_ACTIVE for CREDIT_CARD

#-----------------------------------------------------------------------------------------------------
    Then User UID1 initiates the initial user authorisation to SHOW_CARD_PIN and expects 200 as the status code and a status of USER_AUTHORISATION_SUCCESS

    Then User UID1 initiates the final user authorisation to SHOW_CARD_PIN and expects a user authorisation status of USER_AUTHORISATION_INITIATED

    And User UID1 initiates the PASSCODE journey within the PASSCODE_STEP for authorisation and expects a status of JOURNEY_INITIATED

    Then Process the PASSCODE journey within the PASSCODE_STEP for user UID1 to authorise the user and expect a status JOURNEY_PROCESSED

    And User UID1 submits the PASSCODE journey within the PASSCODE_STEP for authorisation and expects a status of JOURNEY_SUCCESSFUL

    Then User UID1 submits the final user authorisation for SHOW_CARD_PIN and expects a status of USER_AUTHORISATION_SUBMITTED

    And Get the final user authorisation token for SHOW_CARD_PIN of user UID1 and expect a status USER_AUTHORISATION_SUCCESS

    Then I view the credit card PIN for user UID1 and expect the PIN to be returned successfully


  Scenario: View Channel limits (POS,E_COMMERCE,ATM) -> Update Channel limits -> Verify updated limits -> Get Channel limits history
    #------------------------Ordering and activating card----------------------------
    Then I fetch credit card constants for HUGOBANK

    And I validate credit card eligibility using balance of the wallet with product code CASH_WALLET_CURRENT for user UID1
      | credit_limit  |
      | 20000         |

    Then User UID1 initiates the initial user authorisation to ORDER_CARD and expects 200 as the status code and a status of USER_AUTHORISATION_SUCCESS

    Then User UID1 initiates the final user authorisation to ORDER_CARD and expects a user authorisation status of USER_AUTHORISATION_INITIATED

    And User UID1 initiates the PASSCODE journey within the PASSCODE_STEP for authorisation and expects a status of JOURNEY_INITIATED

    Then Process the PASSCODE journey within the PASSCODE_STEP for user UID1 to authorise the user and expect a status JOURNEY_PROCESSED

    And User UID1 submits the PASSCODE journey within the PASSCODE_STEP for authorisation and expects a status of JOURNEY_SUCCESSFUL

    Then User UID1 submits the final user authorisation for ORDER_CARD and expects a status of USER_AUTHORISATION_SUBMITTED

    And Get the final user authorisation token for ORDER_CARD of user UID1 and expect a status USER_AUTHORISATION_SUCCESS

    Then I order a Physical Visa Credit Card as CREDIT_CARD for UID1 with card name as random_valid_choice and expect a status code of 200 and expect a card status of CARD_STATUS_PENDING
      | credit_limit  |
      | 20000         |

#---------------------Activating card----------------------------------------------------
    Then User UID1 initiates the initial user authorisation to ACTIVATE_CARD and expects 200 as the status code and a status of USER_AUTHORISATION_SUCCESS

    Then User UID1 initiates the final user authorisation to ACTIVATE_CARD and expects a user authorisation status of USER_AUTHORISATION_INITIATED

    And User UID1 initiates the PASSCODE journey within the PASSCODE_STEP for authorisation and expects a status of JOURNEY_INITIATED

    Then Process the PASSCODE journey within the PASSCODE_STEP for user UID1 to authorise the user and expect a status JOURNEY_PROCESSED

    And User UID1 submits the PASSCODE journey within the PASSCODE_STEP for authorisation and expects a status of JOURNEY_SUCCESSFUL

    Then User UID1 submits the final user authorisation for ACTIVATE_CARD and expects a status of USER_AUTHORISATION_SUBMITTED

    And Get the final user authorisation token for ACTIVATE_CARD of user UID1 and expect a status USER_AUTHORISATION_SUCCESS

    Then I wait for 40 seconds

    Then I wait for credit card status as CARD_STATUS_UPGRADED to activate PHYSICAL card for user UID1

    Then I wait for 10 seconds

    Then User UID1 activates the CREDIT_CARD with valid token, with status 200

    Then User UID1 checks card status is CARD_STATUS_ACTIVE for CREDIT_CARD

    Then I fetch credit account list for user UID1
#-----------------------------------------------------------------------------------------------------

#-----------------------------for changing limit of channels--------------------------
    Then I get card transaction channel limits for user UID1 and expect status code 200

#    ----------------------UPDATE LIMITS-------------------------------------------
    Then User UID1 initiates the initial user authorisation to UPDATE_CARD_LIMITS and expects 200 as the status code and a status of USER_AUTHORISATION_SUCCESS

    Then User UID1 initiates the final user authorisation to UPDATE_CARD_LIMITS and expects a user authorisation status of USER_AUTHORISATION_INITIATED

    And User UID1 initiates the PASSCODE journey within the PASSCODE_STEP for authorisation and expects a status of JOURNEY_INITIATED

    Then Process the PASSCODE journey within the PASSCODE_STEP for user UID1 to authorise the user and expect a status JOURNEY_PROCESSED

    And User UID1 submits the PASSCODE journey within the PASSCODE_STEP for authorisation and expects a status of JOURNEY_SUCCESSFUL

    Then User UID1 submits the final user authorisation for UPDATE_CARD_LIMITS and expects a status of USER_AUTHORISATION_SUBMITTED

    And Get the final user authorisation token for UPDATE_CARD_LIMITS of user UID1 and expect a status USER_AUTHORISATION_SUCCESS

    Then I update card limit for user UID1 and expect status code 200
      | limit_id        | value |
      | POS_DAILY_LIMIT | 5000  |

    Then I wait for 10 seconds

    And I verified the updated POS_DAILY_LIMIT limit for user UID1 and limit should be 5000

    # Transaction above limit value
    Given User performs the below transaction with CREDIT_CARD and expects a status code of 200
      | user_profile_identifier | transaction_permutation_name | billing_amount | is_foreign_txn | channel    |
      | UID1                    | AUTH_CLEAR                   | 6000           | false          | POS        |

    And I check the available credits for user UID1 and available credit should be 20000 exact

    # Transaction below limit value
    Given User performs the below transaction with CREDIT_CARD and expects a status code of 200
      | user_profile_identifier | transaction_permutation_name | billing_amount | is_foreign_txn | channel    |
      | UID1                    | AUTH_CLEAR                   | 3000           | false          | POS        |

    And I check the available credits for user UID1 and available credit should be 17000 exact

    Then I update card limit for user UID1 and expect status code 200
      | limit_id               | value |
      | E_COMMERCE_DAILY_LIMIT | 5000  |

    Then I wait for 10 seconds

    And I verified the updated E_COMMERCE_DAILY_LIMIT limit for user UID1 and limit should be 5000

   # Transaction above limit value
    Given User performs the below transaction with CREDIT_CARD and expects a status code of 200
      | user_profile_identifier | transaction_permutation_name | billing_amount | is_foreign_txn | channel    |
      | UID1                    | AUTH_CLEAR                   | 6000           | false          | E_COMMERCE |

    And I check the available credits for user UID1 and available credit should be 17000 exact

    # Transaction below limit value
    Given User performs the below transaction with CREDIT_CARD and expects a status code of 200
      | user_profile_identifier | transaction_permutation_name | billing_amount | is_foreign_txn | channel    |
      | UID1                    | AUTH_CLEAR                   | 3000           | false          | E_COMMERCE |

    And I check the available credits for user UID1 and available credit should be 14000 exact

    Then I update card limit for user UID1 and expect status code 200
      | limit_id               | value |
      | ATM_DAILY_LIMIT        | 5000  |

    Then I wait for 10 seconds

    And I verified the updated ATM_DAILY_LIMIT limit for user UID1 and limit should be 5000

   # Transaction above limit value
    Given User performs the below transaction with CREDIT_CARD and expects a status code of 200
      | user_profile_identifier | transaction_permutation_name | billing_amount | is_foreign_txn | channel    |
      | UID1                    | AUTH_CLEAR                   | 6000           | false          | ATM        |

    And I check the available credits for user UID1 and available credit should be 14000 exact

    # Transaction below limit value
    Given User performs the below transaction with CREDIT_CARD and expects a status code of 200
      | user_profile_identifier | transaction_permutation_name | billing_amount | is_foreign_txn | channel    |
      | UID1                    | AUTH_CLEAR                   | 3000           | false          | ATM        |

    And I check the available credits for user UID1 and available credit should be 9850 exact

    # GET limit history
    Then I get limit history for card for user UID1 and expect status code 200
      | limit_id        |
      | POS_DAILY_LIMIT |


  Scenario: Block channels -> transaction through blocked channel -> Un-Block channels -> transaction after unblocking
#------------------------Ordering and activating card-----------------------------------------
    Then I fetch credit card constants for HUGOBANK

    And I validate credit card eligibility using balance of the wallet with product code CASH_WALLET_CURRENT for user UID1
      | credit_limit  |
      | 20000         |

    Then User UID1 initiates the initial user authorisation to ORDER_CARD and expects 200 as the status code and a status of USER_AUTHORISATION_SUCCESS

    Then User UID1 initiates the final user authorisation to ORDER_CARD and expects a user authorisation status of USER_AUTHORISATION_INITIATED

    And User UID1 initiates the PASSCODE journey within the PASSCODE_STEP for authorisation and expects a status of JOURNEY_INITIATED

    Then Process the PASSCODE journey within the PASSCODE_STEP for user UID1 to authorise the user and expect a status JOURNEY_PROCESSED

    And User UID1 submits the PASSCODE journey within the PASSCODE_STEP for authorisation and expects a status of JOURNEY_SUCCESSFUL

    Then User UID1 submits the final user authorisation for ORDER_CARD and expects a status of USER_AUTHORISATION_SUBMITTED

    And Get the final user authorisation token for ORDER_CARD of user UID1 and expect a status USER_AUTHORISATION_SUCCESS

    Then I order a Physical Visa Credit Card as CREDIT_CARD for UID1 with card name as random_valid_choice and expect a status code of 200 and expect a card status of CARD_STATUS_PENDING
      | credit_limit  |
      | 20000         |

#---------------------Activating card----------------------------------------------------
    Then User UID1 initiates the initial user authorisation to ACTIVATE_CARD and expects 200 as the status code and a status of USER_AUTHORISATION_SUCCESS

    Then User UID1 initiates the final user authorisation to ACTIVATE_CARD and expects a user authorisation status of USER_AUTHORISATION_INITIATED

    And User UID1 initiates the PASSCODE journey within the PASSCODE_STEP for authorisation and expects a status of JOURNEY_INITIATED

    Then Process the PASSCODE journey within the PASSCODE_STEP for user UID1 to authorise the user and expect a status JOURNEY_PROCESSED

    And User UID1 submits the PASSCODE journey within the PASSCODE_STEP for authorisation and expects a status of JOURNEY_SUCCESSFUL

    Then User UID1 submits the final user authorisation for ACTIVATE_CARD and expects a status of USER_AUTHORISATION_SUBMITTED

    And Get the final user authorisation token for ACTIVATE_CARD of user UID1 and expect a status USER_AUTHORISATION_SUCCESS

    Then I wait for 40 seconds

    Then I wait for credit card status as CARD_STATUS_UPGRADED to activate PHYSICAL card for user UID1

    Then I wait for 10 seconds

    Then User UID1 activates the CREDIT_CARD with valid token, with status 200

    Then User UID1 checks card status is CARD_STATUS_ACTIVE for CREDIT_CARD

    Then I fetch credit account list for user UID1
#-----------------------------------------------------------------------------------------------------

    Then I get card transaction channel limits for user UID1 and expect status code 200

    Then User UID1 initiates the initial user authorisation to UPDATE_CARD_SETTINGS and expects 200 as the status code and a status of USER_AUTHORISATION_SUCCESS

    Then User UID1 initiates the final user authorisation to UPDATE_CARD_SETTINGS and expects a user authorisation status of USER_AUTHORISATION_INITIATED

    And User UID1 initiates the PASSCODE journey within the PASSCODE_STEP for authorisation and expects a status of JOURNEY_INITIATED

    Then Process the PASSCODE journey within the PASSCODE_STEP for user UID1 to authorise the user and expect a status JOURNEY_PROCESSED

    And User UID1 submits the PASSCODE journey within the PASSCODE_STEP for authorisation and expects a status of JOURNEY_SUCCESSFUL

    Then User UID1 submits the final user authorisation for UPDATE_CARD_SETTINGS and expects a status of USER_AUTHORISATION_SUBMITTED

    And Get the final user authorisation token for UPDATE_CARD_SETTINGS of user UID1 and expect a status USER_AUTHORISATION_SUCCESS

#    Then I block the Visa Physical Credit Card channel E_COMMERCE for user UID1
    Then User UID1 blocks the E_COMMERCE channel on CREDIT_CARD

    And I check status of Visa Physical Credit Card channel E_COMMERCE for UID1 and it should be DISABLED

    Given User performs the below transaction with CREDIT_CARD and expects a status code of 200
      | user_profile_identifier | transaction_permutation_name | billing_amount | is_foreign_txn | channel    |
      | UID1                    | AUTH_CLEAR                   | 3000           | false          | E_COMMERCE |

    And I check the available credits for user UID1 and available credit should be 20000 exact

#    Then I unblock the Visa Physical Credit Card channel E_COMMERCE for user UID1
    Then User UID1 unblocks the E_COMMERCE channel on CREDIT_CARD

    And I check status of Visa Physical Credit Card channel E_COMMERCE for UID1 and it should be ENABLED

    Given User performs the below transaction with CREDIT_CARD and expects a status code of 200
      | user_profile_identifier | transaction_permutation_name | billing_amount | is_foreign_txn | channel    |
      | UID1                    | AUTH_CLEAR                   | 3000           | false          | E_COMMERCE |

    And I check the available credits for user UID1 and available credit should be 17000 exact


  Scenario: View current credit limit -> Update credit limit -> Get updated limit
#------------------------Ordering and activating card-----------------------------------------
    Then I fetch credit card constants for HUGOBANK

    And I validate credit card eligibility using balance of the wallet with product code CASH_WALLET_CURRENT for user UID1
      | credit_limit  |
      | 20000         |

    Then User UID1 initiates the initial user authorisation to ORDER_CARD and expects 200 as the status code and a status of USER_AUTHORISATION_SUCCESS

    Then User UID1 initiates the final user authorisation to ORDER_CARD and expects a user authorisation status of USER_AUTHORISATION_INITIATED

    And User UID1 initiates the PASSCODE journey within the PASSCODE_STEP for authorisation and expects a status of JOURNEY_INITIATED

    Then Process the PASSCODE journey within the PASSCODE_STEP for user UID1 to authorise the user and expect a status JOURNEY_PROCESSED

    And User UID1 submits the PASSCODE journey within the PASSCODE_STEP for authorisation and expects a status of JOURNEY_SUCCESSFUL

    Then User UID1 submits the final user authorisation for ORDER_CARD and expects a status of USER_AUTHORISATION_SUBMITTED

    And Get the final user authorisation token for ORDER_CARD of user UID1 and expect a status USER_AUTHORISATION_SUCCESS

    Then I order a Physical Visa Credit Card as CREDIT_CARD for UID1 with card name as random_valid_choice and expect a status code of 200 and expect a card status of CARD_STATUS_PENDING
      | credit_limit  |
      | 20000         |

#---------------------Activating card----------------------------------------------------
    Then User UID1 initiates the initial user authorisation to ACTIVATE_CARD and expects 200 as the status code and a status of USER_AUTHORISATION_SUCCESS

    Then User UID1 initiates the final user authorisation to ACTIVATE_CARD and expects a user authorisation status of USER_AUTHORISATION_INITIATED

    And User UID1 initiates the PASSCODE journey within the PASSCODE_STEP for authorisation and expects a status of JOURNEY_INITIATED

    Then Process the PASSCODE journey within the PASSCODE_STEP for user UID1 to authorise the user and expect a status JOURNEY_PROCESSED

    And User UID1 submits the PASSCODE journey within the PASSCODE_STEP for authorisation and expects a status of JOURNEY_SUCCESSFUL

    Then User UID1 submits the final user authorisation for ACTIVATE_CARD and expects a status of USER_AUTHORISATION_SUBMITTED

    And Get the final user authorisation token for ACTIVATE_CARD of user UID1 and expect a status USER_AUTHORISATION_SUCCESS

    Then I wait for 40 seconds

    Then I wait for credit card status as CARD_STATUS_UPGRADED to activate PHYSICAL card for user UID1

    Then I wait for 10 seconds

    Then User UID1 activates the CREDIT_CARD with valid token, with status 200

    Then User UID1 checks card status is CARD_STATUS_ACTIVE for CREDIT_CARD

    Then I fetch credit account list for user UID1
#-----------------------------------------------------------------------------------------------------
    # Attempt to update credit limit when available balance < lien amount (should fail)
    Then User UID1 initiates the initial user authorisation to UPDATE_CREDIT_LIMIT and expects 200 as the status code and a status of USER_AUTHORISATION_SUCCESS

    Then User UID1 initiates the final user authorisation to UPDATE_CREDIT_LIMIT and expects a user authorisation status of USER_AUTHORISATION_INITIATED

    And User UID1 initiates the PASSCODE journey within the PASSCODE_STEP for authorisation and expects a status of JOURNEY_INITIATED

    Then Process the PASSCODE journey within the PASSCODE_STEP for user UID1 to authorise the user and expect a status JOURNEY_PROCESSED

    And User UID1 submits the PASSCODE journey within the PASSCODE_STEP for authorisation and expects a status of JOURNEY_SUCCESSFUL

    Then User UID1 submits the final user authorisation for UPDATE_CREDIT_LIMIT and expects a status of USER_AUTHORISATION_SUBMITTED

    And Get the final user authorisation token for UPDATE_CREDIT_LIMIT of user UID1 and expect a status USER_AUTHORISATION_SUCCESS

    Then I update credit limit for user UID1 and expect a status code of HSA_9145
      | credit_limit |
      | 80000        |

    Then I verified approved_limit for user UID1 and approved_limit should be 20000 PKR exact

    And Verify the balance of the wallet with product code CASH_WALLET_CURRENT for user UID1 and the balance should be 41000 PKR exact

#  Attempt to update credit limit when available balance >= lien amount (should pass)
    Then User UID1 initiates the initial user authorisation to UPDATE_CREDIT_LIMIT and expects 200 as the status code and a status of USER_AUTHORISATION_SUCCESS

    Then User UID1 initiates the final user authorisation to UPDATE_CREDIT_LIMIT and expects a user authorisation status of USER_AUTHORISATION_INITIATED

    And User UID1 initiates the PASSCODE journey within the PASSCODE_STEP for authorisation and expects a status of JOURNEY_INITIATED

    Then Process the PASSCODE journey within the PASSCODE_STEP for user UID1 to authorise the user and expect a status JOURNEY_PROCESSED

    And User UID1 submits the PASSCODE journey within the PASSCODE_STEP for authorisation and expects a status of JOURNEY_SUCCESSFUL

    Then User UID1 submits the final user authorisation for UPDATE_CREDIT_LIMIT and expects a status of USER_AUTHORISATION_SUBMITTED

    And Get the final user authorisation token for UPDATE_CREDIT_LIMIT of user UID1 and expect a status USER_AUTHORISATION_SUCCESS

    Then I update credit limit for user UID1 and expect a status code of 200
      | credit_limit |
      | 30000        |

    Then I wait for 40 seconds

    Then I verified approved_limit for user UID1 and approved_limit should be 30000 PKR exact

    And Verify the balance of the wallet with product code CASH_WALLET_CURRENT for user UID1 and the balance should be 26500 PKR exact

    Given User performs the below transaction with CREDIT_CARD and expects a status code of 200
      | user_profile_identifier | transaction_permutation_name | billing_amount | is_foreign_txn | channel    |
      | UID1                    | AUTH_CLEAR                   | 25000          | false          | E_COMMERCE |

    And I check the available credits for user UID1 and available credit should be 5000 approx

    Then I fetch credit account list for user UID1


  Scenario: Credit card cash advance scenario
    #------------------------Ordering and activating card-----------------------------------------
    Then I fetch credit card constants for HUGOBANK

    And I validate credit card eligibility using balance of the wallet with product code CASH_WALLET_CURRENT for user UID1
      | credit_limit  |
      | 20000         |

    Then User UID1 initiates the initial user authorisation to ORDER_CARD and expects 200 as the status code and a status of USER_AUTHORISATION_SUCCESS

    Then User UID1 initiates the final user authorisation to ORDER_CARD and expects a user authorisation status of USER_AUTHORISATION_INITIATED

    And User UID1 initiates the PASSCODE journey within the PASSCODE_STEP for authorisation and expects a status of JOURNEY_INITIATED

    Then Process the PASSCODE journey within the PASSCODE_STEP for user UID1 to authorise the user and expect a status JOURNEY_PROCESSED

    And User UID1 submits the PASSCODE journey within the PASSCODE_STEP for authorisation and expects a status of JOURNEY_SUCCESSFUL

    Then User UID1 submits the final user authorisation for ORDER_CARD and expects a status of USER_AUTHORISATION_SUBMITTED

    And Get the final user authorisation token for ORDER_CARD of user UID1 and expect a status USER_AUTHORISATION_SUCCESS

    Then I order a Physical Visa Credit Card as CREDIT_CARD for UID1 with card name as random_valid_choice and expect a status code of 200 and expect a card status of CARD_STATUS_PENDING
      | credit_limit  |
      | 20000         |

#---------------------Activating card----------------------------------------------------

    Then User UID1 initiates the initial user authorisation to ACTIVATE_CARD and expects 200 as the status code and a status of USER_AUTHORISATION_SUCCESS

    Then User UID1 initiates the final user authorisation to ACTIVATE_CARD and expects a user authorisation status of USER_AUTHORISATION_INITIATED

    And User UID1 initiates the PASSCODE journey within the PASSCODE_STEP for authorisation and expects a status of JOURNEY_INITIATED

    Then Process the PASSCODE journey within the PASSCODE_STEP for user UID1 to authorise the user and expect a status JOURNEY_PROCESSED

    And User UID1 submits the PASSCODE journey within the PASSCODE_STEP for authorisation and expects a status of JOURNEY_SUCCESSFUL

    Then User UID1 submits the final user authorisation for ACTIVATE_CARD and expects a status of USER_AUTHORISATION_SUBMITTED

    And Get the final user authorisation token for ACTIVATE_CARD of user UID1 and expect a status USER_AUTHORISATION_SUCCESS

    Then I wait for 40 seconds

    Then I wait for credit card status as CARD_STATUS_UPGRADED to activate PHYSICAL card for user UID1

    Then I wait for 10 seconds

    Then User UID1 activates the CREDIT_CARD with valid token, with status 200

    Then User UID1 checks card status is CARD_STATUS_ACTIVE for CREDIT_CARD

    Then I fetch credit account list for user UID1
#-----------------------------------------------------------------------------------------------------

    # Check current account balance and available credit before request
    And I check the available credits for user UID1 and available credit should be 20000 exact

    And Verify the balance of the wallet with product code CASH_WALLET_CURRENT for user UID1 and the balance should be 41000 PKR exact

    # Fetch cash advance limit for credit account
    Then I get cash advance limit for credit account of user UID1 and expect a status code of 200

    # Validate requested cash advance amount is within limit
    And I validate cash advance eligibility for user UID1
      | cash_advance_amount  |
      | 2000                 |

    # Authorisation for cash advance
    Then User UID1 initiates the initial user authorisation to REQUEST_CASH_ADVANCE and expects 200 as the status code and a status of USER_AUTHORISATION_SUCCESS

    Then User UID1 initiates the final user authorisation to REQUEST_CASH_ADVANCE and expects a user authorisation status of USER_AUTHORISATION_INITIATED

    And User UID1 initiates the PASSCODE journey within the PASSCODE_STEP for authorisation and expects a status of JOURNEY_INITIATED

    Then Process the PASSCODE journey within the PASSCODE_STEP for user UID1 to authorise the user and expect a status JOURNEY_PROCESSED

    And User UID1 submits the PASSCODE journey within the PASSCODE_STEP for authorisation and expects a status of JOURNEY_SUCCESSFUL

    Then User UID1 submits the final user authorisation for REQUEST_CASH_ADVANCE and expects a status of USER_AUTHORISATION_SUBMITTED

    And Get the final user authorisation token for REQUEST_CASH_ADVANCE of user UID1 and expect a status USER_AUTHORISATION_SUCCESS

    # Request cash advance
    Then I request cash advance for credit account of user UID1 and expect a status code of 200
      | cash_advance_amount |
      | 2000                |

    # Check current account balance and available credit after request
    And I check the available credits for user UID1 and available credit should be 16850 approx

    And Verify the balance of the wallet with product code CASH_WALLET_CURRENT for user UID1 and the balance should be 43000 PKR exact


  Scenario: Credit card bills related scenarios
    #------------------------Ordering and activating card-----------------------------------------
    Then I fetch credit card constants for HUGOBANK

    And I validate credit card eligibility using balance of the wallet with product code CASH_WALLET_CURRENT for user UID1
      | credit_limit  |
      | 20000         |

    Then User UID1 initiates the initial user authorisation to ORDER_CARD and expects 200 as the status code and a status of USER_AUTHORISATION_SUCCESS

    Then User UID1 initiates the final user authorisation to ORDER_CARD and expects a user authorisation status of USER_AUTHORISATION_INITIATED

    And User UID1 initiates the PASSCODE journey within the PASSCODE_STEP for authorisation and expects a status of JOURNEY_INITIATED

    Then Process the PASSCODE journey within the PASSCODE_STEP for user UID1 to authorise the user and expect a status JOURNEY_PROCESSED

    And User UID1 submits the PASSCODE journey within the PASSCODE_STEP for authorisation and expects a status of JOURNEY_SUCCESSFUL

    Then User UID1 submits the final user authorisation for ORDER_CARD and expects a status of USER_AUTHORISATION_SUBMITTED

    And Get the final user authorisation token for ORDER_CARD of user UID1 and expect a status USER_AUTHORISATION_SUCCESS

    Then I order a Physical Visa Credit Card as CREDIT_CARD for UID1 with card name as random_valid_choice and expect a status code of 200 and expect a card status of CARD_STATUS_PENDING
      | credit_limit  |
      | 20000         |

#---------------------Activating card----------------------------------------------------

    Then User UID1 initiates the initial user authorisation to ACTIVATE_CARD and expects 200 as the status code and a status of USER_AUTHORISATION_SUCCESS

    Then User UID1 initiates the final user authorisation to ACTIVATE_CARD and expects a user authorisation status of USER_AUTHORISATION_INITIATED

    And User UID1 initiates the PASSCODE journey within the PASSCODE_STEP for authorisation and expects a status of JOURNEY_INITIATED

    Then Process the PASSCODE journey within the PASSCODE_STEP for user UID1 to authorise the user and expect a status JOURNEY_PROCESSED

    And User UID1 submits the PASSCODE journey within the PASSCODE_STEP for authorisation and expects a status of JOURNEY_SUCCESSFUL

    Then User UID1 submits the final user authorisation for ACTIVATE_CARD and expects a status of USER_AUTHORISATION_SUBMITTED

    And Get the final user authorisation token for ACTIVATE_CARD of user UID1 and expect a status USER_AUTHORISATION_SUCCESS

    Then I wait for 40 seconds

    Then I wait for credit card status as CARD_STATUS_UPGRADED to activate PHYSICAL card for user UID1

    Then I wait for 10 seconds

    Then User UID1 activates the CREDIT_CARD with valid token, with status 200

    Then User UID1 checks card status is CARD_STATUS_ACTIVE for CREDIT_CARD

    Then I fetch credit account list for user UID1
#-----------------------------------------------------------------------------------------------------
# ---------------make some transaction to get due amount------------------
    Given User performs the below transaction with CREDIT_CARD and expects a status code of 200
      | user_profile_identifier | transaction_permutation_name | billing_amount | is_foreign_txn | channel    |
      | UID1                    | AUTH_CLEAR                   | 1000           | false          | E_COMMERCE |

    And I check the available credits for user UID1 and available credit should be 19000 exact

    Then I generate credit account bill for user UID1 and expect status code 200
#    Then I get the credit account bills for user UID1 and expect status code 200
#    Then I get the latest credit account bill for user UID1 and expect status code 200 and bill present as true
#    Then I get the latest credit account bill for user UID1 and expect status code 200 and bill present as false

    Then I pay credit account bill for user UID1 with amount 500 and expect status code 200 and intent status as PENDING

    Then I wait for 10 seconds

    And I check the available credits for user UID1 and available credit should be 19500 approx

    And Verify the balance of the wallet with product code CASH_WALLET_CURRENT for user UID1 and the balance should be 40500 PKR exact


  Scenario: User closes credit account using cash wallet
    #------------------------Ordering and activating card-----------------------------------------
    Then I fetch credit card constants for HUGOBANK

    And I validate credit card eligibility using balance of the wallet with product code CASH_WALLET_CURRENT for user UID1
      | credit_limit  |
      | 20000         |

    Then User UID1 initiates the initial user authorisation to ORDER_CARD and expects 200 as the status code and a status of USER_AUTHORISATION_SUCCESS

    Then User UID1 initiates the final user authorisation to ORDER_CARD and expects a user authorisation status of USER_AUTHORISATION_INITIATED

    And User UID1 initiates the PASSCODE journey within the PASSCODE_STEP for authorisation and expects a status of JOURNEY_INITIATED

    Then Process the PASSCODE journey within the PASSCODE_STEP for user UID1 to authorise the user and expect a status JOURNEY_PROCESSED

    And User UID1 submits the PASSCODE journey within the PASSCODE_STEP for authorisation and expects a status of JOURNEY_SUCCESSFUL

    Then User UID1 submits the final user authorisation for ORDER_CARD and expects a status of USER_AUTHORISATION_SUBMITTED

    And Get the final user authorisation token for ORDER_CARD of user UID1 and expect a status USER_AUTHORISATION_SUCCESS

    Then I order a Physical Visa Credit Card as CREDIT_CARD for UID1 with card name as random_valid_choice and expect a status code of 200 and expect a card status of CARD_STATUS_PENDING
      | credit_limit  |
      | 20000         |

#---------------------Activating card----------------------------------------------------

    Then User UID1 initiates the initial user authorisation to ACTIVATE_CARD and expects 200 as the status code and a status of USER_AUTHORISATION_SUCCESS

    Then User UID1 initiates the final user authorisation to ACTIVATE_CARD and expects a user authorisation status of USER_AUTHORISATION_INITIATED

    And User UID1 initiates the PASSCODE journey within the PASSCODE_STEP for authorisation and expects a status of JOURNEY_INITIATED

    Then Process the PASSCODE journey within the PASSCODE_STEP for user UID1 to authorise the user and expect a status JOURNEY_PROCESSED

    And User UID1 submits the PASSCODE journey within the PASSCODE_STEP for authorisation and expects a status of JOURNEY_SUCCESSFUL

    Then User UID1 submits the final user authorisation for ACTIVATE_CARD and expects a status of USER_AUTHORISATION_SUBMITTED

    And Get the final user authorisation token for ACTIVATE_CARD of user UID1 and expect a status USER_AUTHORISATION_SUCCESS

    Then I wait for 40 seconds

    Then I wait for credit card status as CARD_STATUS_UPGRADED to activate PHYSICAL card for user UID1

    Then I wait for 10 seconds

    Then User UID1 activates the CREDIT_CARD with valid token, with status 200

    Then User UID1 checks card status is CARD_STATUS_ACTIVE for CREDIT_CARD

    Then I fetch credit account list for user UID1
#-----------------------------------------------------------------------------------------------------
# ---------------make some transaction to get due amount------------------
    Given User performs the below transaction with CREDIT_CARD and expects a status code of 200
      | user_profile_identifier | transaction_permutation_name | billing_amount | is_foreign_txn | channel    |
      | UID1                    | AUTH_CLEAR                   | 1000           | false          | E_COMMERCE |

    And I check the available credits for user UID1 and available credit should be 19000 exact

#------------------------------close credit card-------------------------------------------
    Then User UID1 initiates the initial user authorisation to CLOSE_CREDIT_ACCOUNT and expects 200 as the status code and a status of USER_AUTHORISATION_SUCCESS

    Then User UID1 initiates the final user authorisation to CLOSE_CREDIT_ACCOUNT and expects a user authorisation status of USER_AUTHORISATION_INITIATED

    And User UID1 initiates the PASSCODE journey within the PASSCODE_STEP for authorisation and expects a status of JOURNEY_INITIATED

    Then Process the PASSCODE journey within the PASSCODE_STEP for user UID1 to authorise the user and expect a status JOURNEY_PROCESSED

    And User UID1 submits the PASSCODE journey within the PASSCODE_STEP for authorisation and expects a status of JOURNEY_SUCCESSFUL

    Then User UID1 submits the final user authorisation for CLOSE_CREDIT_ACCOUNT and expects a status of USER_AUTHORISATION_SUBMITTED

    And Get the final user authorisation token for CLOSE_CREDIT_ACCOUNT of user UID1 and expect a status USER_AUTHORISATION_SUCCESS

    Then I close credit account for user UID1 using settlement source SETTLEMENT_SOURCE_CASH_ACCOUNT and expect status code 200

    And I verify credit account is closed for user UID1


  Scenario: User closes credit account using lien amount
#------------------------Ordering and activating card-----------------------------------------
    Then I fetch credit card constants for HUGOBANK

    And I validate credit card eligibility using balance of the wallet with product code CASH_WALLET_CURRENT for user UID1
      | credit_limit  |
      | 20000         |

    Then User UID1 initiates the initial user authorisation to ORDER_CARD and expects 200 as the status code and a status of USER_AUTHORISATION_SUCCESS

    Then User UID1 initiates the final user authorisation to ORDER_CARD and expects a user authorisation status of USER_AUTHORISATION_INITIATED

    And User UID1 initiates the PASSCODE journey within the PASSCODE_STEP for authorisation and expects a status of JOURNEY_INITIATED

    Then Process the PASSCODE journey within the PASSCODE_STEP for user UID1 to authorise the user and expect a status JOURNEY_PROCESSED

    And User UID1 submits the PASSCODE journey within the PASSCODE_STEP for authorisation and expects a status of JOURNEY_SUCCESSFUL

    Then User UID1 submits the final user authorisation for ORDER_CARD and expects a status of USER_AUTHORISATION_SUBMITTED

    And Get the final user authorisation token for ORDER_CARD of user UID1 and expect a status USER_AUTHORISATION_SUCCESS

    Then I order a Physical Visa Credit Card as CREDIT_CARD for UID1 with card name as random_valid_choice and expect a status code of 200 and expect a card status of CARD_STATUS_PENDING
      | credit_limit  |
      | 20000         |

#---------------------Activating card----------------------------------------------------

    Then User UID1 initiates the initial user authorisation to ACTIVATE_CARD and expects 200 as the status code and a status of USER_AUTHORISATION_SUCCESS

    Then User UID1 initiates the final user authorisation to ACTIVATE_CARD and expects a user authorisation status of USER_AUTHORISATION_INITIATED

    And User UID1 initiates the PASSCODE journey within the PASSCODE_STEP for authorisation and expects a status of JOURNEY_INITIATED

    Then Process the PASSCODE journey within the PASSCODE_STEP for user UID1 to authorise the user and expect a status JOURNEY_PROCESSED

    And User UID1 submits the PASSCODE journey within the PASSCODE_STEP for authorisation and expects a status of JOURNEY_SUCCESSFUL

    Then User UID1 submits the final user authorisation for ACTIVATE_CARD and expects a status of USER_AUTHORISATION_SUBMITTED

    And Get the final user authorisation token for ACTIVATE_CARD of user UID1 and expect a status USER_AUTHORISATION_SUCCESS

    Then I wait for 40 seconds

    Then I wait for credit card status as CARD_STATUS_UPGRADED to activate PHYSICAL card for user UID1

    Then I wait for 10 seconds

    Then User UID1 activates the CREDIT_CARD with valid token, with status 200

    Then User UID1 checks card status is CARD_STATUS_ACTIVE for CREDIT_CARD

    Then I fetch credit account list for user UID1
#-----------------------------------------------------------------------------------------------------
# ---------------make some transaction to get due amount------------------
    Given User performs the below transaction with CREDIT_CARD and expects a status code of 200
      | user_profile_identifier | transaction_permutation_name | billing_amount | is_foreign_txn | channel    |
      | UID1                    | AUTH_CLEAR                   | 1000           | false          | E_COMMERCE |

    And I check the available credits for user UID1 and available credit should be 19000 exact

#------------------------------close credit card-------------------------------------------
    Then User UID1 initiates the initial user authorisation to CLOSE_CREDIT_ACCOUNT and expects 200 as the status code and a status of USER_AUTHORISATION_SUCCESS

    Then User UID1 initiates the final user authorisation to CLOSE_CREDIT_ACCOUNT and expects a user authorisation status of USER_AUTHORISATION_INITIATED

    And User UID1 initiates the PASSCODE journey within the PASSCODE_STEP for authorisation and expects a status of JOURNEY_INITIATED

    Then Process the PASSCODE journey within the PASSCODE_STEP for user UID1 to authorise the user and expect a status JOURNEY_PROCESSED

    And User UID1 submits the PASSCODE journey within the PASSCODE_STEP for authorisation and expects a status of JOURNEY_SUCCESSFUL

    Then User UID1 submits the final user authorisation for CLOSE_CREDIT_ACCOUNT and expects a status of USER_AUTHORISATION_SUBMITTED

    And Get the final user authorisation token for CLOSE_CREDIT_ACCOUNT of user UID1 and expect a status USER_AUTHORISATION_SUCCESS

    Then I close credit account for user UID1 using settlement source SETTLEMENT_SOURCE_LIEN and expect status code 200

    And I verify credit account is closed for user UID1


  Scenario: Replace Physical Secured Credit Card and verify financial integrity
    #------------------------Ordering and activating card-----------------------------------------
    Then I fetch credit card constants for HUGOBANK

    And I validate credit card eligibility using balance of the wallet with product code CASH_WALLET_CURRENT for user UID1
      | credit_limit  |
      | 20000         |

    Then User UID1 initiates the initial user authorisation to ORDER_CARD and expects 200 as the status code and a status of USER_AUTHORISATION_SUCCESS

    Then User UID1 initiates the final user authorisation to ORDER_CARD and expects a user authorisation status of USER_AUTHORISATION_INITIATED

    And User UID1 initiates the PASSCODE journey within the PASSCODE_STEP for authorisation and expects a status of JOURNEY_INITIATED

    Then Process the PASSCODE journey within the PASSCODE_STEP for user UID1 to authorise the user and expect a status JOURNEY_PROCESSED

    And User UID1 submits the PASSCODE journey within the PASSCODE_STEP for authorisation and expects a status of JOURNEY_SUCCESSFUL

    Then User UID1 submits the final user authorisation for ORDER_CARD and expects a status of USER_AUTHORISATION_SUBMITTED

    And Get the final user authorisation token for ORDER_CARD of user UID1 and expect a status USER_AUTHORISATION_SUCCESS

    Then I order a Physical Visa Credit Card as CREDIT_CARD for UID1 with card name as random_valid_choice and expect a status code of 200 and expect a card status of CARD_STATUS_PENDING
      | credit_limit  |
      | 20000         |

#---------------------Activating card----------------------------------------------------

    Then User UID1 initiates the initial user authorisation to ACTIVATE_CARD and expects 200 as the status code and a status of USER_AUTHORISATION_SUCCESS

    Then User UID1 initiates the final user authorisation to ACTIVATE_CARD and expects a user authorisation status of USER_AUTHORISATION_INITIATED

    And User UID1 initiates the PASSCODE journey within the PASSCODE_STEP for authorisation and expects a status of JOURNEY_INITIATED

    Then Process the PASSCODE journey within the PASSCODE_STEP for user UID1 to authorise the user and expect a status JOURNEY_PROCESSED

    And User UID1 submits the PASSCODE journey within the PASSCODE_STEP for authorisation and expects a status of JOURNEY_SUCCESSFUL

    Then User UID1 submits the final user authorisation for ACTIVATE_CARD and expects a status of USER_AUTHORISATION_SUBMITTED

    And Get the final user authorisation token for ACTIVATE_CARD of user UID1 and expect a status USER_AUTHORISATION_SUCCESS

    Then I wait for 40 seconds

    Then I wait for credit card status as CARD_STATUS_UPGRADED to activate PHYSICAL card for user UID1

    Then I wait for 10 seconds

    Then User UID1 activates the CREDIT_CARD with valid token, with status 200

    Then User UID1 checks card status is CARD_STATUS_ACTIVE for CREDIT_CARD

    Then I fetch credit account list for user UID1
#-----------------------------------------------------------------------------------------------------
    And I fetch credit account balance for user UID1

    # Store snapshot before replacement
    And I store credit card replacement details for user UID1

    Then User UID1 initiates the initial user authorisation to REPLACE_CARD and expects 200 as the status code and a status of USER_AUTHORISATION_SUCCESS

    Then User UID1 initiates the final user authorisation to REPLACE_CARD and expects a user authorisation status of USER_AUTHORISATION_INITIATED

    And User UID1 initiates the PASSCODE journey within the PASSCODE_STEP for authorisation and expects a status of JOURNEY_INITIATED

    Then Process the PASSCODE journey within the PASSCODE_STEP for user UID1 to authorise the user and expect a status JOURNEY_PROCESSED

    And User UID1 submits the PASSCODE journey within the PASSCODE_STEP for authorisation and expects a status of JOURNEY_SUCCESSFUL

    Then User UID1 submits the final user authorisation for REPLACE_CARD and expects a status of USER_AUTHORISATION_SUBMITTED

    And Get the final user authorisation token for REPLACE_CARD of user UID1 and expect a status USER_AUTHORISATION_SUCCESS

    Then I replace Physical credit card for user UID1 and expect a card status of CARD_STATUS_PENDING

    Then I check old card status is CARD_STATUS_DISABLED for user UID1

    Then I fetch credit account list for user UID1

    And I fetch credit account balance for user UID1

    And I verify credit account integrity after replacement for user UID1


#######################Scenario outline##########################################################
  Scenario Outline: View Channel limits (POS,E_COMMERCE,ATM) -> Update Channel limits -> Verify updated limits

    #------------------------Ordering and activating card----------------------------
    Then I fetch credit card constants for HUGOBANK

    And I validate credit card eligibility using balance of the wallet with product code CASH_WALLET_CURRENT for user UID1
      | credit_limit  |
      | 20000         |

    Then User UID1 initiates the initial user authorisation to ORDER_CARD and expects 200 as the status code and a status of USER_AUTHORISATION_SUCCESS

    Then User UID1 initiates the final user authorisation to ORDER_CARD and expects a user authorisation status of USER_AUTHORISATION_INITIATED

    And User UID1 initiates the PASSCODE journey within the PASSCODE_STEP for authorisation and expects a status of JOURNEY_INITIATED

    Then Process the PASSCODE journey within the PASSCODE_STEP for user UID1 to authorise the user and expect a status JOURNEY_PROCESSED

    And User UID1 submits the PASSCODE journey within the PASSCODE_STEP for authorisation and expects a status of JOURNEY_SUCCESSFUL

    Then User UID1 submits the final user authorisation for ORDER_CARD and expects a status of USER_AUTHORISATION_SUBMITTED

    And Get the final user authorisation token for ORDER_CARD of user UID1 and expect a status USER_AUTHORISATION_SUCCESS

    Then I order a Physical Visa Credit Card as CREDIT_CARD for UID1 with card name as random_valid_choice and expect a status code of 200 and expect a card status of CARD_STATUS_PENDING
      | credit_limit  |
      | 20000         |

#---------------------Activating card----------------------------------------------------

    Then User UID1 initiates the initial user authorisation to ACTIVATE_CARD and expects 200 as the status code and a status of USER_AUTHORISATION_SUCCESS

    Then User UID1 initiates the final user authorisation to ACTIVATE_CARD and expects a user authorisation status of USER_AUTHORISATION_INITIATED

    And User UID1 initiates the PASSCODE journey within the PASSCODE_STEP for authorisation and expects a status of JOURNEY_INITIATED

    Then Process the PASSCODE journey within the PASSCODE_STEP for user UID1 to authorise the user and expect a status JOURNEY_PROCESSED

    And User UID1 submits the PASSCODE journey within the PASSCODE_STEP for authorisation and expects a status of JOURNEY_SUCCESSFUL

    Then User UID1 submits the final user authorisation for ACTIVATE_CARD and expects a status of USER_AUTHORISATION_SUBMITTED

    And Get the final user authorisation token for ACTIVATE_CARD of user UID1 and expect a status USER_AUTHORISATION_SUCCESS

    Then I wait for 40 seconds

    Then I wait for credit card status as CARD_STATUS_UPGRADED to activate PHYSICAL card for user UID1

    Then I wait for 10 seconds

    Then User UID1 activates the CREDIT_CARD with valid token, with status 200

    Then User UID1 checks card status is CARD_STATUS_ACTIVE for CREDIT_CARD

    Then I fetch credit account list for user UID1
#-----------------------------------------------------------------------------------------------------

    Then I get card transaction channel limits for user UID1 and expect status code 200

  # Authorisation for limit update
    Then User UID1 initiates the initial user authorisation to UPDATE_CARD_LIMITS and expects 200 as the status code and a status of USER_AUTHORISATION_SUCCESS

    Then User UID1 initiates the final user authorisation to UPDATE_CARD_LIMITS and expects a user authorisation status of USER_AUTHORISATION_INITIATED

    And User UID1 initiates the PASSCODE journey within the PASSCODE_STEP for authorisation and expects a status of JOURNEY_INITIATED

    Then Process the PASSCODE journey within the PASSCODE_STEP for user UID1 to authorise the user and expect a status JOURNEY_PROCESSED

    And User UID1 submits the PASSCODE journey within the PASSCODE_STEP for authorisation and expects a status of JOURNEY_SUCCESSFUL

    Then User UID1 submits the final user authorisation for UPDATE_CARD_LIMITS and expects a status of USER_AUTHORISATION_SUBMITTED

    And Get the final user authorisation token for UPDATE_CARD_LIMITS of user UID1 and expect a status USER_AUTHORISATION_SUCCESS


  # Update limit
    Then I update <limit_id> to <limit_value> for user UID1 and expect status code 200
    And I verify <limit_id> limit for user UID1 should be <limit_value>

  # Transaction above limit
    Given User performs the below transaction with CREDIT_CARD and expects a status code of 200
      | user_profile_identifier | transaction_permutation_name | billing_amount | is_foreign_txn | channel       |
      | UID1                    | AUTH_CLEAR                   | <above_amount> | false          | <channel>     |

    Then I check available credit for user UID1 should be <credit_after_above>

  # Transaction below limit
    Given User performs the below transaction with CREDIT_CARD and expects a status code of 200
      | user_profile_identifier | transaction_permutation_name | billing_amount | is_foreign_txn | channel       |
      | UID1                    | AUTH_CLEAR                   | <below_amount> | false          | <channel>     |

    Then I check available credit for user UID1 should be <credit_after_below>

    Examples:
      | limit_id               | limit_value | channel      | above_amount | below_amount | credit_after_above | credit_after_below |
      | POS_DAILY_LIMIT        | 5000        | POS          | 6000         | 3000         | 20000              | 17000              |
      | E_COMMERCE_DAILY_LIMIT | 5000        | E_COMMERCE   | 6000         | 3000         | 20000              | 17000              |
      | ATM_DAILY_LIMIT        | 5000        | ATM          | 6000         | 3000         | 20000              | 15850              |


