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

    Then User fetch credit card constants for HUGOBANK

    And Validate credit card eligibility using balance of the wallet with product code CASH_WALLET_CURRENT for user UID1
      | credit_limit  |
      | 20000         |

    Then User UID1 initiates the initial user authorisation to ORDER_CARD and expects 200 as the status code and a status of USER_AUTHORISATION_SUCCESS

    Then User UID1 initiates the final user authorisation to ORDER_CARD and expects a user authorisation status of USER_AUTHORISATION_INITIATED

    And User UID1 initiates the PASSCODE journey within the PASSCODE_STEP for authorisation and expects a status of JOURNEY_INITIATED

    Then Process the PASSCODE journey within the PASSCODE_STEP for user UID1 to authorise the user and expect a status JOURNEY_PROCESSED

    And User UID1 submits the PASSCODE journey within the PASSCODE_STEP for authorisation and expects a status of JOURNEY_SUCCESSFUL

    Then User UID1 submits the final user authorisation for ORDER_CARD and expects a status of USER_AUTHORISATION_SUBMITTED

    And Get the final user authorisation token for ORDER_CARD of user UID1 and expect a status USER_AUTHORISATION_SUCCESS

    Then User order a Physical Visa Credit Card as CREDIT_CARD for UID1 with card name as random_valid_choice and expect a status code of 200 and expect a card status of CARD_STATUS_PENDING
      | credit_limit  |
      | 20000         |

#--------------------------------Activation and other steps------------------------------------------------------

    Then User UID1 fetch credit account list
    #------------------------------------Transaction without activation------------------------------------------------

    Given User performs the below transaction with CREDIT_CARD and expects a status code of 200
      | user_profile_identifier | transaction_permutation_name | billing_amount | is_foreign_txn | channel    |
      | UID1                    | AUTH_CLEAR                   | 500            | false          | POS        |

    And Check the available credits for user UID1 and available credit should be 19500 approx

    Given User performs the below transaction with CREDIT_CARD and expects a status code of 200
      | user_profile_identifier | transaction_permutation_name | billing_amount | is_foreign_txn | channel    |
      | UID1                    | AUTH_CLEAR                   | 500            | false          | E_COMMERCE |

    And Check the available credits for user UID1 and available credit should be 19000 approx

#    # ATM transaction — should fail
    Given User performs the below transaction with CREDIT_CARD and expects a status code of HSA_9121
      | user_profile_identifier | transaction_permutation_name | billing_amount | is_foreign_txn | channel    |
      | UID1                    | AUTH_CLEAR                   | 500            | false          | ATM        |

    And Check the available credits for user UID1 and available credit should be 19000 approx

#-------------------------------------Transaction after activation------------------------------------------------

    Then User UID1 initiates the initial user authorisation to ACTIVATE_CARD and expects 200 as the status code and a status of USER_AUTHORISATION_SUCCESS

    Then User UID1 initiates the final user authorisation to ACTIVATE_CARD and expects a user authorisation status of USER_AUTHORISATION_INITIATED

    And User UID1 initiates the PASSCODE journey within the PASSCODE_STEP for authorisation and expects a status of JOURNEY_INITIATED

    Then Process the PASSCODE journey within the PASSCODE_STEP for user UID1 to authorise the user and expect a status JOURNEY_PROCESSED

    And User UID1 submits the PASSCODE journey within the PASSCODE_STEP for authorisation and expects a status of JOURNEY_SUCCESSFUL

    Then User UID1 submits the final user authorisation for ACTIVATE_CARD and expects a status of USER_AUTHORISATION_SUBMITTED

    And Get the final user authorisation token for ACTIVATE_CARD of user UID1 and expect a status USER_AUTHORISATION_SUCCESS

    Then I wait for 40 seconds

    Then Wait for credit card status as CARD_STATUS_UPGRADED to activate PHYSICAL card for user UID1

    Then I wait for 10 seconds

    Then User UID1 activates the CREDIT_CARD with valid token, with status 200

    Then User UID1 checks card status is CARD_STATUS_ACTIVE for CREDIT_CARD

    Given User performs the below transaction with CREDIT_CARD and expects a status code of 200
      | user_profile_identifier | transaction_permutation_name | billing_amount | is_foreign_txn | channel    |
      | UID1                    | AUTH_CLEAR                   | 500            | false          | POS        |

    And Check the available credits for user UID1 and available credit should be 18500 approx

    Given User performs the below transaction with CREDIT_CARD and expects a status code of 200
      | user_profile_identifier | transaction_permutation_name | billing_amount | is_foreign_txn | channel    |
      | UID1                    | AUTH_CLEAR                   | 500            | false          | E_COMMERCE |

    And Check the available credits for user UID1 and available credit should be 18000 approx

    Given User performs the below transaction with CREDIT_CARD and expects a status code of 200
      | user_profile_identifier | transaction_permutation_name | billing_amount | is_foreign_txn | channel    |
      | UID1                    | AUTH_CLEAR                   | 500            | false          | ATM        |

    And Check the available credits for user UID1 and available credit should be 16350 approx


  Scenario: Credit card order -> Activate -> Block -> Unblock -> Disable
#---------------------Ordering card----------------------------------------------------
    Then User fetch credit card constants for HUGOBANK

    And Validate credit card eligibility using balance of the wallet with product code CASH_WALLET_CURRENT for user UID1
      | credit_limit  |
      | 20000         |

    Then User UID1 initiates the initial user authorisation to ORDER_CARD and expects 200 as the status code and a status of USER_AUTHORISATION_SUCCESS

    Then User UID1 initiates the final user authorisation to ORDER_CARD and expects a user authorisation status of USER_AUTHORISATION_INITIATED

    And User UID1 initiates the PASSCODE journey within the PASSCODE_STEP for authorisation and expects a status of JOURNEY_INITIATED

    Then Process the PASSCODE journey within the PASSCODE_STEP for user UID1 to authorise the user and expect a status JOURNEY_PROCESSED

    And User UID1 submits the PASSCODE journey within the PASSCODE_STEP for authorisation and expects a status of JOURNEY_SUCCESSFUL

    Then User UID1 submits the final user authorisation for ORDER_CARD and expects a status of USER_AUTHORISATION_SUBMITTED

    And Get the final user authorisation token for ORDER_CARD of user UID1 and expect a status USER_AUTHORISATION_SUCCESS

    Then User order a Physical Visa Credit Card as CREDIT_CARD for UID1 with card name as random_valid_choice and expect a status code of 200 and expect a card status of CARD_STATUS_PENDING
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

    Then Wait for credit card status as CARD_STATUS_UPGRADED to activate PHYSICAL card for user UID1

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
    Then User fetch credit card constants for HUGOBANK

    Then User UID1 initiates the initial user authorisation to ORDER_CARD and expects 200 as the status code and a status of USER_AUTHORISATION_SUCCESS

    Then User UID1 initiates the final user authorisation to ORDER_CARD and expects a user authorisation status of USER_AUTHORISATION_INITIATED

    And User UID1 initiates the PASSCODE journey within the PASSCODE_STEP for authorisation and expects a status of JOURNEY_INITIATED

    Then Process the PASSCODE journey within the PASSCODE_STEP for user UID1 to authorise the user and expect a status JOURNEY_PROCESSED

    And User UID1 submits the PASSCODE journey within the PASSCODE_STEP for authorisation and expects a status of JOURNEY_SUCCESSFUL

    Then User UID1 submits the final user authorisation for ORDER_CARD and expects a status of USER_AUTHORISATION_SUBMITTED

    And Get the final user authorisation token for ORDER_CARD of user UID1 and expect a status USER_AUTHORISATION_SUCCESS

    Then User order a Physical Visa Credit Card as CREDIT_CARD for UID1 with card name as random_valid_choice and expect a status code of 200 and expect a card status of CARD_STATUS_PENDING
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

    Then Wait for credit card status as CARD_STATUS_UPGRADED to activate PHYSICAL card for user UID1

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

    Then User UID1 view the credit card PIN and expect the PIN to be returned successfully


  Scenario: View Channel limits (POS,E_COMMERCE,ATM) -> Update Channel limits -> Verify updated limits -> Get Channel limits history
    #------------------------Ordering and activating card----------------------------
    Then User fetch credit card constants for HUGOBANK

    Then User UID1 initiates the initial user authorisation to ORDER_CARD and expects 200 as the status code and a status of USER_AUTHORISATION_SUCCESS

    Then User UID1 initiates the final user authorisation to ORDER_CARD and expects a user authorisation status of USER_AUTHORISATION_INITIATED

    And User UID1 initiates the PASSCODE journey within the PASSCODE_STEP for authorisation and expects a status of JOURNEY_INITIATED

    Then Process the PASSCODE journey within the PASSCODE_STEP for user UID1 to authorise the user and expect a status JOURNEY_PROCESSED

    And User UID1 submits the PASSCODE journey within the PASSCODE_STEP for authorisation and expects a status of JOURNEY_SUCCESSFUL

    Then User UID1 submits the final user authorisation for ORDER_CARD and expects a status of USER_AUTHORISATION_SUBMITTED

    And Get the final user authorisation token for ORDER_CARD of user UID1 and expect a status USER_AUTHORISATION_SUCCESS

    Then User order a Physical Visa Credit Card as CREDIT_CARD for UID1 with card name as random_valid_choice and expect a status code of 200 and expect a card status of CARD_STATUS_PENDING
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

    Then Wait for credit card status as CARD_STATUS_UPGRADED to activate PHYSICAL card for user UID1

    Then User UID1 activates the CREDIT_CARD with valid token, with status 200

    Then User UID1 checks card status is CARD_STATUS_ACTIVE for CREDIT_CARD

    Then User UID1 fetch credit account list
#-----------------------------------------------------------------------------------------------------

#-----------------------------for changing limit of channels--------------------------
    Then User UID1 get card transaction channel limits and expect status code 200

#    ----------------------UPDATE LIMITS-------------------------------------------
    Then User UID1 initiates the initial user authorisation to UPDATE_CARD_LIMITS and expects 200 as the status code and a status of USER_AUTHORISATION_SUCCESS

    Then User UID1 initiates the final user authorisation to UPDATE_CARD_LIMITS and expects a user authorisation status of USER_AUTHORISATION_INITIATED

    And User UID1 initiates the PASSCODE journey within the PASSCODE_STEP for authorisation and expects a status of JOURNEY_INITIATED

    Then Process the PASSCODE journey within the PASSCODE_STEP for user UID1 to authorise the user and expect a status JOURNEY_PROCESSED

    And User UID1 submits the PASSCODE journey within the PASSCODE_STEP for authorisation and expects a status of JOURNEY_SUCCESSFUL

    Then User UID1 submits the final user authorisation for UPDATE_CARD_LIMITS and expects a status of USER_AUTHORISATION_SUBMITTED

    And Get the final user authorisation token for UPDATE_CARD_LIMITS of user UID1 and expect a status USER_AUTHORISATION_SUCCESS

    Then User UID1 update card channel limit and expect status code 200
      | limit_id        | value |
      | POS_DAILY_LIMIT | 5000  |


    And User UID1 verified the updated POS_DAILY_LIMIT limit and limit should be 5000

    # Transaction above limit value
    Given User performs the below transaction with CREDIT_CARD and expects a status code of 200
      | user_profile_identifier | transaction_permutation_name | billing_amount | is_foreign_txn | channel    |
      | UID1                    | AUTH_CLEAR                   | 6000           | false          | POS        |

    And Check the available credits for user UID1 and available credit should be 20000 exact

    # Transaction below limit value
    Given User performs the below transaction with CREDIT_CARD and expects a status code of 200
      | user_profile_identifier | transaction_permutation_name | billing_amount | is_foreign_txn | channel    |
      | UID1                    | AUTH_CLEAR                   | 3000           | false          | POS        |

    And Check the available credits for user UID1 and available credit should be 17000 exact

    Then User UID1 update card channel limit and expect status code 200
      | limit_id               | value |
      | E_COMMERCE_DAILY_LIMIT | 5000  |

#    Then I wait for 10 seconds

    And User UID1 verified the updated E_COMMERCE_DAILY_LIMIT limit and limit should be 5000

   # Transaction above limit value
    Given User performs the below transaction with CREDIT_CARD and expects a status code of 200
      | user_profile_identifier | transaction_permutation_name | billing_amount | is_foreign_txn | channel    |
      | UID1                    | AUTH_CLEAR                   | 6000           | false          | E_COMMERCE |

    And Check the available credits for user UID1 and available credit should be 17000 exact

    # Transaction below limit value
    Given User performs the below transaction with CREDIT_CARD and expects a status code of 200
      | user_profile_identifier | transaction_permutation_name | billing_amount | is_foreign_txn | channel    |
      | UID1                    | AUTH_CLEAR                   | 3000           | false          | E_COMMERCE |

    And Check the available credits for user UID1 and available credit should be 14000 exact

    Then User UID1 update card channel limit and expect status code 200
      | limit_id               | value |
      | ATM_DAILY_LIMIT        | 5000  |


    And User UID1 verified the updated ATM_DAILY_LIMIT limit and limit should be 5000

   # Transaction above limit value
    Given User performs the below transaction with CREDIT_CARD and expects a status code of 200
      | user_profile_identifier | transaction_permutation_name | billing_amount | is_foreign_txn | channel    |
      | UID1                    | AUTH_CLEAR                   | 6000           | false          | ATM        |

    And Check the available credits for user UID1 and available credit should be 14000 exact

    # Transaction below limit value
    Given User performs the below transaction with CREDIT_CARD and expects a status code of 200
      | user_profile_identifier | transaction_permutation_name | billing_amount | is_foreign_txn | channel    |
      | UID1                    | AUTH_CLEAR                   | 3000           | false          | ATM        |

    And Check the available credits for user UID1 and available credit should be 9850 exact

    # GET limit history
    Then User UID1 get channel limit history for credit card and expect status code 200
      | limit_id        |
      | POS_DAILY_LIMIT |


  Scenario: Block channels -> transaction through blocked channel -> Un-Block channels -> transaction after unblocking
#------------------------Ordering and activating card-----------------------------------------
    Then User fetch credit card constants for HUGOBANK

    Then User UID1 initiates the initial user authorisation to ORDER_CARD and expects 200 as the status code and a status of USER_AUTHORISATION_SUCCESS

    Then User UID1 initiates the final user authorisation to ORDER_CARD and expects a user authorisation status of USER_AUTHORISATION_INITIATED

    And User UID1 initiates the PASSCODE journey within the PASSCODE_STEP for authorisation and expects a status of JOURNEY_INITIATED

    Then Process the PASSCODE journey within the PASSCODE_STEP for user UID1 to authorise the user and expect a status JOURNEY_PROCESSED

    And User UID1 submits the PASSCODE journey within the PASSCODE_STEP for authorisation and expects a status of JOURNEY_SUCCESSFUL

    Then User UID1 submits the final user authorisation for ORDER_CARD and expects a status of USER_AUTHORISATION_SUBMITTED

    And Get the final user authorisation token for ORDER_CARD of user UID1 and expect a status USER_AUTHORISATION_SUCCESS

    Then User order a Physical Visa Credit Card as CREDIT_CARD for UID1 with card name as random_valid_choice and expect a status code of 200 and expect a card status of CARD_STATUS_PENDING
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

    Then Wait for credit card status as CARD_STATUS_UPGRADED to activate PHYSICAL card for user UID1

    Then User UID1 activates the CREDIT_CARD with valid token, with status 200

    Then User UID1 checks card status is CARD_STATUS_ACTIVE for CREDIT_CARD

    Then User UID1 fetch credit account list
#-----------------------------------------------------------------------------------------------------

    Then User UID1 get card transaction channel limits and expect status code 200

    Then User UID1 initiates the initial user authorisation to UPDATE_CARD_SETTINGS and expects 200 as the status code and a status of USER_AUTHORISATION_SUCCESS

    Then User UID1 initiates the final user authorisation to UPDATE_CARD_SETTINGS and expects a user authorisation status of USER_AUTHORISATION_INITIATED

    And User UID1 initiates the PASSCODE journey within the PASSCODE_STEP for authorisation and expects a status of JOURNEY_INITIATED

    Then Process the PASSCODE journey within the PASSCODE_STEP for user UID1 to authorise the user and expect a status JOURNEY_PROCESSED

    And User UID1 submits the PASSCODE journey within the PASSCODE_STEP for authorisation and expects a status of JOURNEY_SUCCESSFUL

    Then User UID1 submits the final user authorisation for UPDATE_CARD_SETTINGS and expects a status of USER_AUTHORISATION_SUBMITTED

    And Get the final user authorisation token for UPDATE_CARD_SETTINGS of user UID1 and expect a status USER_AUTHORISATION_SUCCESS

    Then User UID1 blocks the E_COMMERCE channel on CREDIT_CARD

    And User UID1 check status of Visa Physical Credit Card for channel E_COMMERCE and it should be DISABLED

    Given User performs the below transaction with CREDIT_CARD and expects a status code of 200
      | user_profile_identifier | transaction_permutation_name | billing_amount | is_foreign_txn | channel    |
      | UID1                    | AUTH_CLEAR                   | 3000           | false          | E_COMMERCE |

    And Check the available credits for user UID1 and available credit should be 20000 exact

    Then User UID1 unblocks the E_COMMERCE channel on CREDIT_CARD

    And User UID1 check status of Visa Physical Credit Card for channel E_COMMERCE and it should be ENABLED

    Given User performs the below transaction with CREDIT_CARD and expects a status code of 200
      | user_profile_identifier | transaction_permutation_name | billing_amount | is_foreign_txn | channel    |
      | UID1                    | AUTH_CLEAR                   | 3000           | false          | E_COMMERCE |

    And Check the available credits for user UID1 and available credit should be 17000 exact


  Scenario: View current credit limit -> Update credit limit -> Get updated limit
#------------------------Ordering and activating card-----------------------------------------
    Then User fetch credit card constants for HUGOBANK

    Then User UID1 initiates the initial user authorisation to ORDER_CARD and expects 200 as the status code and a status of USER_AUTHORISATION_SUCCESS

    Then User UID1 initiates the final user authorisation to ORDER_CARD and expects a user authorisation status of USER_AUTHORISATION_INITIATED

    And User UID1 initiates the PASSCODE journey within the PASSCODE_STEP for authorisation and expects a status of JOURNEY_INITIATED

    Then Process the PASSCODE journey within the PASSCODE_STEP for user UID1 to authorise the user and expect a status JOURNEY_PROCESSED

    And User UID1 submits the PASSCODE journey within the PASSCODE_STEP for authorisation and expects a status of JOURNEY_SUCCESSFUL

    Then User UID1 submits the final user authorisation for ORDER_CARD and expects a status of USER_AUTHORISATION_SUBMITTED

    And Get the final user authorisation token for ORDER_CARD of user UID1 and expect a status USER_AUTHORISATION_SUCCESS

    Then User order a Physical Visa Credit Card as CREDIT_CARD for UID1 with card name as random_valid_choice and expect a status code of 200 and expect a card status of CARD_STATUS_PENDING
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

    Then Wait for credit card status as CARD_STATUS_UPGRADED to activate PHYSICAL card for user UID1

    Then User UID1 activates the CREDIT_CARD with valid token, with status 200

    Then User UID1 checks card status is CARD_STATUS_ACTIVE for CREDIT_CARD

    Then User UID1 fetch credit account list
#-----------------------------------------------------------------------------------------------------
    # Attempt to update credit limit when available balance < lien amount (should fail)
    Then User UID1 initiates the initial user authorisation to UPDATE_CREDIT_LIMIT and expects 200 as the status code and a status of USER_AUTHORISATION_SUCCESS

    Then User UID1 initiates the final user authorisation to UPDATE_CREDIT_LIMIT and expects a user authorisation status of USER_AUTHORISATION_INITIATED

    And User UID1 initiates the PASSCODE journey within the PASSCODE_STEP for authorisation and expects a status of JOURNEY_INITIATED

    Then Process the PASSCODE journey within the PASSCODE_STEP for user UID1 to authorise the user and expect a status JOURNEY_PROCESSED

    And User UID1 submits the PASSCODE journey within the PASSCODE_STEP for authorisation and expects a status of JOURNEY_SUCCESSFUL

    Then User UID1 submits the final user authorisation for UPDATE_CREDIT_LIMIT and expects a status of USER_AUTHORISATION_SUBMITTED

    And Get the final user authorisation token for UPDATE_CREDIT_LIMIT of user UID1 and expect a status USER_AUTHORISATION_SUCCESS

    Then User UID1 update credit limit and expect a status code of HSA_9145
      | credit_limit |
      | 80000        |

    Then User UID1 verified approved limit and it should be 20000 PKR exact

    And Verify the balance of the wallet with product code CASH_WALLET_CURRENT for user UID1 and the balance should be 41000 PKR exact

#  Attempt to update credit limit when available balance >= lien amount (should pass)
    Then User UID1 initiates the initial user authorisation to UPDATE_CREDIT_LIMIT and expects 200 as the status code and a status of USER_AUTHORISATION_SUCCESS

    Then User UID1 initiates the final user authorisation to UPDATE_CREDIT_LIMIT and expects a user authorisation status of USER_AUTHORISATION_INITIATED

    And User UID1 initiates the PASSCODE journey within the PASSCODE_STEP for authorisation and expects a status of JOURNEY_INITIATED

    Then Process the PASSCODE journey within the PASSCODE_STEP for user UID1 to authorise the user and expect a status JOURNEY_PROCESSED

    And User UID1 submits the PASSCODE journey within the PASSCODE_STEP for authorisation and expects a status of JOURNEY_SUCCESSFUL

    Then User UID1 submits the final user authorisation for UPDATE_CREDIT_LIMIT and expects a status of USER_AUTHORISATION_SUBMITTED

    And Get the final user authorisation token for UPDATE_CREDIT_LIMIT of user UID1 and expect a status USER_AUTHORISATION_SUCCESS

    Then User UID1 update credit limit and expect a status code of 200
      | credit_limit |
      | 30000        |

    Then User UID1 verified approved limit and it should be 30000 PKR exact

    And Verify the balance of the wallet with product code CASH_WALLET_CURRENT for user UID1 and the balance should be 26500 PKR exact

    Given User performs the below transaction with CREDIT_CARD and expects a status code of 200
      | user_profile_identifier | transaction_permutation_name | billing_amount | is_foreign_txn | channel    |
      | UID1                    | AUTH_CLEAR                   | 25000          | false          | E_COMMERCE |

    And Check the available credits for user UID1 and available credit should be 5000 approx

    Then User UID1 fetch credit account list


  Scenario: Credit card cash advance scenario
    #------------------------Ordering and activating card-----------------------------------------
    Then User fetch credit card constants for HUGOBANK

    Then User UID1 initiates the initial user authorisation to ORDER_CARD and expects 200 as the status code and a status of USER_AUTHORISATION_SUCCESS

    Then User UID1 initiates the final user authorisation to ORDER_CARD and expects a user authorisation status of USER_AUTHORISATION_INITIATED

    And User UID1 initiates the PASSCODE journey within the PASSCODE_STEP for authorisation and expects a status of JOURNEY_INITIATED

    Then Process the PASSCODE journey within the PASSCODE_STEP for user UID1 to authorise the user and expect a status JOURNEY_PROCESSED

    And User UID1 submits the PASSCODE journey within the PASSCODE_STEP for authorisation and expects a status of JOURNEY_SUCCESSFUL

    Then User UID1 submits the final user authorisation for ORDER_CARD and expects a status of USER_AUTHORISATION_SUBMITTED

    And Get the final user authorisation token for ORDER_CARD of user UID1 and expect a status USER_AUTHORISATION_SUCCESS

    Then User order a Physical Visa Credit Card as CREDIT_CARD for UID1 with card name as random_valid_choice and expect a status code of 200 and expect a card status of CARD_STATUS_PENDING
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

    Then Wait for credit card status as CARD_STATUS_UPGRADED to activate PHYSICAL card for user UID1

    Then User UID1 activates the CREDIT_CARD with valid token, with status 200

    Then User UID1 checks card status is CARD_STATUS_ACTIVE for CREDIT_CARD

    Then User UID1 fetch credit account list
#-----------------------------------------------------------------------------------------------------

    # Check current account balance and available credit before request
    And Check the available credits for user UID1 and available credit should be 20000 exact

    And Verify the balance of the wallet with product code CASH_WALLET_CURRENT for user UID1 and the balance should be 41000 PKR exact

    # Fetch cash advance limit for credit account
    Then User UID1 get cash advance limit for credit account expect a status code of 200

    # Validate requested cash advance amount is within limit
    And User UID1 validate cash advance eligibility
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
    Then User UID1 request cash advance for credit account and expect a status code of 200
      | cash_advance_amount |
      | 2000                |

    # Check current account balance and available credit after request
    And Check the available credits for user UID1 and available credit should be 16850 approx

    And Verify the balance of the wallet with product code CASH_WALLET_CURRENT for user UID1 and the balance should be 43000 PKR exact


  Scenario: Credit card bills related scenarios
    #------------------------Ordering and activating card-----------------------------------------
    Then User fetch credit card constants for HUGOBANK

    Then User UID1 initiates the initial user authorisation to ORDER_CARD and expects 200 as the status code and a status of USER_AUTHORISATION_SUCCESS

    Then User UID1 initiates the final user authorisation to ORDER_CARD and expects a user authorisation status of USER_AUTHORISATION_INITIATED

    And User UID1 initiates the PASSCODE journey within the PASSCODE_STEP for authorisation and expects a status of JOURNEY_INITIATED

    Then Process the PASSCODE journey within the PASSCODE_STEP for user UID1 to authorise the user and expect a status JOURNEY_PROCESSED

    And User UID1 submits the PASSCODE journey within the PASSCODE_STEP for authorisation and expects a status of JOURNEY_SUCCESSFUL

    Then User UID1 submits the final user authorisation for ORDER_CARD and expects a status of USER_AUTHORISATION_SUBMITTED

    And Get the final user authorisation token for ORDER_CARD of user UID1 and expect a status USER_AUTHORISATION_SUCCESS

    Then User order a Physical Visa Credit Card as CREDIT_CARD for UID1 with card name as random_valid_choice and expect a status code of 200 and expect a card status of CARD_STATUS_PENDING
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

    Then Wait for credit card status as CARD_STATUS_UPGRADED to activate PHYSICAL card for user UID1

    Then User UID1 activates the CREDIT_CARD with valid token, with status 200

    Then User UID1 checks card status is CARD_STATUS_ACTIVE for CREDIT_CARD

    Then User UID1 fetch credit account list
#-----------------------------------------------------------------------------------------------------
# ---------------make some transaction to get due amount------------------
    Given User performs the below transaction with CREDIT_CARD and expects a status code of 200
      | user_profile_identifier | transaction_permutation_name | billing_amount | is_foreign_txn | channel    |
      | UID1                    | AUTH_CLEAR                   | 1000           | false          | E_COMMERCE |

    And Check the available credits for user UID1 and available credit should be 19000 exact

#    Then User UID1 generate credit account bill and expect status code 200
#    Then User UID1 get the credit account bills and expect status code 200
#    Then User UID1 get the latest credit account bill and expect status code 200 and bill present as true
#    Then User UID1 get the latest credit account bill and expect status code 200 and bill present as false

    Then User UID1 pay credit account bill with amount 500 and expect status code 200 and intent status as PENDING

    And Check the available credits for user UID1 and available credit should be 19500 approx

    And Verify the balance of the wallet with product code CASH_WALLET_CURRENT for user UID1 and the balance should be 40500 PKR exact


  Scenario: User closes credit account using cash wallet
    #------------------------Ordering and activating card-----------------------------------------
    Then User fetch credit card constants for HUGOBANK

    Then User UID1 initiates the initial user authorisation to ORDER_CARD and expects 200 as the status code and a status of USER_AUTHORISATION_SUCCESS

    Then User UID1 initiates the final user authorisation to ORDER_CARD and expects a user authorisation status of USER_AUTHORISATION_INITIATED

    And User UID1 initiates the PASSCODE journey within the PASSCODE_STEP for authorisation and expects a status of JOURNEY_INITIATED

    Then Process the PASSCODE journey within the PASSCODE_STEP for user UID1 to authorise the user and expect a status JOURNEY_PROCESSED

    And User UID1 submits the PASSCODE journey within the PASSCODE_STEP for authorisation and expects a status of JOURNEY_SUCCESSFUL

    Then User UID1 submits the final user authorisation for ORDER_CARD and expects a status of USER_AUTHORISATION_SUBMITTED

    And Get the final user authorisation token for ORDER_CARD of user UID1 and expect a status USER_AUTHORISATION_SUCCESS

    Then User order a Physical Visa Credit Card as CREDIT_CARD for UID1 with card name as random_valid_choice and expect a status code of 200 and expect a card status of CARD_STATUS_PENDING
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

    Then Wait for credit card status as CARD_STATUS_UPGRADED to activate PHYSICAL card for user UID1

    Then User UID1 activates the CREDIT_CARD with valid token, with status 200

    Then User UID1 checks card status is CARD_STATUS_ACTIVE for CREDIT_CARD

    Then User UID1 fetch credit account list
#-----------------------------------------------------------------------------------------------------
# ---------------make some transaction to get due amount------------------
    Given User performs the below transaction with CREDIT_CARD and expects a status code of 200
      | user_profile_identifier | transaction_permutation_name | billing_amount | is_foreign_txn | channel    |
      | UID1                    | AUTH_CLEAR                   | 1000           | false          | E_COMMERCE |

    And Check the available credits for user UID1 and available credit should be 19000 exact

#------------------------------close credit card-------------------------------------------
    Then User UID1 initiates the initial user authorisation to CLOSE_CREDIT_ACCOUNT and expects 200 as the status code and a status of USER_AUTHORISATION_SUCCESS

    Then User UID1 initiates the final user authorisation to CLOSE_CREDIT_ACCOUNT and expects a user authorisation status of USER_AUTHORISATION_INITIATED

    And User UID1 initiates the PASSCODE journey within the PASSCODE_STEP for authorisation and expects a status of JOURNEY_INITIATED

    Then Process the PASSCODE journey within the PASSCODE_STEP for user UID1 to authorise the user and expect a status JOURNEY_PROCESSED

    And User UID1 submits the PASSCODE journey within the PASSCODE_STEP for authorisation and expects a status of JOURNEY_SUCCESSFUL

    Then User UID1 submits the final user authorisation for CLOSE_CREDIT_ACCOUNT and expects a status of USER_AUTHORISATION_SUBMITTED

    And Get the final user authorisation token for CLOSE_CREDIT_ACCOUNT of user UID1 and expect a status USER_AUTHORISATION_SUCCESS

    Then User UID1 close credit account using settlement source SETTLEMENT_SOURCE_CASH_ACCOUNT and expect status code 200

    And User UID1 verify credit account is closed


  Scenario: User closes credit account using lien amount
#------------------------Ordering and activating card-----------------------------------------
    Then User fetch credit card constants for HUGOBANK

    Then User UID1 initiates the initial user authorisation to ORDER_CARD and expects 200 as the status code and a status of USER_AUTHORISATION_SUCCESS

    Then User UID1 initiates the final user authorisation to ORDER_CARD and expects a user authorisation status of USER_AUTHORISATION_INITIATED

    And User UID1 initiates the PASSCODE journey within the PASSCODE_STEP for authorisation and expects a status of JOURNEY_INITIATED

    Then Process the PASSCODE journey within the PASSCODE_STEP for user UID1 to authorise the user and expect a status JOURNEY_PROCESSED

    And User UID1 submits the PASSCODE journey within the PASSCODE_STEP for authorisation and expects a status of JOURNEY_SUCCESSFUL

    Then User UID1 submits the final user authorisation for ORDER_CARD and expects a status of USER_AUTHORISATION_SUBMITTED

    And Get the final user authorisation token for ORDER_CARD of user UID1 and expect a status USER_AUTHORISATION_SUCCESS

    Then User order a Physical Visa Credit Card as CREDIT_CARD for UID1 with card name as random_valid_choice and expect a status code of 200 and expect a card status of CARD_STATUS_PENDING
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

    Then Wait for credit card status as CARD_STATUS_UPGRADED to activate PHYSICAL card for user UID1

    Then User UID1 activates the CREDIT_CARD with valid token, with status 200

    Then User UID1 checks card status is CARD_STATUS_ACTIVE for CREDIT_CARD

    Then User UID1 fetch credit account list
#-----------------------------------------------------------------------------------------------------
# ---------------make some transaction to get due amount------------------
    Given User performs the below transaction with CREDIT_CARD and expects a status code of 200
      | user_profile_identifier | transaction_permutation_name | billing_amount | is_foreign_txn | channel    |
      | UID1                    | AUTH_CLEAR                   | 1000           | false          | E_COMMERCE |

    And Check the available credits for user UID1 and available credit should be 19000 exact

#------------------------------close credit card-------------------------------------------
    Then User UID1 initiates the initial user authorisation to CLOSE_CREDIT_ACCOUNT and expects 200 as the status code and a status of USER_AUTHORISATION_SUCCESS

    Then User UID1 initiates the final user authorisation to CLOSE_CREDIT_ACCOUNT and expects a user authorisation status of USER_AUTHORISATION_INITIATED

    And User UID1 initiates the PASSCODE journey within the PASSCODE_STEP for authorisation and expects a status of JOURNEY_INITIATED

    Then Process the PASSCODE journey within the PASSCODE_STEP for user UID1 to authorise the user and expect a status JOURNEY_PROCESSED

    And User UID1 submits the PASSCODE journey within the PASSCODE_STEP for authorisation and expects a status of JOURNEY_SUCCESSFUL

    Then User UID1 submits the final user authorisation for CLOSE_CREDIT_ACCOUNT and expects a status of USER_AUTHORISATION_SUBMITTED

    And Get the final user authorisation token for CLOSE_CREDIT_ACCOUNT of user UID1 and expect a status USER_AUTHORISATION_SUCCESS

    Then User UID1 close credit account using settlement source SETTLEMENT_SOURCE_LIEN and expect status code 200

    And User UID1 verify credit account is closed


  Scenario: Replace Physical Secured Credit Card and verify financial integrity
    #------------------------Ordering and activating card-----------------------------------------
    Then User fetch credit card constants for HUGOBANK

    Then User UID1 initiates the initial user authorisation to ORDER_CARD and expects 200 as the status code and a status of USER_AUTHORISATION_SUCCESS

    Then User UID1 initiates the final user authorisation to ORDER_CARD and expects a user authorisation status of USER_AUTHORISATION_INITIATED

    And User UID1 initiates the PASSCODE journey within the PASSCODE_STEP for authorisation and expects a status of JOURNEY_INITIATED

    Then Process the PASSCODE journey within the PASSCODE_STEP for user UID1 to authorise the user and expect a status JOURNEY_PROCESSED

    And User UID1 submits the PASSCODE journey within the PASSCODE_STEP for authorisation and expects a status of JOURNEY_SUCCESSFUL

    Then User UID1 submits the final user authorisation for ORDER_CARD and expects a status of USER_AUTHORISATION_SUBMITTED

    And Get the final user authorisation token for ORDER_CARD of user UID1 and expect a status USER_AUTHORISATION_SUCCESS

    Then User order a Physical Visa Credit Card as CREDIT_CARD for UID1 with card name as random_valid_choice and expect a status code of 200 and expect a card status of CARD_STATUS_PENDING
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

    Then Wait for credit card status as CARD_STATUS_UPGRADED to activate PHYSICAL card for user UID1

    Then User UID1 activates the CREDIT_CARD with valid token, with status 200

    Then User UID1 checks card status is CARD_STATUS_ACTIVE for CREDIT_CARD

    Then User UID1 fetch credit account list
#-----------------------------------------------------------------------------------------------------
    And User UID1 fetch credit account balance

    # Store snapshot before replacement
    And Store credit card replacement details for user UID1

    Then User UID1 initiates the initial user authorisation to REPLACE_CARD and expects 200 as the status code and a status of USER_AUTHORISATION_SUCCESS

    Then User UID1 initiates the final user authorisation to REPLACE_CARD and expects a user authorisation status of USER_AUTHORISATION_INITIATED

    And User UID1 initiates the PASSCODE journey within the PASSCODE_STEP for authorisation and expects a status of JOURNEY_INITIATED

    Then Process the PASSCODE journey within the PASSCODE_STEP for user UID1 to authorise the user and expect a status JOURNEY_PROCESSED

    And User UID1 submits the PASSCODE journey within the PASSCODE_STEP for authorisation and expects a status of JOURNEY_SUCCESSFUL

    Then User UID1 submits the final user authorisation for REPLACE_CARD and expects a status of USER_AUTHORISATION_SUBMITTED

    And Get the final user authorisation token for REPLACE_CARD of user UID1 and expect a status USER_AUTHORISATION_SUCCESS

    Then I replace Physical credit card for user UID1 and expect a card status of CARD_STATUS_PENDING

    Then I check old card status is CARD_STATUS_DISABLED for user UID1

    Then User UID1 fetch credit account list

    And User UID1 fetch credit account balance

    And User UID1 verify credit account integrity after replacement


#######################Scenario outline##########################################################
  Scenario Outline: View Channel limits -> Update Channel limits -> Verify updated limits

    #------------------------Ordering and activating card----------------------------
    Then User fetch credit card constants for HUGOBANK

    Then User UID1 initiates the initial user authorisation to ORDER_CARD and expects 200 as the status code and a status of USER_AUTHORISATION_SUCCESS

    Then User UID1 initiates the final user authorisation to ORDER_CARD and expects a user authorisation status of USER_AUTHORISATION_INITIATED

    And User UID1 initiates the PASSCODE journey within the PASSCODE_STEP for authorisation and expects a status of JOURNEY_INITIATED

    Then Process the PASSCODE journey within the PASSCODE_STEP for user UID1 to authorise the user and expect a status JOURNEY_PROCESSED

    And User UID1 submits the PASSCODE journey within the PASSCODE_STEP for authorisation and expects a status of JOURNEY_SUCCESSFUL

    Then User UID1 submits the final user authorisation for ORDER_CARD and expects a status of USER_AUTHORISATION_SUBMITTED

    And Get the final user authorisation token for ORDER_CARD of user UID1 and expect a status USER_AUTHORISATION_SUCCESS

    Then User order a Physical Visa Credit Card as CREDIT_CARD for UID1 with card name as random_valid_choice and expect a status code of 200 and expect a card status of CARD_STATUS_PENDING
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

    Then Wait for credit card status as CARD_STATUS_UPGRADED to activate PHYSICAL card for user UID1

    Then User UID1 activates the CREDIT_CARD with valid token, with status 200

    Then User UID1 checks card status is CARD_STATUS_ACTIVE for CREDIT_CARD

    Then User UID1 fetch credit account list
#-----------------------------------------------------------------------------------------------------

    Then User UID1 get card transaction channel limits and expect status code 200

  # Authorisation for limit update
    Then User UID1 initiates the initial user authorisation to UPDATE_CARD_LIMITS and expects 200 as the status code and a status of USER_AUTHORISATION_SUCCESS

    Then User UID1 initiates the final user authorisation to UPDATE_CARD_LIMITS and expects a user authorisation status of USER_AUTHORISATION_INITIATED

    And User UID1 initiates the PASSCODE journey within the PASSCODE_STEP for authorisation and expects a status of JOURNEY_INITIATED

    Then Process the PASSCODE journey within the PASSCODE_STEP for user UID1 to authorise the user and expect a status JOURNEY_PROCESSED

    And User UID1 submits the PASSCODE journey within the PASSCODE_STEP for authorisation and expects a status of JOURNEY_SUCCESSFUL

    Then User UID1 submits the final user authorisation for UPDATE_CARD_LIMITS and expects a status of USER_AUTHORISATION_SUBMITTED

    And Get the final user authorisation token for UPDATE_CARD_LIMITS of user UID1 and expect a status USER_AUTHORISATION_SUCCESS


  # Update limit
    Then User UID1 update <limit_id> to <limit_value> and expect status code 200
    And User UID1 verify <limit_id> limit and it should be <limit_value>

  # Transaction above limit
    Given User performs the below transaction with CREDIT_CARD and expects a status code of 200
      | user_profile_identifier | transaction_permutation_name | billing_amount | is_foreign_txn | channel       |
      | UID1                    | AUTH_CLEAR                   | <above_amount> | false          | <channel>     |

    Then User UID1 check available credit and it should be <credit_after_above>

  # Transaction below limit
    Given User performs the below transaction with CREDIT_CARD and expects a status code of 200
      | user_profile_identifier | transaction_permutation_name | billing_amount | is_foreign_txn | channel       |
      | UID1                    | AUTH_CLEAR                   | <below_amount> | false          | <channel>     |

    Then User UID1 check available credit and it should be <credit_after_below>

    Examples:
      | limit_id               | limit_value | channel      | above_amount | below_amount | credit_after_above | credit_after_below |
      | POS_DAILY_LIMIT        | 5000        | POS          | 6000         | 3000         | 20000              | 17000              |
      | E_COMMERCE_DAILY_LIMIT | 5000        | E_COMMERCE   | 6000         | 3000         | 20000              | 17000              |
      | ATM_DAILY_LIMIT        | 5000        | ATM          | 6000         | 3000         | 20000              | 15850              |


  Scenario Outline: Block channels -> transaction through blocked channels -> Un-Block channels -> transaction after unblocking
#------------------------Ordering and activating card-----------------------------------------
    Then User fetch credit card constants for HUGOBANK

    Then User UID1 initiates the initial user authorisation to ORDER_CARD and expects 200 as the status code and a status of USER_AUTHORISATION_SUCCESS

    Then User UID1 initiates the final user authorisation to ORDER_CARD and expects a user authorisation status of USER_AUTHORISATION_INITIATED

    And User UID1 initiates the PASSCODE journey within the PASSCODE_STEP for authorisation and expects a status of JOURNEY_INITIATED

    Then Process the PASSCODE journey within the PASSCODE_STEP for user UID1 to authorise the user and expect a status JOURNEY_PROCESSED

    And User UID1 submits the PASSCODE journey within the PASSCODE_STEP for authorisation and expects a status of JOURNEY_SUCCESSFUL

    Then User UID1 submits the final user authorisation for ORDER_CARD and expects a status of USER_AUTHORISATION_SUBMITTED

    And Get the final user authorisation token for ORDER_CARD of user UID1 and expect a status USER_AUTHORISATION_SUCCESS

    Then User order a Physical Visa Credit Card as CREDIT_CARD for UID1 with card name as random_valid_choice and expect a status code of 200 and expect a card status of CARD_STATUS_PENDING
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

    Then Wait for credit card status as CARD_STATUS_UPGRADED to activate PHYSICAL card for user UID1

    Then User UID1 activates the CREDIT_CARD with valid token, with status 200

    Then User UID1 checks card status is CARD_STATUS_ACTIVE for CREDIT_CARD

    Then User UID1 fetch credit account list
#-----------------------------------------------------------------------------------------------------

    Then User UID1 get card transaction channel limits and expect status code 200

    Then User UID1 initiates the initial user authorisation to UPDATE_CARD_SETTINGS and expects 200 as the status code and a status of USER_AUTHORISATION_SUCCESS

    Then User UID1 initiates the final user authorisation to UPDATE_CARD_SETTINGS and expects a user authorisation status of USER_AUTHORISATION_INITIATED

    And User UID1 initiates the PASSCODE journey within the PASSCODE_STEP for authorisation and expects a status of JOURNEY_INITIATED

    Then Process the PASSCODE journey within the PASSCODE_STEP for user UID1 to authorise the user and expect a status JOURNEY_PROCESSED

    And User UID1 submits the PASSCODE journey within the PASSCODE_STEP for authorisation and expects a status of JOURNEY_SUCCESSFUL

    Then User UID1 submits the final user authorisation for UPDATE_CARD_SETTINGS and expects a status of USER_AUTHORISATION_SUBMITTED

    And Get the final user authorisation token for UPDATE_CARD_SETTINGS of user UID1 and expect a status USER_AUTHORISATION_SUCCESS

    Then User UID1 blocks the <channel> channel on CREDIT_CARD

    And User UID1 check status of Visa Physical Credit Card for channel <channel> and it should be DISABLED

    Given User performs the below transaction with CREDIT_CARD and expects a status code of 200
      | user_profile_identifier | transaction_permutation_name | billing_amount | is_foreign_txn | channel    |
      | UID1                    | AUTH_CLEAR                   | 3000           | false          | <channel> |

#    And I check the available credits for user UID1 and available credit should be 20000 exact
    And User UID1 check available credit and it should be <credit_after_block>

    Then User UID1 unblocks the <channel> channel on CREDIT_CARD

    And User UID1 check status of Visa Physical Credit Card for channel <channel> and it should be DISABLED

    Given User performs the below transaction with CREDIT_CARD and expects a status code of 200
      | user_profile_identifier | transaction_permutation_name | billing_amount | is_foreign_txn | channel    |
      | UID1                    | AUTH_CLEAR                   | 3000           | false          | <channel> |

#    And I check the available credits for user UID1 and available credit should be 17000 exact
    And User UID1 check available credit and it should be <credit_after_unblock>

    Examples:
      | channel      | credit_after_block | credit_after_unblock |
      | POS          | 20000              | 17000                |
      | E_COMMERCE   | 20000              | 17000                |
      | ATM          | 20000              | 15850                |



  Scenario Outline: Order credit card

    Then User fetch credit card constants for HUGOBANK

    Then User UID1 initiates the initial user authorisation to ORDER_CARD and expects 200 as the status code and a status of USER_AUTHORISATION_SUCCESS

    Then User UID1 initiates the final user authorisation to ORDER_CARD and expects a user authorisation status of USER_AUTHORISATION_INITIATED

    And User UID1 initiates the PASSCODE journey within the PASSCODE_STEP for authorisation and expects a status of JOURNEY_INITIATED

    Then Process the PASSCODE journey within the PASSCODE_STEP for user UID1 to authorise the user and expect a status JOURNEY_PROCESSED

    And User UID1 submits the PASSCODE journey within the PASSCODE_STEP for authorisation and expects a status of JOURNEY_SUCCESSFUL

    Then User UID1 submits the final user authorisation for ORDER_CARD and expects a status of USER_AUTHORISATION_SUBMITTED

    And Get the final user authorisation token for ORDER_CARD of user UID1 and expect a status USER_AUTHORISATION_SUCCESS

    Then User order a Physical Visa Credit Card as CREDIT_CARD for UID1 with card name as random_valid_choice and expect a status code of <expected_status_code> and expect a card status of CARD_STATUS_PENDING
      | credit_limit           |
      | <credit_limit>         |

    Examples:
      | credit_limit       | expected_status_code    |
      | 4000               | E9400                   |
      | 360000             | E9400                   |
      | 60000              | HSA_9145                |
      | 20000              | 200                     |


