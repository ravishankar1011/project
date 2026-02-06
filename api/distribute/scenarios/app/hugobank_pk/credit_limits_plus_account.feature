Feature: Check Daily Receiving Limits for a plus user

  Background: Create a HUGOBANK PLUS accounts to test limits scenarios

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

  Scenario: I edit the User's Receiving Limits - receive more than set limit and receive exactly set limit amount

    Then I initiate the initial user authorisation to UPDATE_USER_TRANSACTION_LIMITS for user UID1 and expect a status of USER_AUTHORISATION_SUCCESS

    Then I initiate the final user authorisation to UPDATE_USER_TRANSACTION_LIMITS and expect a user authorisation status as USER_AUTHORISATION_INITIATED for user UID1

    And I initiate the PASSCODE journey within the PASSCODE_STEP for user UID1 to authorise the user and expect a status JOURNEY_INITIATED

    Then I process the PASSCODE journey within the PASSCODE_STEP for user UID1 to authorise the user and expect a status JOURNEY_PROCESSED

    And I submit the PASSCODE journey within the PASSCODE_STEP for user UID1 to authorise the user and expect a status JOURNEY_SUCCESSFUL

    Then I submit the final user authorisation for UPDATE_USER_TRANSACTION_LIMITS of user UID1 and expect a status USER_AUTHORISATION_SUBMITTED

    And I get the final user authorisation token for UPDATE_USER_TRANSACTION_LIMITS of user UID1 and expect a status USER_AUTHORISATION_SUCCESS

    Given I edit the External Credit limits for user UID1 to 150000 PKR and expect a status code of 200

    Then I check if the hard limits are updated to 150000 for user UID1

    Then I get the user cash wallets for the user UID1 and expect the account status of CASH_ACCOUNT_STATUS_CREATED

    # receive - above set limits
    Then I deposit 150100 PKR which is more than daily receiving limit of into wallet with product code CASH_WALLET_CURRENT to check limits for user UID1 and expect a status of 200

    And I check the balance of the wallet with product code CASH_WALLET_CURRENT for user UID1 and the balance should be 0 PKR exact

    # receive - exact set limits
    Then I deposit 150000 PKR into wallet with product code CASH_WALLET_CURRENT for user UID1 and expect a status code of 200

    And I check the balance of the wallet with product code CASH_WALLET_CURRENT for user UID1 and the balance should be 150000 PKR exact

  Scenario: check the default limits (2000000 PKR)

    Then I get the user cash wallets for the user UID1 and expect the account status of CASH_ACCOUNT_STATUS_CREATED

    # receive - above default limit (2000000 PKR)
    Then I deposit 2000100 PKR which is more than daily receiving limit of into wallet with product code CASH_WALLET_CURRENT to check limits for user UID1 and expect a status of 200

    And I check the balance of the wallet with product code CASH_WALLET_CURRENT for user UID1 and the balance should be 0 PKR exact

    # receive - exactly default limit (200000 PKR)
    Then I deposit 2000000 PKR into wallet with product code CASH_WALLET_CURRENT for user UID1 and expect a status code of 200

    And I check the balance of the wallet with product code CASH_WALLET_CURRENT for user UID1 and the balance should be 2000000 PKR exact

  Scenario: I edit the User's Receiving Limits - Set the Minimum amount - 0 PKR and check

    Then I initiate the initial user authorisation to UPDATE_USER_TRANSACTION_LIMITS for user UID1 and expect a status of USER_AUTHORISATION_SUCCESS

    Then I initiate the final user authorisation to UPDATE_USER_TRANSACTION_LIMITS and expect a user authorisation status as USER_AUTHORISATION_INITIATED for user UID1

    And I initiate the PASSCODE journey within the PASSCODE_STEP for user UID1 to authorise the user and expect a status JOURNEY_INITIATED

    Then I process the PASSCODE journey within the PASSCODE_STEP for user UID1 to authorise the user and expect a status JOURNEY_PROCESSED

    And I submit the PASSCODE journey within the PASSCODE_STEP for user UID1 to authorise the user and expect a status JOURNEY_SUCCESSFUL

    Then I submit the final user authorisation for UPDATE_USER_TRANSACTION_LIMITS of user UID1 and expect a status USER_AUTHORISATION_SUBMITTED

    And I get the final user authorisation token for UPDATE_USER_TRANSACTION_LIMITS of user UID1 and expect a status USER_AUTHORISATION_SUCCESS

    Given I edit the External Credit limits for user UID1 to 0 PKR and expect a status code of 200

    Then I check if the hard limits are updated to 0 for user UID1

    Then I get the user cash wallets for the user UID1 and expect the account status of CASH_ACCOUNT_STATUS_CREATED

    # receive - above set limit (0 PKR)
    Then I deposit 1 PKR which is more than daily receiving limit of into wallet with product code CASH_WALLET_CURRENT to check limits for user UID1 and expect a status of 200

    And I check the balance of the wallet with product code CASH_WALLET_CURRENT for user UID1 and the balance should be 0 PKR exact

