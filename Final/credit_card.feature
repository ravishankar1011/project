Feature: Credit_card feature

  Background: Create 1 HUGOBANK PLUS account to test

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

    Then I get the user cash wallets for the user UID1 and expect the account status of CASH_ACCOUNT_STATUS_CREATED

    Then I deposit 70000 PKR into wallet with product code CASH_WALLET_CURRENT for user UID1 and expect a status code of 200

    And I check the balance of the wallet with product code CASH_WALLET_CURRENT for user UID1 and the balance should be 70000 PKR exact

#    Then I print the current context for UID1

  Scenario: Credit card order -> Transactions without activation -> Activation -> Transactions after activation

    Then I fetch credit card constants for HUGOBANK

    And I validate credit card eligibility using balance of the wallet with product code CASH_WALLET_CURRENT for user UID1
      | credit_limit  |
      | 20000         |

    Then I initiate the initial user authorisation to ORDER_CARD for user UID1 and expect a status of USER_AUTHORISATION_SUCCESS

    Then I initiate the final user authorisation to ORDER_CARD and expect a user authorisation status as USER_AUTHORISATION_INITIATED for user UID1

    And I initiate the PASSCODE journey within the PASSCODE_STEP for user UID1 to authorise the user and expect a status JOURNEY_INITIATED

    Then I process the PASSCODE journey within the PASSCODE_STEP for user UID1 to authorise the user and expect a status JOURNEY_PROCESSED

    And I submit the PASSCODE journey within the PASSCODE_STEP for user UID1 to authorise the user and expect a status JOURNEY_SUCCESSFUL

    Then I submit the final user authorisation for ORDER_CARD of user UID1 and expect a status USER_AUTHORISATION_SUBMITTED

    And I get the final user authorisation token for ORDER_CARD of user UID1 and expect a status USER_AUTHORISATION_SUCCESS

    Then I order a Physical Visa Credit Card for UID1 with card name as random_valid_choice and expect a status code of 200 and expect a card status of CARD_STATUS_PENDING
      | credit_limit  |
      | 20000         |

    Then I wait for 120 seconds

#--------------------------------Activation and other steps------------------------------------------------------
  #    Then I wait for 60 seconds

    Then I wait for credit card status as CARD_STATUS_UPGRADED to activate PHYSICAL card for user UID1

    Then I fetch credit account list for user UID1
    #------------------------------------Transaction without activation------------------------------------------------

    # POS transaction — should succeed
    Given I create below transaction for PHYSICAL card for user profile id and expect a status code of 200
      | user_profile_identifier | transaction_permutation_name | billing_amount | is_foreign_txn | channel |
      | UID1                    | AUTH_CLEAR                   | 500            | false          | E_COMMERCE     |

    Then I wait for 10 seconds

    And I check the available credits for user UID1 and available credit should be 19500 approx

    # E-COMMERCE transaction — should succeed
    Given I create below transaction for PHYSICAL card for user profile id and expect a status code of 200
      | user_profile_identifier | transaction_permutation_name | billing_amount | is_foreign_txn | channel    |
      | UID1                    | AUTH_CLEAR                   | 500            | false          | POS        |

    Then I wait for 10 seconds

    And I check the available credits for user UID1 and available credit should be 19000 approx


    # ATM transaction — should fail
    # Note:- ATM transaction is taking place even without activation, please check ,,i used dev urls for this
    Given I create below transaction for PHYSICAL card for user profile id and expect a status code of 200
      | user_profile_identifier | transaction_permutation_name | billing_amount | is_foreign_txn | channel |
      | UID1                    | AUTH_CLEAR                   | 500            | false          | ATM     |

    Then I wait for 10 seconds

    And I check the available credits for user UID1 and available credit should be 17350 approx

#-------------------------------------Transaction after activation------------------------------------------------

    Then I initiate the initial user authorisation to ACTIVATE_CARD for user UID1 and expect a status of USER_AUTHORISATION_SUCCESS

    Then I initiate the final user authorisation to ACTIVATE_CARD and expect a user authorisation status as USER_AUTHORISATION_INITIATED for user UID1

    And I initiate the PASSCODE journey within the PASSCODE_STEP for user UID1 to authorise the user and expect a status JOURNEY_INITIATED

    Then I process the PASSCODE journey within the PASSCODE_STEP for user UID1 to authorise the user and expect a status JOURNEY_PROCESSED

    And I submit the PASSCODE journey within the PASSCODE_STEP for user UID1 to authorise the user and expect a status JOURNEY_SUCCESSFUL

    Then I submit the final user authorisation for ACTIVATE_CARD of user UID1 and expect a status USER_AUTHORISATION_SUBMITTED

    And I get the final user authorisation token for ACTIVATE_CARD of user UID1 and expect a status USER_AUTHORISATION_SUCCESS

    Then I wait for credit card status as CARD_STATUS_UPGRADED to activate PHYSICAL card for user UID1

    Then I wait for 10 seconds

    Then I activate the PHYSICAL card for the user UID1 with valid token, with status 200

    Then I check card status is CARD_STATUS_ACTIVE for user UID1 for PHYSICAL card

    # POS transaction — should succeed
    Given I create below transaction for PHYSICAL card for user profile id and expect a status code of 200
      | user_profile_identifier | transaction_permutation_name | billing_amount | is_foreign_txn | channel |
      | UID1                    | AUTH_CLEAR                   | 500            | false          | POS     |

    Then I wait for 10 seconds

    And I check the available credits for user UID1 and available credit should be 16850 approx

    # E-COMMERCE transaction — should succeed
    Given I create below transaction for PHYSICAL card for user profile id and expect a status code of 200
      | user_profile_identifier | transaction_permutation_name | billing_amount | is_foreign_txn | channel    |
      | UID1                    | AUTH_CLEAR                   | 500            | false          | E_COMMERCE |

    Then I wait for 10 seconds

    And I check the available credits for user UID1 and available credit should be 16350 approx

    # ATM transaction — should succeed
    Given I create below transaction for PHYSICAL card for user profile id and expect a status code of 200
      | user_profile_identifier | transaction_permutation_name | billing_amount | is_foreign_txn | channel |
      | UID1                    | AUTH_CLEAR                   | 500            | false          | ATM     |

    Then I wait for 10 seconds

    And I check the available credits for user UID1 and available credit should be 14700 approx


  Scenario: Credit card order -> Activate -> Block -> Unblock -> Disable
#---------------------Ordering card----------------------------------------------------
    Then I fetch credit card constants for HUGOBANK

    And I validate credit card eligibility using balance of the wallet with product code CASH_WALLET_CURRENT for user UID1
      | credit_limit |
      | 6000         |

    Then I initiate the initial user authorisation to ORDER_CARD for user UID1 and expect a status of USER_AUTHORISATION_SUCCESS

    Then I initiate the final user authorisation to ORDER_CARD and expect a user authorisation status as USER_AUTHORISATION_INITIATED for user UID1

    And I initiate the PASSCODE journey within the PASSCODE_STEP for user UID1 to authorise the user and expect a status JOURNEY_INITIATED

    Then I process the PASSCODE journey within the PASSCODE_STEP for user UID1 to authorise the user and expect a status JOURNEY_PROCESSED

    And I submit the PASSCODE journey within the PASSCODE_STEP for user UID1 to authorise the user and expect a status JOURNEY_SUCCESSFUL

    Then I submit the final user authorisation for ORDER_CARD of user UID1 and expect a status USER_AUTHORISATION_SUBMITTED

    And I get the final user authorisation token for ORDER_CARD of user UID1 and expect a status USER_AUTHORISATION_SUCCESS

    Then I order a Physical Visa Credit Card for UID1 with card name as random_valid_choice and expect a status code of 200 and expect a card status of CARD_STATUS_PENDING
      | credit_limit |
      | 6000         |

#---------------------Activating card----------------------------------------------------

    Then I initiate the initial user authorisation to ACTIVATE_CARD for user UID1 and expect a status of USER_AUTHORISATION_SUCCESS

    Then I initiate the final user authorisation to ACTIVATE_CARD and expect a user authorisation status as USER_AUTHORISATION_INITIATED for user UID1

    And I initiate the PASSCODE journey within the PASSCODE_STEP for user UID1 to authorise the user and expect a status JOURNEY_INITIATED

    Then I process the PASSCODE journey within the PASSCODE_STEP for user UID1 to authorise the user and expect a status JOURNEY_PROCESSED

    And I submit the PASSCODE journey within the PASSCODE_STEP for user UID1 to authorise the user and expect a status JOURNEY_SUCCESSFUL

    Then I submit the final user authorisation for ACTIVATE_CARD of user UID1 and expect a status USER_AUTHORISATION_SUBMITTED

    And I get the final user authorisation token for ACTIVATE_CARD of user UID1 and expect a status USER_AUTHORISATION_SUCCESS

    Then I wait for 40 seconds

    Then I wait for credit card status as CARD_STATUS_UPGRADED to activate PHYSICAL card for user UID1

    Then I wait for 10 seconds

    Then I activate the PHYSICAL card for the user UID1 with valid token, with status 200

    Then I check card status is CARD_STATUS_ACTIVE for user UID1 for PHYSICAL card

#---------------------Blocking card----------------------------------------------------
    Then I initiate the initial user authorisation to UPDATE_CARD_STATUS for user UID1 and expect a status of USER_AUTHORISATION_SUCCESS

    Then I initiate the final user authorisation to UPDATE_CARD_STATUS and expect a user authorisation status as USER_AUTHORISATION_INITIATED for user UID1

    And I initiate the PASSCODE journey within the PASSCODE_STEP for user UID1 to authorise the user and expect a status JOURNEY_INITIATED

    Then I process the PASSCODE journey within the PASSCODE_STEP for user UID1 to authorise the user and expect a status JOURNEY_PROCESSED

    And I submit the PASSCODE journey within the PASSCODE_STEP for user UID1 to authorise the user and expect a status JOURNEY_SUCCESSFUL

    Then I submit the final user authorisation for UPDATE_CARD_STATUS of user UID1 and expect a status USER_AUTHORISATION_SUBMITTED

    And I get the final user authorisation token for UPDATE_CARD_STATUS of user UID1 and expect a status USER_AUTHORISATION_SUCCESS

    Then I update the card status of the PHYSICAL card to BLOCK for user UID1 and expect a status code of 200

    Then I check card status is CARD_STATUS_BLOCKED for user UID1 for PHYSICAL card

#---------------------Un-Blocking card----------------------------------------------------
    Then I initiate the initial user authorisation to UPDATE_CARD_STATUS for user UID1 and expect a status of USER_AUTHORISATION_SUCCESS

    Then I initiate the final user authorisation to UPDATE_CARD_STATUS and expect a user authorisation status as USER_AUTHORISATION_INITIATED for user UID1

    And I initiate the PASSCODE journey within the PASSCODE_STEP for user UID1 to authorise the user and expect a status JOURNEY_INITIATED

    Then I process the PASSCODE journey within the PASSCODE_STEP for user UID1 to authorise the user and expect a status JOURNEY_PROCESSED

    And I submit the PASSCODE journey within the PASSCODE_STEP for user UID1 to authorise the user and expect a status JOURNEY_SUCCESSFUL

    Then I submit the final user authorisation for UPDATE_CARD_STATUS of user UID1 and expect a status USER_AUTHORISATION_SUBMITTED

    And I get the final user authorisation token for UPDATE_CARD_STATUS of user UID1 and expect a status USER_AUTHORISATION_SUCCESS

    Then I update the card status of the PHYSICAL card to UNBLOCK for user UID1 and expect a status code of 200

    Then I check card status is CARD_STATUS_ACTIVE for user UID1 for PHYSICAL card

#---------------------Disable card----------------------------------------------------
    Then I initiate the initial user authorisation to UPDATE_CARD_STATUS for user UID1 and expect a status of USER_AUTHORISATION_SUCCESS

    Then I initiate the final user authorisation to UPDATE_CARD_STATUS and expect a user authorisation status as USER_AUTHORISATION_INITIATED for user UID1

    And I initiate the PASSCODE journey within the PASSCODE_STEP for user UID1 to authorise the user and expect a status JOURNEY_INITIATED

    Then I process the PASSCODE journey within the PASSCODE_STEP for user UID1 to authorise the user and expect a status JOURNEY_PROCESSED

    And I submit the PASSCODE journey within the PASSCODE_STEP for user UID1 to authorise the user and expect a status JOURNEY_SUCCESSFUL

    Then I submit the final user authorisation for UPDATE_CARD_STATUS of user UID1 and expect a status USER_AUTHORISATION_SUBMITTED

    And I get the final user authorisation token for UPDATE_CARD_STATUS of user UID1 and expect a status USER_AUTHORISATION_SUCCESS

    Then I update the card status of the PHYSICAL card to DISABLE for user UID1 and expect a status code of 200

    Then I check card status is CARD_STATUS_DISABLED for user UID1 for PHYSICAL card


  Scenario: User views credit card PIN successfully
#------------------------Ordering and activating card----------------------------
    Then I fetch credit card constants for HUGOBANK

    And I validate credit card eligibility using balance of the wallet with product code CASH_WALLET_CURRENT for user UID1
      | credit_limit |
      | 6000         |

    Then I initiate the initial user authorisation to ORDER_CARD for user UID1 and expect a status of USER_AUTHORISATION_SUCCESS

    Then I initiate the final user authorisation to ORDER_CARD and expect a user authorisation status as USER_AUTHORISATION_INITIATED for user UID1

    And I initiate the PASSCODE journey within the PASSCODE_STEP for user UID1 to authorise the user and expect a status JOURNEY_INITIATED

    Then I process the PASSCODE journey within the PASSCODE_STEP for user UID1 to authorise the user and expect a status JOURNEY_PROCESSED

    And I submit the PASSCODE journey within the PASSCODE_STEP for user UID1 to authorise the user and expect a status JOURNEY_SUCCESSFUL

    Then I submit the final user authorisation for ORDER_CARD of user UID1 and expect a status USER_AUTHORISATION_SUBMITTED

    And I get the final user authorisation token for ORDER_CARD of user UID1 and expect a status USER_AUTHORISATION_SUCCESS

    Then I order a Physical Visa Credit Card for UID1 with card name as random_valid_choice and expect a status code of 200 and expect a card status of CARD_STATUS_PENDING
      | credit_limit |
      | 6000         |

    Then I initiate the initial user authorisation to ACTIVATE_CARD for user UID1 and expect a status of USER_AUTHORISATION_SUCCESS

    Then I initiate the final user authorisation to ACTIVATE_CARD and expect a user authorisation status as USER_AUTHORISATION_INITIATED for user UID1

    And I initiate the PASSCODE journey within the PASSCODE_STEP for user UID1 to authorise the user and expect a status JOURNEY_INITIATED

    Then I process the PASSCODE journey within the PASSCODE_STEP for user UID1 to authorise the user and expect a status JOURNEY_PROCESSED

    And I submit the PASSCODE journey within the PASSCODE_STEP for user UID1 to authorise the user and expect a status JOURNEY_SUCCESSFUL

    Then I submit the final user authorisation for ACTIVATE_CARD of user UID1 and expect a status USER_AUTHORISATION_SUBMITTED

    And I get the final user authorisation token for ACTIVATE_CARD of user UID1 and expect a status USER_AUTHORISATION_SUCCESS

    Then I wait for 40 seconds

    Then I wait for credit card status as CARD_STATUS_UPGRADED to activate PHYSICAL card for user UID1

    Then I activate the PHYSICAL card for the user UID1 with valid token, with status 200

    Then I check card status is CARD_STATUS_ACTIVE for user UID1 for PHYSICAL card

#-----------------------------------------------------------------------------------------------------

    Then I initiate the initial user authorisation to SHOW_CARD_PIN for user UID1 and expect a status of USER_AUTHORISATION_SUCCESS

    Then I initiate the final user authorisation to SHOW_CARD_PIN and expect a user authorisation status as USER_AUTHORISATION_INITIATED for user UID1

    And I initiate the PASSCODE journey within the PASSCODE_STEP for user UID1 to authorise the user and expect a status JOURNEY_INITIATED

    Then I process the PASSCODE journey within the PASSCODE_STEP for user UID1 to authorise the user and expect a status JOURNEY_PROCESSED

    And I submit the PASSCODE journey within the PASSCODE_STEP for user UID1 to authorise the user and expect a status JOURNEY_SUCCESSFUL

    Then I submit the final user authorisation for SHOW_CARD_PIN of user UID1 and expect a status USER_AUTHORISATION_SUBMITTED

    And I get the final user authorisation token for SHOW_CARD_PIN of user UID1 and expect a status USER_AUTHORISATION_SUCCESS

    Then I view the credit card PIN for user UID1 and expect the PIN to be returned successfully


  Scenario: View Channel limits (POS,E_COMMERCE,ATM) -> Update Channel limits -> Verify updated limits -> Get Channel limits history
    #------------------------Ordering and activating card----------------------------
    Then I fetch credit card constants for HUGOBANK

    And I validate credit card eligibility using balance of the wallet with product code CASH_WALLET_CURRENT for user UID1
      | credit_limit |
      | 6000         |

    Then I initiate the initial user authorisation to ORDER_CARD for user UID1 and expect a status of USER_AUTHORISATION_SUCCESS

    Then I initiate the final user authorisation to ORDER_CARD and expect a user authorisation status as USER_AUTHORISATION_INITIATED for user UID1

    And I initiate the PASSCODE journey within the PASSCODE_STEP for user UID1 to authorise the user and expect a status JOURNEY_INITIATED

    Then I process the PASSCODE journey within the PASSCODE_STEP for user UID1 to authorise the user and expect a status JOURNEY_PROCESSED

    And I submit the PASSCODE journey within the PASSCODE_STEP for user UID1 to authorise the user and expect a status JOURNEY_SUCCESSFUL

    Then I submit the final user authorisation for ORDER_CARD of user UID1 and expect a status USER_AUTHORISATION_SUBMITTED

    And I get the final user authorisation token for ORDER_CARD of user UID1 and expect a status USER_AUTHORISATION_SUCCESS

    Then I order a Physical Visa Credit Card for UID1 with card name as random_valid_choice and expect a status code of 200 and expect a card status of CARD_STATUS_PENDING
      | credit_limit |
      | 6000         |

    Then I initiate the initial user authorisation to ACTIVATE_CARD for user UID1 and expect a status of USER_AUTHORISATION_SUCCESS

    Then I initiate the final user authorisation to ACTIVATE_CARD and expect a user authorisation status as USER_AUTHORISATION_INITIATED for user UID1

    And I initiate the PASSCODE journey within the PASSCODE_STEP for user UID1 to authorise the user and expect a status JOURNEY_INITIATED

    Then I process the PASSCODE journey within the PASSCODE_STEP for user UID1 to authorise the user and expect a status JOURNEY_PROCESSED

    And I submit the PASSCODE journey within the PASSCODE_STEP for user UID1 to authorise the user and expect a status JOURNEY_SUCCESSFUL

    Then I submit the final user authorisation for ACTIVATE_CARD of user UID1 and expect a status USER_AUTHORISATION_SUBMITTED

    And I get the final user authorisation token for ACTIVATE_CARD of user UID1 and expect a status USER_AUTHORISATION_SUCCESS

    Then I wait for 40 seconds

    Then I wait for credit card status as CARD_STATUS_UPGRADED to activate PHYSICAL card for user UID1

    Then I activate the PHYSICAL card for the user UID1 with valid token, with status 200

    Then I check card status is CARD_STATUS_ACTIVE for user UID1 for PHYSICAL card

    Then I fetch credit account list for user UID1
#-----------------------------------------------------------------------------------------------------

#-----------------------------for changing limit of channels--------------------------
    Then I get card transaction channel limits for user UID1 and expect status code 200


#    ----------------------UPDATE LIMITS-------------------------------------------
    Then I initiate the initial user authorisation to UPDATE_CARD_LIMITS for user UID1 and expect a status of USER_AUTHORISATION_SUCCESS

    Then I initiate the final user authorisation to UPDATE_CARD_LIMITS and expect a user authorisation status as USER_AUTHORISATION_INITIATED for user UID1

    And I initiate the PASSCODE journey within the PASSCODE_STEP for user UID1 to authorise the user and expect a status JOURNEY_INITIATED

    Then I process the PASSCODE journey within the PASSCODE_STEP for user UID1 to authorise the user and expect a status JOURNEY_PROCESSED

    And I submit the PASSCODE journey within the PASSCODE_STEP for user UID1 to authorise the user and expect a status JOURNEY_SUCCESSFUL

    Then I submit the final user authorisation for UPDATE_CARD_LIMITS of user UID1 and expect a status USER_AUTHORISATION_SUBMITTED

    And I get the final user authorisation token for UPDATE_CARD_LIMITS of user UID1 and expect a status USER_AUTHORISATION_SUCCESS

    Then I update card limit for user UID1 and expect status code 200
      | limit_id        | value |
      | POS_DAILY_LIMIT | 5000  |

    Then I wait for 10 seconds

    And I verified the updated POS_DAILY_LIMIT limit for user UID1 and limit should be 5000

    Then I update card limit for user UID1 and expect status code 200
      | limit_id               | value |
      | E_COMMERCE_DAILY_LIMIT | 5000  |

    Then I wait for 10 seconds

    And I verified the updated E_COMMERCE_DAILY_LIMIT limit for user UID1 and limit should be 5000

    Then I update card limit for user UID1 and expect status code 200
      | limit_id               | value |
      | ATM_DAILY_LIMIT | 5000  |

    Then I wait for 10 seconds

    And I verified the updated ATM_DAILY_LIMIT limit for user UID1 and limit should be 5000

    # GET limit history
    Then I get limit history for card for user UID1 and expect status code 200
      | limit_id        |
      | POS_DAILY_LIMIT |


  Scenario: Block channels -> transaction through blocked channel -> Un-Block channels -> transaction after unblocking
#------------------------Ordering and activating card-----------------------------------------
    Then I fetch credit card constants for HUGOBANK

    And I validate credit card eligibility using balance of the wallet with product code CASH_WALLET_CURRENT for user UID1
      | credit_limit |
      | 6000         |

    Then I initiate the initial user authorisation to ORDER_CARD for user UID1 and expect a status of USER_AUTHORISATION_SUCCESS

    Then I initiate the final user authorisation to ORDER_CARD and expect a user authorisation status as USER_AUTHORISATION_INITIATED for user UID1

    And I initiate the PASSCODE journey within the PASSCODE_STEP for user UID1 to authorise the user and expect a status JOURNEY_INITIATED

    Then I process the PASSCODE journey within the PASSCODE_STEP for user UID1 to authorise the user and expect a status JOURNEY_PROCESSED

    And I submit the PASSCODE journey within the PASSCODE_STEP for user UID1 to authorise the user and expect a status JOURNEY_SUCCESSFUL

    Then I submit the final user authorisation for ORDER_CARD of user UID1 and expect a status USER_AUTHORISATION_SUBMITTED

    And I get the final user authorisation token for ORDER_CARD of user UID1 and expect a status USER_AUTHORISATION_SUCCESS

    Then I order a Physical Visa Credit Card for UID1 with card name as random_valid_choice and expect a status code of 200 and expect a card status of CARD_STATUS_PENDING
      | credit_limit |
      | 6000         |

    Then I initiate the initial user authorisation to ACTIVATE_CARD for user UID1 and expect a status of USER_AUTHORISATION_SUCCESS

    Then I initiate the final user authorisation to ACTIVATE_CARD and expect a user authorisation status as USER_AUTHORISATION_INITIATED for user UID1

    And I initiate the PASSCODE journey within the PASSCODE_STEP for user UID1 to authorise the user and expect a status JOURNEY_INITIATED

    Then I process the PASSCODE journey within the PASSCODE_STEP for user UID1 to authorise the user and expect a status JOURNEY_PROCESSED

    And I submit the PASSCODE journey within the PASSCODE_STEP for user UID1 to authorise the user and expect a status JOURNEY_SUCCESSFUL

    Then I submit the final user authorisation for ACTIVATE_CARD of user UID1 and expect a status USER_AUTHORISATION_SUBMITTED

    And I get the final user authorisation token for ACTIVATE_CARD of user UID1 and expect a status USER_AUTHORISATION_SUCCESS

    Then I wait for 40 seconds

    Then I wait for credit card status as CARD_STATUS_UPGRADED to activate PHYSICAL card for user UID1

    Then I activate the PHYSICAL card for the user UID1 with valid token, with status 200

    Then I check card status is CARD_STATUS_ACTIVE for user UID1 for PHYSICAL card

    Then I fetch credit account list for user UID1
#-----------------------------------------------------------------------------------------------------

    Then I get card transaction channel limits for user UID1 and expect status code 200

    Then I initiate the initial user authorisation to UPDATE_CARD_SETTINGS for user UID1 and expect a status of USER_AUTHORISATION_SUCCESS

    Then I initiate the final user authorisation to UPDATE_CARD_SETTINGS and expect a user authorisation status as USER_AUTHORISATION_INITIATED for user UID1

    And I initiate the PASSCODE journey within the PASSCODE_STEP for user UID1 to authorise the user and expect a status JOURNEY_INITIATED

    Then I process the PASSCODE journey within the PASSCODE_STEP for user UID1 to authorise the user and expect a status JOURNEY_PROCESSED

    And I submit the PASSCODE journey within the PASSCODE_STEP for user UID1 to authorise the user and expect a status JOURNEY_SUCCESSFUL

    Then I submit the final user authorisation for UPDATE_CARD_SETTINGS of user UID1 and expect a status USER_AUTHORISATION_SUBMITTED

    And I get the final user authorisation token for UPDATE_CARD_SETTINGS of user UID1 and expect a status USER_AUTHORISATION_SUCCESS

    Then I block the Visa Physical Credit Card channel E_COMMERCE for user UID1

    And I check status of Visa Physical Credit Card channel E_COMMERCE for UID1 and it should be DISABLED

    Given I create below transaction for PHYSICAL card for user profile id and expect a status code of 200
      | user_profile_identifier | transaction_permutation_name | billing_amount | is_foreign_txn | channel        |
      | UID1                    | AUTH_CLEAR                   | 1000           | false          | E_COMMERCE     |

    Then I wait for 10 seconds

    And I check the available credits for user UID1 and available credit should be 6000 exact

    Then I unblock the Visa Physical Credit Card channel E_COMMERCE for user UID1

    And I check status of Visa Physical Credit Card channel E_COMMERCE for UID1 and it should be ENABLED

    Given I create below transaction for PHYSICAL card for user profile id and expect a status code of 200
      | user_profile_identifier | transaction_permutation_name | billing_amount | is_foreign_txn | channel        |
      | UID1                    | AUTH_CLEAR                   | 1000           | false          | E_COMMERCE     |

    Then I wait for 10 seconds

    And I check the available credits for user UID1 and available credit should be 5000 exact


  Scenario: View current credit limit -> Update credit limit -> Get updated limit
#------------------------Ordering and activating card-----------------------------------------
    Then I fetch credit card constants for HUGOBANK

    And I validate credit card eligibility using balance of the wallet with product code CASH_WALLET_CURRENT for user UID1
      | credit_limit  |
      | 20000         |

    Then I initiate the initial user authorisation to ORDER_CARD for user UID1 and expect a status of USER_AUTHORISATION_SUCCESS

    Then I initiate the final user authorisation to ORDER_CARD and expect a user authorisation status as USER_AUTHORISATION_INITIATED for user UID1

    And I initiate the PASSCODE journey within the PASSCODE_STEP for user UID1 to authorise the user and expect a status JOURNEY_INITIATED

    Then I process the PASSCODE journey within the PASSCODE_STEP for user UID1 to authorise the user and expect a status JOURNEY_PROCESSED

    And I submit the PASSCODE journey within the PASSCODE_STEP for user UID1 to authorise the user and expect a status JOURNEY_SUCCESSFUL

    Then I submit the final user authorisation for ORDER_CARD of user UID1 and expect a status USER_AUTHORISATION_SUBMITTED

    And I get the final user authorisation token for ORDER_CARD of user UID1 and expect a status USER_AUTHORISATION_SUCCESS

    Then I order a Physical Visa Credit Card for UID1 with card name as random_valid_choice and expect a status code of 200 and expect a card status of CARD_STATUS_PENDING
      | credit_limit  |
      | 20000         |

    Then I initiate the initial user authorisation to ACTIVATE_CARD for user UID1 and expect a status of USER_AUTHORISATION_SUCCESS

    Then I initiate the final user authorisation to ACTIVATE_CARD and expect a user authorisation status as USER_AUTHORISATION_INITIATED for user UID1

    And I initiate the PASSCODE journey within the PASSCODE_STEP for user UID1 to authorise the user and expect a status JOURNEY_INITIATED

    Then I process the PASSCODE journey within the PASSCODE_STEP for user UID1 to authorise the user and expect a status JOURNEY_PROCESSED

    And I submit the PASSCODE journey within the PASSCODE_STEP for user UID1 to authorise the user and expect a status JOURNEY_SUCCESSFUL

    Then I submit the final user authorisation for ACTIVATE_CARD of user UID1 and expect a status USER_AUTHORISATION_SUBMITTED

    And I get the final user authorisation token for ACTIVATE_CARD of user UID1 and expect a status USER_AUTHORISATION_SUCCESS

    Then I wait for 40 seconds

    Then I wait for credit card status as CARD_STATUS_UPGRADED to activate PHYSICAL card for user UID1

    Then I activate the PHYSICAL card for the user UID1 with valid token, with status 200

    Then I check card status is CARD_STATUS_ACTIVE for user UID1 for PHYSICAL card

    Then I fetch credit account list for user UID1
#-----------------------------------------------------------------------------------------------------

    # Attempt to update credit limit when available balance < lien amount (should fail)
    Then I initiate the initial user authorisation to UPDATE_CREDIT_LIMIT for user UID1 and expect a status of USER_AUTHORISATION_SUCCESS

    Then I initiate the final user authorisation to UPDATE_CREDIT_LIMIT and expect a user authorisation status as USER_AUTHORISATION_INITIATED for user UID1

    And I initiate the PASSCODE journey within the PASSCODE_STEP for user UID1 to authorise the user and expect a status JOURNEY_INITIATED

    Then I process the PASSCODE journey within the PASSCODE_STEP for user UID1 to authorise the user and expect a status JOURNEY_PROCESSED

    And I submit the PASSCODE journey within the PASSCODE_STEP for user UID1 to authorise the user and expect a status JOURNEY_SUCCESSFUL

    Then I submit the final user authorisation for UPDATE_CREDIT_LIMIT of user UID1 and expect a status USER_AUTHORISATION_SUBMITTED

    And I get the final user authorisation token for UPDATE_CREDIT_LIMIT of user UID1 and expect a status USER_AUTHORISATION_SUCCESS

    Then I update credit limit for user UID1 and expect a status code of HSA_9145
      | credit_limit |
      | 80000        |

    Then I verified approved_limit for user UID1 and approved_limit should be 20000 PKR exact

    And I check the balance of the wallet with product code CASH_WALLET_CURRENT for user UID1 and the balance should be 41000 PKR exact

#  Attempt to update credit limit when available balance >= lien amount (should pass)

    Then I initiate the initial user authorisation to UPDATE_CREDIT_LIMIT for user UID1 and expect a status of USER_AUTHORISATION_SUCCESS

    Then I initiate the final user authorisation to UPDATE_CREDIT_LIMIT and expect a user authorisation status as USER_AUTHORISATION_INITIATED for user UID1

    And I initiate the PASSCODE journey within the PASSCODE_STEP for user UID1 to authorise the user and expect a status JOURNEY_INITIATED

    Then I process the PASSCODE journey within the PASSCODE_STEP for user UID1 to authorise the user and expect a status JOURNEY_PROCESSED

    And I submit the PASSCODE journey within the PASSCODE_STEP for user UID1 to authorise the user and expect a status JOURNEY_SUCCESSFUL

    Then I submit the final user authorisation for UPDATE_CREDIT_LIMIT of user UID1 and expect a status USER_AUTHORISATION_SUBMITTED

    And I get the final user authorisation token for UPDATE_CREDIT_LIMIT of user UID1 and expect a status USER_AUTHORISATION_SUCCESS

    Then I update credit limit for user UID1 and expect a status code of 200
      | credit_limit |
      | 30000        |

    Then I wait for 40 seconds

    Then I verified approved_limit for user UID1 and approved_limit should be 30000 PKR exact

    And I check the balance of the wallet with product code CASH_WALLET_CURRENT for user UID1 and the balance should be 26500 PKR exact

    Then I fetch credit account list for user UID1


  Scenario: Credit card cash advance scenario
    #------------------------Ordering and activating card-----------------------------------------
    Then I fetch credit card constants for HUGOBANK

    And I validate credit card eligibility using balance of the wallet with product code CASH_WALLET_CURRENT for user UID1
      | credit_limit  |
      | 20000         |

    Then I initiate the initial user authorisation to ORDER_CARD for user UID1 and expect a status of USER_AUTHORISATION_SUCCESS

    Then I initiate the final user authorisation to ORDER_CARD and expect a user authorisation status as USER_AUTHORISATION_INITIATED for user UID1

    And I initiate the PASSCODE journey within the PASSCODE_STEP for user UID1 to authorise the user and expect a status JOURNEY_INITIATED

    Then I process the PASSCODE journey within the PASSCODE_STEP for user UID1 to authorise the user and expect a status JOURNEY_PROCESSED

    And I submit the PASSCODE journey within the PASSCODE_STEP for user UID1 to authorise the user and expect a status JOURNEY_SUCCESSFUL

    Then I submit the final user authorisation for ORDER_CARD of user UID1 and expect a status USER_AUTHORISATION_SUBMITTED

    And I get the final user authorisation token for ORDER_CARD of user UID1 and expect a status USER_AUTHORISATION_SUCCESS

    Then I order a Physical Visa Credit Card for UID1 with card name as random_valid_choice and expect a status code of 200 and expect a card status of CARD_STATUS_PENDING
      | credit_limit  |
      | 20000         |

    Then I initiate the initial user authorisation to ACTIVATE_CARD for user UID1 and expect a status of USER_AUTHORISATION_SUCCESS

    Then I initiate the final user authorisation to ACTIVATE_CARD and expect a user authorisation status as USER_AUTHORISATION_INITIATED for user UID1

    And I initiate the PASSCODE journey within the PASSCODE_STEP for user UID1 to authorise the user and expect a status JOURNEY_INITIATED

    Then I process the PASSCODE journey within the PASSCODE_STEP for user UID1 to authorise the user and expect a status JOURNEY_PROCESSED

    And I submit the PASSCODE journey within the PASSCODE_STEP for user UID1 to authorise the user and expect a status JOURNEY_SUCCESSFUL

    Then I submit the final user authorisation for ACTIVATE_CARD of user UID1 and expect a status USER_AUTHORISATION_SUBMITTED

    And I get the final user authorisation token for ACTIVATE_CARD of user UID1 and expect a status USER_AUTHORISATION_SUCCESS

    Then I wait for 40 seconds

    Then I wait for credit card status as CARD_STATUS_UPGRADED to activate PHYSICAL card for user UID1

    Then I activate the PHYSICAL card for the user UID1 with valid token, with status 200

    Then I check card status is CARD_STATUS_ACTIVE for user UID1 for PHYSICAL card

    Then I fetch credit account list for user UID1
#-----------------------------------------------------------------------------------------------------

    # Check current account balance and available credit before request
    And I check the available credits for user UID1 and available credit should be 20000 exact

    And I check the balance of the wallet with product code CASH_WALLET_CURRENT for user UID1 and the balance should be 41000 PKR exact

    # Fetch cash advance limit for credit account
    Then I get cash advance limit for credit account of user UID1 and expect a status code of 200

    # Validate requested cash advance amount is within limit
    And I validate cash advance eligibility for user UID1
      | cash_advance_amount  |
      | 2000                 |


    # Authorisation for cash advance
    Then I initiate the initial user authorisation to REQUEST_CASH_ADVANCE for user UID1 and expect a status of USER_AUTHORISATION_SUCCESS

    Then I initiate the final user authorisation to REQUEST_CASH_ADVANCE and expect a user authorisation status as USER_AUTHORISATION_INITIATED for user UID1

    And I initiate the PASSCODE journey within the PASSCODE_STEP for user UID1 to authorise the user and expect a status JOURNEY_INITIATED

    Then I process the PASSCODE journey within the PASSCODE_STEP for user UID1 to authorise the user and expect a status JOURNEY_PROCESSED

    And I submit the PASSCODE journey within the PASSCODE_STEP for user UID1 to authorise the user and expect a status JOURNEY_SUCCESSFUL

    Then I submit the final user authorisation for REQUEST_CASH_ADVANCE of user UID1 and expect a status USER_AUTHORISATION_SUBMITTED

    And I get the final user authorisation token for REQUEST_CASH_ADVANCE of user UID1 and expect a status USER_AUTHORISATION_SUCCESS

    # Request cash advance
    Then I request cash advance for credit account of user UID1 and expect a status code of 200
      | cash_advance_amount |
      | 2000                |

    # Check current account balance and available credit after request
    And I check the available credits for user UID1 and available credit should be 16850 approx

    And I check the balance of the wallet with product code CASH_WALLET_CURRENT for user UID1 and the balance should be 43000 PKR exact


  Scenario: Credit card bills related scenarios
    #------------------------Ordering and activating card-----------------------------------------
    Then I fetch credit card constants for HUGOBANK

    And I validate credit card eligibility using balance of the wallet with product code CASH_WALLET_CURRENT for user UID1
      | credit_limit  |
      | 20000         |

    Then I initiate the initial user authorisation to ORDER_CARD for user UID1 and expect a status of USER_AUTHORISATION_SUCCESS

    Then I initiate the final user authorisation to ORDER_CARD and expect a user authorisation status as USER_AUTHORISATION_INITIATED for user UID1

    And I initiate the PASSCODE journey within the PASSCODE_STEP for user UID1 to authorise the user and expect a status JOURNEY_INITIATED

    Then I process the PASSCODE journey within the PASSCODE_STEP for user UID1 to authorise the user and expect a status JOURNEY_PROCESSED

    And I submit the PASSCODE journey within the PASSCODE_STEP for user UID1 to authorise the user and expect a status JOURNEY_SUCCESSFUL

    Then I submit the final user authorisation for ORDER_CARD of user UID1 and expect a status USER_AUTHORISATION_SUBMITTED

    And I get the final user authorisation token for ORDER_CARD of user UID1 and expect a status USER_AUTHORISATION_SUCCESS

    Then I order a Physical Visa Credit Card for UID1 with card name as random_valid_choice and expect a status code of 200 and expect a card status of CARD_STATUS_PENDING
      | credit_limit  |
      | 20000         |

    Then I initiate the initial user authorisation to ACTIVATE_CARD for user UID1 and expect a status of USER_AUTHORISATION_SUCCESS

    Then I initiate the final user authorisation to ACTIVATE_CARD and expect a user authorisation status as USER_AUTHORISATION_INITIATED for user UID1

    And I initiate the PASSCODE journey within the PASSCODE_STEP for user UID1 to authorise the user and expect a status JOURNEY_INITIATED

    Then I process the PASSCODE journey within the PASSCODE_STEP for user UID1 to authorise the user and expect a status JOURNEY_PROCESSED

    And I submit the PASSCODE journey within the PASSCODE_STEP for user UID1 to authorise the user and expect a status JOURNEY_SUCCESSFUL

    Then I submit the final user authorisation for ACTIVATE_CARD of user UID1 and expect a status USER_AUTHORISATION_SUBMITTED

    And I get the final user authorisation token for ACTIVATE_CARD of user UID1 and expect a status USER_AUTHORISATION_SUCCESS

    Then I wait for 40 seconds

    Then I wait for credit card status as CARD_STATUS_UPGRADED to activate PHYSICAL card for user UID1

    Then I activate the PHYSICAL card for the user UID1 with valid token, with status 200

    Then I check card status is CARD_STATUS_ACTIVE for user UID1 for PHYSICAL card

    Then I fetch credit account list for user UID1
#-----------------------------------------------------------------------------------------------------
# ---------------make some transaction to get due amount------------------
    Given I create below transaction for PHYSICAL card for user profile id and expect a status code of 200
      | user_profile_identifier | transaction_permutation_name | billing_amount | is_foreign_txn | channel        |
      | UID1                    | AUTH_CLEAR                   | 1000           | false          | E_COMMERCE     |

    Then I wait for 10 seconds

    And I check the available credits for user UID1 and available credit should be 19000 exact

#    Then I generate credit account bill for user UID1 and expect status code 200
#    Then I get the credit account bills for user UID1 and expect status code 200
#    Then I get the latest credit account bill for user UID1 and expect status code 200 and bill present as true
#    Then I get the latest credit account bill for user UID1 and expect status code 200 and bill present as false

    Then I pay credit account bill for user UID1 with amount 500 and expect status code 200 and intent status as PENDING

    Then I wait for 10 seconds

    And I check the available credits for user UID1 and available credit should be 19500 approx

    And I check the balance of the wallet with product code CASH_WALLET_CURRENT for user UID1 and the balance should be 40500 PKR exact


  Scenario: User closes credit account using cash wallet
    #------------------------Ordering and activating card-----------------------------------------
    Then I fetch credit card constants for HUGOBANK

    And I validate credit card eligibility using balance of the wallet with product code CASH_WALLET_CURRENT for user UID1
      | credit_limit  |
      | 20000         |

    Then I initiate the initial user authorisation to ORDER_CARD for user UID1 and expect a status of USER_AUTHORISATION_SUCCESS

    Then I initiate the final user authorisation to ORDER_CARD and expect a user authorisation status as USER_AUTHORISATION_INITIATED for user UID1

    And I initiate the PASSCODE journey within the PASSCODE_STEP for user UID1 to authorise the user and expect a status JOURNEY_INITIATED

    Then I process the PASSCODE journey within the PASSCODE_STEP for user UID1 to authorise the user and expect a status JOURNEY_PROCESSED

    And I submit the PASSCODE journey within the PASSCODE_STEP for user UID1 to authorise the user and expect a status JOURNEY_SUCCESSFUL

    Then I submit the final user authorisation for ORDER_CARD of user UID1 and expect a status USER_AUTHORISATION_SUBMITTED

    And I get the final user authorisation token for ORDER_CARD of user UID1 and expect a status USER_AUTHORISATION_SUCCESS

    Then I order a Physical Visa Credit Card for UID1 with card name as random_valid_choice and expect a status code of 200 and expect a card status of CARD_STATUS_PENDING
      | credit_limit  |
      | 20000         |

    Then I initiate the initial user authorisation to ACTIVATE_CARD for user UID1 and expect a status of USER_AUTHORISATION_SUCCESS

    Then I initiate the final user authorisation to ACTIVATE_CARD and expect a user authorisation status as USER_AUTHORISATION_INITIATED for user UID1

    And I initiate the PASSCODE journey within the PASSCODE_STEP for user UID1 to authorise the user and expect a status JOURNEY_INITIATED

    Then I process the PASSCODE journey within the PASSCODE_STEP for user UID1 to authorise the user and expect a status JOURNEY_PROCESSED

    And I submit the PASSCODE journey within the PASSCODE_STEP for user UID1 to authorise the user and expect a status JOURNEY_SUCCESSFUL

    Then I submit the final user authorisation for ACTIVATE_CARD of user UID1 and expect a status USER_AUTHORISATION_SUBMITTED

    And I get the final user authorisation token for ACTIVATE_CARD of user UID1 and expect a status USER_AUTHORISATION_SUCCESS

    Then I wait for 40 seconds

    Then I wait for credit card status as CARD_STATUS_UPGRADED to activate PHYSICAL card for user UID1

    Then I activate the PHYSICAL card for the user UID1 with valid token, with status 200

    Then I check card status is CARD_STATUS_ACTIVE for user UID1 for PHYSICAL card

    Then I fetch credit account list for user UID1
#-----------------------------------------------------------------------------------------------------
# ---------------make some transaction to get due amount------------------
    Given I create below transaction for PHYSICAL card for user profile id and expect a status code of 200
      | user_profile_identifier | transaction_permutation_name | billing_amount | is_foreign_txn | channel        |
      | UID1                    | AUTH_CLEAR                   | 1000           | false          | E_COMMERCE     |

    Then I wait for 10 seconds

    And I check the available credits for user UID1 and available credit should be 19000 exact

#------------------------------close credit card-------------------------------------------
    Then I initiate the initial user authorisation to CLOSE_CREDIT_ACCOUNT for user UID1 and expect a status of USER_AUTHORISATION_SUCCESS

    Then I initiate the final user authorisation to CLOSE_CREDIT_ACCOUNT and expect a user authorisation status as USER_AUTHORISATION_INITIATED for user UID1

    And I initiate the PASSCODE journey within the PASSCODE_STEP for user UID1 to authorise the user and expect a status JOURNEY_INITIATED

    Then I process the PASSCODE journey within the PASSCODE_STEP for user UID1 to authorise the user and expect a status JOURNEY_PROCESSED

    And I submit the PASSCODE journey within the PASSCODE_STEP for user UID1 to authorise the user and expect a status JOURNEY_SUCCESSFUL

    Then I submit the final user authorisation for CLOSE_CREDIT_ACCOUNT of user UID1 and expect a status USER_AUTHORISATION_SUBMITTED

    And I get the final user authorisation token for CLOSE_CREDIT_ACCOUNT of user UID1 and expect a status USER_AUTHORISATION_SUCCESS

    Then I close credit account for user UID1 using settlement source SETTLEMENT_SOURCE_CASH_ACCOUNT and expect status code 200

    And I verify credit account is closed for user UID1


  Scenario: User closes credit account using lien amount
#------------------------Ordering and activating card-----------------------------------------
    Then I fetch credit card constants for HUGOBANK

    And I validate credit card eligibility using balance of the wallet with product code CASH_WALLET_CURRENT for user UID1
      | credit_limit  |
      | 20000         |

    Then I initiate the initial user authorisation to ORDER_CARD for user UID1 and expect a status of USER_AUTHORISATION_SUCCESS

    Then I initiate the final user authorisation to ORDER_CARD and expect a user authorisation status as USER_AUTHORISATION_INITIATED for user UID1

    And I initiate the PASSCODE journey within the PASSCODE_STEP for user UID1 to authorise the user and expect a status JOURNEY_INITIATED

    Then I process the PASSCODE journey within the PASSCODE_STEP for user UID1 to authorise the user and expect a status JOURNEY_PROCESSED

    And I submit the PASSCODE journey within the PASSCODE_STEP for user UID1 to authorise the user and expect a status JOURNEY_SUCCESSFUL

    Then I submit the final user authorisation for ORDER_CARD of user UID1 and expect a status USER_AUTHORISATION_SUBMITTED

    And I get the final user authorisation token for ORDER_CARD of user UID1 and expect a status USER_AUTHORISATION_SUCCESS

    Then I order a Physical Visa Credit Card for UID1 with card name as random_valid_choice and expect a status code of 200 and expect a card status of CARD_STATUS_PENDING
      | credit_limit  |
      | 20000         |

    Then I initiate the initial user authorisation to ACTIVATE_CARD for user UID1 and expect a status of USER_AUTHORISATION_SUCCESS

    Then I initiate the final user authorisation to ACTIVATE_CARD and expect a user authorisation status as USER_AUTHORISATION_INITIATED for user UID1

    And I initiate the PASSCODE journey within the PASSCODE_STEP for user UID1 to authorise the user and expect a status JOURNEY_INITIATED

    Then I process the PASSCODE journey within the PASSCODE_STEP for user UID1 to authorise the user and expect a status JOURNEY_PROCESSED

    And I submit the PASSCODE journey within the PASSCODE_STEP for user UID1 to authorise the user and expect a status JOURNEY_SUCCESSFUL

    Then I submit the final user authorisation for ACTIVATE_CARD of user UID1 and expect a status USER_AUTHORISATION_SUBMITTED

    And I get the final user authorisation token for ACTIVATE_CARD of user UID1 and expect a status USER_AUTHORISATION_SUCCESS

    Then I wait for 40 seconds

    Then I wait for credit card status as CARD_STATUS_UPGRADED to activate PHYSICAL card for user UID1

    Then I activate the PHYSICAL card for the user UID1 with valid token, with status 200

    Then I check card status is CARD_STATUS_ACTIVE for user UID1 for PHYSICAL card

    Then I fetch credit account list for user UID1
#-----------------------------------------------------------------------------------------------------
# ---------------make some transaction to get due amount------------------
    Given I create below transaction for PHYSICAL card for user profile id and expect a status code of 200
      | user_profile_identifier | transaction_permutation_name | billing_amount | is_foreign_txn | channel        |
      | UID1                    | AUTH_CLEAR                   | 1000           | false          | E_COMMERCE     |

    Then I wait for 10 seconds

    And I check the available credits for user UID1 and available credit should be 19000 exact

#------------------------------close credit card-------------------------------------------
    Then I initiate the initial user authorisation to CLOSE_CREDIT_ACCOUNT for user UID1 and expect a status of USER_AUTHORISATION_SUCCESS

    Then I initiate the final user authorisation to CLOSE_CREDIT_ACCOUNT and expect a user authorisation status as USER_AUTHORISATION_INITIATED for user UID1

    And I initiate the PASSCODE journey within the PASSCODE_STEP for user UID1 to authorise the user and expect a status JOURNEY_INITIATED

    Then I process the PASSCODE journey within the PASSCODE_STEP for user UID1 to authorise the user and expect a status JOURNEY_PROCESSED

    And I submit the PASSCODE journey within the PASSCODE_STEP for user UID1 to authorise the user and expect a status JOURNEY_SUCCESSFUL

    Then I submit the final user authorisation for CLOSE_CREDIT_ACCOUNT of user UID1 and expect a status USER_AUTHORISATION_SUBMITTED

    And I get the final user authorisation token for CLOSE_CREDIT_ACCOUNT of user UID1 and expect a status USER_AUTHORISATION_SUCCESS

    Then I close credit account for user UID1 using settlement source SETTLEMENT_SOURCE_LIEN and expect status code 200

    And I verify credit account is closed for user UID1


  Scenario: Replace Physical Secured Credit Card and verify financial integrity
    #------------------------Ordering and activating card-----------------------------------------
    Then I fetch credit card constants for HUGOBANK

    And I validate credit card eligibility using balance of the wallet with product code CASH_WALLET_CURRENT for user UID1
      | credit_limit  |
      | 20000         |

    Then I initiate the initial user authorisation to ORDER_CARD for user UID1 and expect a status of USER_AUTHORISATION_SUCCESS

    Then I initiate the final user authorisation to ORDER_CARD and expect a user authorisation status as USER_AUTHORISATION_INITIATED for user UID1

    And I initiate the PASSCODE journey within the PASSCODE_STEP for user UID1 to authorise the user and expect a status JOURNEY_INITIATED

    Then I process the PASSCODE journey within the PASSCODE_STEP for user UID1 to authorise the user and expect a status JOURNEY_PROCESSED

    And I submit the PASSCODE journey within the PASSCODE_STEP for user UID1 to authorise the user and expect a status JOURNEY_SUCCESSFUL

    Then I submit the final user authorisation for ORDER_CARD of user UID1 and expect a status USER_AUTHORISATION_SUBMITTED

    And I get the final user authorisation token for ORDER_CARD of user UID1 and expect a status USER_AUTHORISATION_SUCCESS

    Then I order a Physical Visa Credit Card for UID1 with card name as random_valid_choice and expect a status code of 200 and expect a card status of CARD_STATUS_PENDING
      | credit_limit  |
      | 20000         |

    Then I initiate the initial user authorisation to ACTIVATE_CARD for user UID1 and expect a status of USER_AUTHORISATION_SUCCESS

    Then I initiate the final user authorisation to ACTIVATE_CARD and expect a user authorisation status as USER_AUTHORISATION_INITIATED for user UID1

    And I initiate the PASSCODE journey within the PASSCODE_STEP for user UID1 to authorise the user and expect a status JOURNEY_INITIATED

    Then I process the PASSCODE journey within the PASSCODE_STEP for user UID1 to authorise the user and expect a status JOURNEY_PROCESSED

    And I submit the PASSCODE journey within the PASSCODE_STEP for user UID1 to authorise the user and expect a status JOURNEY_SUCCESSFUL

    Then I submit the final user authorisation for ACTIVATE_CARD of user UID1 and expect a status USER_AUTHORISATION_SUBMITTED

    And I get the final user authorisation token for ACTIVATE_CARD of user UID1 and expect a status USER_AUTHORISATION_SUCCESS

    Then I wait for 40 seconds

    Then I wait for credit card status as CARD_STATUS_UPGRADED to activate PHYSICAL card for user UID1

    Then I wait for 10 seconds

    Then I activate the PHYSICAL card for the user UID1 with valid token, with status 200

    Then I check card status is CARD_STATUS_ACTIVE for user UID1 for PHYSICAL card

    Then I fetch credit account list for user UID1
#-----------------------------------------------------------------------------------------------------

    And I fetch credit account balance for user UID1

    # Store snapshot before replacement
    And I store credit card replacement details for user UID1

    Then I initiate the initial user authorisation to REPLACE_CARD for user UID1 and expect a status of USER_AUTHORISATION_SUCCESS

    Then I initiate the final user authorisation to REPLACE_CARD and expect a user authorisation status as USER_AUTHORISATION_INITIATED for user UID1

    And I initiate the PASSCODE journey within the PASSCODE_STEP for user UID1 to authorise the user and expect a status JOURNEY_INITIATED

    Then I process the PASSCODE journey within the PASSCODE_STEP for user UID1 to authorise the user and expect a status JOURNEY_PROCESSED

    And I submit the PASSCODE journey within the PASSCODE_STEP for user UID1 to authorise the user and expect a status JOURNEY_SUCCESSFUL

    Then I submit the final user authorisation for REPLACE_CARD of user UID1 and expect a status USER_AUTHORISATION_SUBMITTED

    And I get the final user authorisation token for REPLACE_CARD of user UID1 and expect a status USER_AUTHORISATION_SUCCESS


    Then I replace Physical credit card for user UID1 and expect a card status of CARD_STATUS_PENDING


    Then I check old card status is CARD_STATUS_DISABLED for user UID1

    Then I fetch credit account list for user UID1

    And I fetch credit account balance for user UID1

    And I verify credit account integrity after replacement for user UID1
