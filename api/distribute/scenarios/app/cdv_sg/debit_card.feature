Feature:  Create a new debit card

  Background: : Create a new account for a user

    Given The user UID1 provides a valid mobile number on device_1 to initiate onboarding and the expected status is VERIFICATION_INITIATED
      | user_name | user_name_type |
      | random    | EMAIL_ADDRESS  |

    Then The user UID1 submits OTP to proceed with verification and expects a status code of 200 and a status of VERIFICATION_SUCCESS

    Given I open a new CDV user account and expect the status code 200
      | user_profile_identifier |  | legal_name | name   | account_type |
      | UID1                    |  | John Doe   | Johnny | PERSONAL     |

    Then I initiate the initial onboarding of the user UID1 and expect a status INITIATED

    Then I initiate the initial onboarding journey ONFIDO within the ID_VERIFICATION_STEP for the user UID1 and expect a status of JOURNEY_PROCESSING

    Then I process the initial onboarding journey ONFIDO within the ID_VERIFICATION_STEP for user UID1, and expect a status JOURNEY_PROCESSED

    Then I check status of the initial onboarding journey ONFIDO within the ID_VERIFICATION_STEP for the user UID1, the status should be JOURNEY_PROCESSED

    Then I submit the initial onboarding journey ONFIDO within the ID_VERIFICATION_STEP for the user UID1 and expect the journey status to be JOURNEY_SUCCESSFUL

    Then I initiate the initial onboarding journey CDV_CDC_DOCUMENT within the DOCUMENT_UPLOAD_STEP for the user UID1 and expect a status of JOURNEY_INITIATED

    Then I upload document1 for cdcDocument for the CDV_CDC_DOCUMENT journey for user UID1 as the cdcDocument

    Then I process the initial onboarding journey CDV_CDC_DOCUMENT within the DOCUMENT_UPLOAD_STEP for user UID1, and expect a status JOURNEY_HOLD

    Then I update the CDV_CDC_DOCUMENT journey status within the DOCUMENT_UPLOAD_STEP as ACCEPT if operator action status is OPERATOR_ACTION_REQUIRED for user UID1

    Then I initiate the initial onboarding journey CDV_ADDITIONAL_DETAILS within the ADDITIONAL_DETAILS_STEP for the user UID1 and expect a status of JOURNEY_INITIATED

    Then I upload document1 for addressProof for the CDV_ADDITIONAL_DETAILS journey for user UID1 as the addressProof

    Then I process the initial onboarding journey CDV_ADDITIONAL_DETAILS within the ADDITIONAL_DETAILS_STEP for user UID1, and expect a status JOURNEY_HOLD

    Then I update the CDV_ADDITIONAL_DETAILS journey status within the ADDITIONAL_DETAILS_STEP as ACCEPT if operator action status is OPERATOR_ACTION_REQUIRED for user UID1

    Then I submit the initial onboarding for UID1, the onboarding status should be IN_PROGRESS and the account level should be L1

    And I check the status of initial onboarding for UID1 and expect a onboarding status of COMPLETED

    And I get user details for user UID1 and the user profile status should be PROFILE_IN_PROGRESS

    Then I check the authorisation status of the device_1 for the user UID1 and expect a device authorisation status of DEVICE_AUTHORISATION_SUCCESS

    And Create a binding signature for the user UID1 to bind the device_1 and the device binding status should be ACTIVE

    Then I list all user devices for user UID1 and the user should have device_1

    And I check the user details to confirm if user UID1 is L1 and the user profile status should be PROFILE_ACTIVE

  Scenario: Order Card -> Activate -> Block/Unblock -> Disable

    Then I order a physical card for UID1 with card name as random_valid_choice and expect a status code of 200 and expect a card status of CARD_STATUS_PENDING

    Then I wait for 10 seconds

    Then I get the user cash wallets for the user UID1 and expect the account status of CASH_ACCOUNT_STATUS_CREATED

    Then I wait for card status as CARD_STATUS_UPGRADED to activate PHYSICAL card for user UID1

    Then I wait for 40 seconds

    Then I activate the PHYSICAL card for the user UID1 with valid token, with status 200

    Then I check card status is CARD_STATUS_ACTIVE for user UID1 for PHYSICAL card

    Then I update the card status of the PHYSICAL card to BLOCK for user UID1 and expect a status code of 200

    Then I check card status is CARD_STATUS_BLOCKED for user UID1 for PHYSICAL card

    Then I update the card status of the PHYSICAL card to UNBLOCK for user UID1 and expect a status code of 200

    Then I check card status is CARD_STATUS_ACTIVE for user UID1 for PHYSICAL card

    Then I update the card status of the PHYSICAL card to DISABLE for user UID1 and expect a status code of 200

    Then I check card status is CARD_STATUS_DISABLED for user UID1 for PHYSICAL card

  Scenario: Order Card -> Activate -> Do a card transaction

    Then I get the user cash wallets for the user UID1 and expect the account status of CASH_ACCOUNT_STATUS_CREATED

    Then I deposit 1000 USD into wallet with product code CASH_WALLET_DIGITAL for user UID1 and expect a status code of 200

    And I check the balance of the wallet with product code CASH_WALLET_DIGITAL for user UID1 and the balance should be 1000 USD exact

    Then I order a physical card for UID1 with card name as random_valid_choice and expect a status code of 200 and expect a card status of CARD_STATUS_PENDING

    Then I wait for 10 seconds

    Then I get the user cash wallets for the user UID1 and expect the account status of CASH_ACCOUNT_STATUS_CREATED

    Then I wait for card status as CARD_STATUS_UPGRADED to activate PHYSICAL card for user UID1

    Then I wait for 25 seconds

    Then I activate the PHYSICAL card for the user UID1 with valid token, with status 200

    Then I check card status is CARD_STATUS_ACTIVE for user UID1 for PHYSICAL card

    Given I create below transaction for PHYSICAL card for user profile id and expect a status code of 200
      | user_profile_identifier | transaction_permutation_name | billing_amount | is_foreign_txn | channel |
      | UID1                    | AUTH_CLEAR                   | 500            | false          | POS     |

    And I check the balance of the wallet with product code CASH_WALLET_DIGITAL for user UID1 and the balance should be 500 USD exact

