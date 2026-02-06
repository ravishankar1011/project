Feature: Integration test of Document Center for LITE account

  Background: Create a HUGOBANK LITE account

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

  Scenario: Generate Transaction Statement for user

    Given I get all the user document types for user UID1 and expect a status code of 200

    Then I get the user cash wallets for the user UID1 and expect the account status of CASH_ACCOUNT_STATUS_CREATED

    Then I deposit 100 PKR into wallet with product code CASH_WALLET_CURRENT for user UID1 and expect a status code of 200

    And I check the balance of the wallet with product code CASH_WALLET_CURRENT for user UID1 and the balance should be 100 PKR exact

    Then I generate a STATEMENT of type TRANSACTION_STATEMENT for user UID1 for the CASH_WALLET account

    And I check the balance of the wallet with product code CASH_WALLET_CURRENT for user UID1 and the balance should be 90 PKR exact

    And I get the STATEMENT of type TRANSACTION_STATEMENT for user UID1

  Scenario: Generate Account Balance Certificate for user

    Given I get all the user document types for user UID1 and expect a status code of 200

    Then I get the user cash wallets for the user UID1 and expect the account status of CASH_ACCOUNT_STATUS_CREATED

    Then I deposit 100 PKR into wallet with product code CASH_WALLET_CURRENT for user UID1 and expect a status code of 200

    And I check the balance of the wallet with product code CASH_WALLET_CURRENT for user UID1 and the balance should be 100 PKR exact

    Then I generate a CERTIFICATE of type ACCOUNT_BALANCE_CERTIFICATE for user UID1 for the CASH_WALLET account

    And I check the balance of the wallet with product code CASH_WALLET_CURRENT for user UID1 and the balance should be 90 PKR exact

    And I get the CERTIFICATE of type ACCOUNT_BALANCE_CERTIFICATE for user UID1

  Scenario: Generate Account Maintenance Certificate for user

    Given I get all the user document types for user UID1 and expect a status code of 200

    Then I get the user cash wallets for the user UID1 and expect the account status of CASH_ACCOUNT_STATUS_CREATED

    Then I deposit 100 PKR into wallet with product code CASH_WALLET_CURRENT for user UID1 and expect a status code of 200

    And I check the balance of the wallet with product code CASH_WALLET_CURRENT for user UID1 and the balance should be 100 PKR exact

    Then I generate a CERTIFICATE of type ACCOUNT_MAINTENANCE_CERTIFICATE for user UID1 for the CASH_WALLET account

    And I check the balance of the wallet with product code CASH_WALLET_CURRENT for user UID1 and the balance should be 90 PKR exact

    And I get the CERTIFICATE of type ACCOUNT_MAINTENANCE_CERTIFICATE for user UID1

  Scenario: Generate Withholding Tax Certificate Certificate for user

    Given I get all the user document types for user UID1 and expect a status code of 200

    Then I get the user cash wallets for the user UID1 and expect the account status of CASH_ACCOUNT_STATUS_CREATED

    Then I deposit 100 PKR into wallet with product code CASH_WALLET_CURRENT for user UID1 and expect a status code of 200

    And I check the balance of the wallet with product code CASH_WALLET_CURRENT for user UID1 and the balance should be 100 PKR exact

    Then I generate a CERTIFICATE of type WITHHOLDING_TAX_CERTIFICATE for user UID1 for the CASH_WALLET account

    And I check the balance of the wallet with product code CASH_WALLET_CURRENT for user UID1 and the balance should be 90 PKR exact

    And I get the CERTIFICATE of type WITHHOLDING_TAX_CERTIFICATE for user UID1
