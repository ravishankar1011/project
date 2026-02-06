Feature: Payee scenarios for a LITE account

  Background: Create 2 HUGOBANK LITE accounts to test payee scenarios

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

    # user 2
    Given The user UID2 provides a valid mobile number on device_1 to initiate onboarding and the expected status is VERIFICATION_INITIATED
      | user_name | user_name_type | ph_prefix |
      | random    | PHONE_NUMBER   | +373      |

    Then The user UID2 submits OTP to proceed with verification and expects a status code of 200 and a status of VERIFICATION_SUCCESS

    Given I open a new HUGOBANK user account and expect the status code 200
      | user_profile_identifier | email          | legal_name | name   | account_type |
      | UID2                    | test@gmail.com | John Doe   | Johnny | PERSONAL     |

    Then I initiate the initial onboarding of the user UID2 and expect a status INITIATED

    Then I initiate the initial onboarding journey HUGOBANK_VERISYS within the ID_VERIFICATION_STEP for the user UID2 and expect a status of JOURNEY_INITIATED

    Then I update HUGOBANK_VERISYS journey within the ID_VERIFICATION_STEP for user UID2 as pass

    Then I process the initial onboarding journey HUGOBANK_VERISYS within the ID_VERIFICATION_STEP for user UID2, and expect a status JOURNEY_PROCESSED

    Then I check status of the initial onboarding journey HUGOBANK_VERISYS within the ID_VERIFICATION_STEP for the user UID2, the status should be JOURNEY_PROCESSED

    Then I submit the initial onboarding journey HUGOBANK_VERISYS within the ID_VERIFICATION_STEP for the user UID2 and expect the journey status to be JOURNEY_SUBMITTED

    Then I check status of the initial onboarding journey HUGOBANK_VERISYS within the ID_VERIFICATION_STEP for the user UID2, the status should be JOURNEY_SUCCESSFUL

    Then I initiate the initial onboarding journey HUGOBANK_BIO_VERISYS within the BIOMETRIC_VERIFICATION_STEP for the user UID2 and expect a status of JOURNEY_INITIATED

    Then I update HUGOBANK_BIO_VERISYS journey within the BIOMETRIC_VERIFICATION_STEP for user UID2 as pass

    Then I process the initial onboarding journey HUGOBANK_BIO_VERISYS within the BIOMETRIC_VERIFICATION_STEP for user UID2, and expect a status JOURNEY_PROCESSED

    Then I check status of the initial onboarding journey HUGOBANK_BIO_VERISYS within the BIOMETRIC_VERIFICATION_STEP for the user UID2, the status should be JOURNEY_PROCESSED

    Then I submit the initial onboarding journey HUGOBANK_BIO_VERISYS within the BIOMETRIC_VERIFICATION_STEP for the user UID2 and expect the journey status to be JOURNEY_SUBMITTED

    Then I submit the initial onboarding for UID2, the onboarding status should be IN_PROGRESS and the account level should be L1

    And I check the status of initial onboarding for UID2 and expect a onboarding status of COMPLETED

    And I get user details for user UID2 and the user profile status should be PROFILE_IN_PROGRESS

    Then I check the authorisation status of the device_1 for the user UID2 and expect a device authorisation status of DEVICE_AUTHORISATION_SUCCESS

    And Create a binding signature for the user UID2 to bind the device_1 and the device binding status should be ACTIVE

    Then I list all user devices for user UID2 and the user should have device_1

    And I check the user details to confirm if user UID2 is L1 and the user profile status should be PROFILE_ACTIVE

  Scenario: Add payee using IBAN Number

    Then I initiate the initial user authorisation to ADD_PAYEE for user UID1 and expect a status of USER_AUTHORISATION_SUCCESS

    Then I initiate the final user authorisation to ADD_PAYEE and expect a user authorisation status as USER_AUTHORISATION_INITIATED for user UID1

    And I initiate the OTP journey within the OTP_STEP for user UID1 to authorise the user and expect a status JOURNEY_INITIATED

    Then I process the OTP journey within the OTP_STEP for user UID1 to authorise the user and expect a status JOURNEY_PROCESSED

    And I submit the OTP journey within the OTP_STEP for user UID1 to authorise the user and expect a status JOURNEY_SUCCESSFUL

    And I initiate the PASSCODE journey within the PASSCODE_STEP for user UID1 to authorise the user and expect a status JOURNEY_INITIATED

    Then I process the PASSCODE journey within the PASSCODE_STEP for user UID1 to authorise the user and expect a status JOURNEY_PROCESSED

    And I submit the PASSCODE journey within the PASSCODE_STEP for user UID1 to authorise the user and expect a status JOURNEY_SUCCESSFUL

    Then I submit the final user authorisation for ADD_PAYEE of user UID1 and expect a status USER_AUTHORISATION_SUBMITTED

    And I get the final user authorisation token for ADD_PAYEE of user UID1 and expect a status USER_AUTHORISATION_SUCCESS

    Then I get the user cash wallets for the user UID2 and expect the account status of CASH_ACCOUNT_STATUS_CREATED

    Then I add the wallet with product code CASH_WALLET_CURRENT of user UID2 to user UID1 as payee PID1 with valid_iban and expect a status code of 200 and a status of BENEFICIARY_STATUS_PENDING

    And I check if the wallet with product code CASH_WALLET_CURRENT of user UID2 is added as payee to user UID1 and expect a status of BENEFICIARY_STATUS_CREATED

    # edit details
    And I edit the payee UID2 details for the user UID1 and expect a status code of 200

    Then I check if the payee UID2 details are updated for the user UID1 and expect a status of BENEFICIARY_STATUS_CREATED

  Scenario: Add payee using Account Number, edit payee details

    Then I initiate the initial user authorisation to ADD_PAYEE for user UID1 and expect a status of USER_AUTHORISATION_SUCCESS

    Then I initiate the final user authorisation to ADD_PAYEE and expect a user authorisation status as USER_AUTHORISATION_INITIATED for user UID1

    And I initiate the OTP journey within the OTP_STEP for user UID1 to authorise the user and expect a status JOURNEY_INITIATED

    Then I process the OTP journey within the OTP_STEP for user UID1 to authorise the user and expect a status JOURNEY_PROCESSED

    And I submit the OTP journey within the OTP_STEP for user UID1 to authorise the user and expect a status JOURNEY_SUCCESSFUL

    And I initiate the PASSCODE journey within the PASSCODE_STEP for user UID1 to authorise the user and expect a status JOURNEY_INITIATED

    Then I process the PASSCODE journey within the PASSCODE_STEP for user UID1 to authorise the user and expect a status JOURNEY_PROCESSED

    And I submit the PASSCODE journey within the PASSCODE_STEP for user UID1 to authorise the user and expect a status JOURNEY_SUCCESSFUL

    Then I submit the final user authorisation for ADD_PAYEE of user UID1 and expect a status USER_AUTHORISATION_SUBMITTED

    And I get the final user authorisation token for ADD_PAYEE of user UID1 and expect a status USER_AUTHORISATION_SUCCESS

    Then I get the user cash wallets for the user UID2 and expect the account status of CASH_ACCOUNT_STATUS_CREATED

    Then I add the wallet with product code CASH_WALLET_CURRENT of user UID2 to user UID1 as payee PID1 with valid_swift_bic and expect a status code of 200 and a status of BENEFICIARY_STATUS_PENDING

    And I check if the wallet with product code CASH_WALLET_CURRENT of user UID2 is added as payee to user UID1 and expect a status of BENEFICIARY_STATUS_CREATED

    # edit details
    And I edit the payee UID2 details for the user UID1 and expect a status code of 200

    Then I check if the payee UID2 details are updated for the user UID1 and expect a status of BENEFICIARY_STATUS_CREATED

  Scenario: Add Payee, Pay Payee

    Then I initiate the initial user authorisation to ADD_PAYEE for user UID1 and expect a status of USER_AUTHORISATION_SUCCESS

    Then I initiate the final user authorisation to ADD_PAYEE and expect a user authorisation status as USER_AUTHORISATION_INITIATED for user UID1

    And I initiate the OTP journey within the OTP_STEP for user UID1 to authorise the user and expect a status JOURNEY_INITIATED

    Then I process the OTP journey within the OTP_STEP for user UID1 to authorise the user and expect a status JOURNEY_PROCESSED

    And I submit the OTP journey within the OTP_STEP for user UID1 to authorise the user and expect a status JOURNEY_SUCCESSFUL

    And I initiate the PASSCODE journey within the PASSCODE_STEP for user UID1 to authorise the user and expect a status JOURNEY_INITIATED

    Then I process the PASSCODE journey within the PASSCODE_STEP for user UID1 to authorise the user and expect a status JOURNEY_PROCESSED

    And I submit the PASSCODE journey within the PASSCODE_STEP for user UID1 to authorise the user and expect a status JOURNEY_SUCCESSFUL

    Then I submit the final user authorisation for ADD_PAYEE of user UID1 and expect a status USER_AUTHORISATION_SUBMITTED

    And I get the final user authorisation token for ADD_PAYEE of user UID1 and expect a status USER_AUTHORISATION_SUCCESS

    Then I get the user cash wallets for the user UID2 and expect the account status of CASH_ACCOUNT_STATUS_CREATED

    Then I add the wallet with product code CASH_WALLET_CURRENT of user UID2 to user UID1 as payee PID1 with valid_swift_bic and expect a status code of 200 and a status of BENEFICIARY_STATUS_PENDING

    And I check if the wallet with product code CASH_WALLET_CURRENT of user UID2 is added as payee to user UID1 and expect a status of BENEFICIARY_STATUS_CREATED

    Then I get the user cash wallets for the user UID1 and expect the account status of CASH_ACCOUNT_STATUS_CREATED

    Then I deposit 50 PKR into wallet with product code CASH_WALLET_CURRENT for user UID1 and expect a status code of 200

    And I check the balance of the wallet with product code CASH_WALLET_CURRENT for user UID1 and the balance should be 50 PKR exact

    Then I initiate the initial user authorisation to PAY_PAYEE for user UID1 and expect a status of USER_AUTHORISATION_SUCCESS

    Then I initiate the final user authorisation to PAY_PAYEE and expect a user authorisation status as USER_AUTHORISATION_INITIATED for user UID1 with below soft limit

    And I initiate the PASSCODE journey within the PASSCODE_STEP for user UID1 to authorise the user and expect a status JOURNEY_INITIATED

    Then I process the PASSCODE journey within the PASSCODE_STEP for user UID1 to authorise the user and expect a status JOURNEY_PROCESSED

    And I submit the PASSCODE journey within the PASSCODE_STEP for user UID1 to authorise the user and expect a status JOURNEY_SUCCESSFUL

    Then I submit the final user authorisation for PAY_PAYEE of user UID1 and expect a status USER_AUTHORISATION_SUBMITTED

    And I get the final user authorisation token for PAY_PAYEE of user UID1 and expect a status USER_AUTHORISATION_SUCCESS

    Then I transfer 20 PKR from user UID1 to user UID2 with no reference and valid payee id and expect a status code of 200

    And I check the balance of the wallet with product code CASH_WALLET_CURRENT for user UID1 and the balance should be 30 PKR exact

    And I check the balance of the wallet with product code CASH_WALLET_CURRENT for user UID2 and the balance should be 20 PKR exact

    Then I add a random note to the latest intent of user UID1 and check if note is saved

  Scenario: Add Payee, Pay Payee using Raast (virtual ID)

    Then I get the user cash wallets for the user UID2 and expect the account status of CASH_ACCOUNT_STATUS_CREATED

    Then I initiate the initial user authorisation to CREATE_VIRTUAL_ID for user UID2 and expect a status of USER_AUTHORISATION_SUCCESS

    Then I initiate the final user authorisation to CREATE_VIRTUAL_ID and expect a user authorisation status as USER_AUTHORISATION_SUCCESS for user UID2

    Then I create a virtual ID for the user UID2

    Then I initiate the initial user authorisation to LINK_VIRTUAL_ID for user UID2 and expect a status of USER_AUTHORISATION_SUCCESS

    Then I initiate the final user authorisation to LINK_VIRTUAL_ID and expect a user authorisation status as USER_AUTHORISATION_SUCCESS for user UID2

    Then I link the raast ID for the user UID2

    Then I initiate the initial user authorisation to ADD_PAYEE for user UID1 and expect a status of USER_AUTHORISATION_SUCCESS

    Then I initiate the final user authorisation to ADD_PAYEE and expect a user authorisation status as USER_AUTHORISATION_INITIATED for user UID1

    And I initiate the OTP journey within the OTP_STEP for user UID1 to authorise the user and expect a status JOURNEY_INITIATED

    Then I process the OTP journey within the OTP_STEP for user UID1 to authorise the user and expect a status JOURNEY_PROCESSED

    And I submit the OTP journey within the OTP_STEP for user UID1 to authorise the user and expect a status JOURNEY_SUCCESSFUL

    And I initiate the PASSCODE journey within the PASSCODE_STEP for user UID1 to authorise the user and expect a status JOURNEY_INITIATED

    Then I process the PASSCODE journey within the PASSCODE_STEP for user UID1 to authorise the user and expect a status JOURNEY_PROCESSED

    And I submit the PASSCODE journey within the PASSCODE_STEP for user UID1 to authorise the user and expect a status JOURNEY_SUCCESSFUL

    Then I submit the final user authorisation for ADD_PAYEE of user UID1 and expect a status USER_AUTHORISATION_SUBMITTED

    And I get the final user authorisation token for ADD_PAYEE of user UID1 and expect a status USER_AUTHORISATION_SUCCESS

    Then I add the user UID2 as Payee PID1 to the user UID1 using raast ID

    And I check if the raast ID of user UID2 is added as payee PID1 to user UID1

    Then I get the user cash wallets for the user UID1 and expect the account status of CASH_ACCOUNT_STATUS_CREATED

    Then I deposit 50 PKR into wallet with product code CASH_WALLET_CURRENT for user UID1 and expect a status code of 200

    And I check the balance of the wallet with product code CASH_WALLET_CURRENT for user UID1 and the balance should be 50 PKR exact

    Then I initiate the initial user authorisation to PAY_PAYEE for user UID1 and expect a status of USER_AUTHORISATION_SUCCESS

    Then I initiate the final user authorisation to PAY_PAYEE and expect a user authorisation status as USER_AUTHORISATION_INITIATED for user UID1

    And I initiate the PASSCODE journey within the PASSCODE_STEP for user UID1 to authorise the user and expect a status JOURNEY_INITIATED

    Then I process the PASSCODE journey within the PASSCODE_STEP for user UID1 to authorise the user and expect a status JOURNEY_PROCESSED

    And I submit the PASSCODE journey within the PASSCODE_STEP for user UID1 to authorise the user and expect a status JOURNEY_SUCCESSFUL

    Then I submit the final user authorisation for PAY_PAYEE of user UID1 and expect a status USER_AUTHORISATION_SUBMITTED

    And I get the final user authorisation token for PAY_PAYEE of user UID1 and expect a status USER_AUTHORISATION_SUCCESS

    Then I transfer 20 PKR from user UID1 to user UID2 with no reference and valid payee id and expect a status code of 200

    And I check the balance of the wallet with product code CASH_WALLET_CURRENT for user UID1 and the balance should be 30 PKR exact

    And I check the balance of the wallet with product code CASH_WALLET_CURRENT for user UID2 and the balance should be 20 PKR exact

    Then I add a random note to the latest intent of user UID1 and check if note is saved

  Scenario: Pay Payee Using Static QR code

    Then I get the user cash wallets for the user UID1 and expect the account status of CASH_ACCOUNT_STATUS_CREATED

    Given I deposit 50 PKR into wallet with product code CASH_WALLET_CURRENT for user UID1 and expect a status code of 200

    And I check the balance of the wallet with product code CASH_WALLET_CURRENT for user UID1 and the balance should be 50 PKR exact

    Then I get the user cash wallets for the user UID2 and expect the account status of CASH_ACCOUNT_STATUS_CREATED

    And I get QR code for user UID2

    And I get the user UID2 transfer out account details using Valid QR code and expect a status of BENEFICIARY_STATUS_PENDING

    Then I initiate the initial user authorisation to PAY_PAYEE for user UID1 and expect a status of USER_AUTHORISATION_SUCCESS

    Then I initiate the final user authorisation to PAY_PAYEE and expect a user authorisation status as USER_AUTHORISATION_INITIATED for user UID1 with below soft limit

    And I initiate the PASSCODE journey within the PASSCODE_STEP for user UID1 to authorise the user and expect a status JOURNEY_INITIATED

    Then I process the PASSCODE journey within the PASSCODE_STEP for user UID1 to authorise the user and expect a status JOURNEY_PROCESSED

    And I submit the PASSCODE journey within the PASSCODE_STEP for user UID1 to authorise the user and expect a status JOURNEY_SUCCESSFUL

    Then I submit the final user authorisation for PAY_PAYEE of user UID1 and expect a status USER_AUTHORISATION_SUBMITTED

    And I get the final user authorisation token for PAY_PAYEE of user UID1 and expect a status USER_AUTHORISATION_SUCCESS

    And I wait for 5 seconds

    Then I transfer 20 PKR from user UID1 to user UID2 using Static QR code

    And I check the balance of the wallet with product code CASH_WALLET_CURRENT for user UID1 and the balance should be 30 PKR exact

  Scenario: Pay Payee Using Dynamic QR code

    Then I get the user cash wallets for the user UID2 and expect the account status of CASH_ACCOUNT_STATUS_CREATED

    Given I create dynamic QR code with amount 50 PKR for user UID2

    Then I get the user cash wallets for the user UID1 and expect the account status of CASH_ACCOUNT_STATUS_CREATED

    Given I deposit 100 PKR into wallet with product code CASH_WALLET_CURRENT for user UID1 and expect a status code of 200

    And I check the balance of the wallet with product code CASH_WALLET_CURRENT for user UID1 and the balance should be 100 PKR exact

    And I get the user UID2 transfer out account details using Valid QR code and expect a status of BENEFICIARY_STATUS_PENDING

    Then I initiate the initial user authorisation to PAY_PAYEE for user UID1 and expect a status of USER_AUTHORISATION_SUCCESS

    Then I initiate the final user authorisation to PAY_PAYEE and expect a user authorisation status as USER_AUTHORISATION_INITIATED for user UID1 with below soft limit

    And I initiate the PASSCODE journey within the PASSCODE_STEP for user UID1 to authorise the user and expect a status JOURNEY_INITIATED

    Then I process the PASSCODE journey within the PASSCODE_STEP for user UID1 to authorise the user and expect a status JOURNEY_PROCESSED

    And I submit the PASSCODE journey within the PASSCODE_STEP for user UID1 to authorise the user and expect a status JOURNEY_SUCCESSFUL

    Then I submit the final user authorisation for PAY_PAYEE of user UID1 and expect a status USER_AUTHORISATION_SUBMITTED

    And I get the final user authorisation token for PAY_PAYEE of user UID1 and expect a status USER_AUTHORISATION_SUCCESS

    And I wait for 5 seconds

    Then I transfer 50 PKR from user UID1 to user UID2 using Dynamic QR code

    And I check the balance of the wallet with product code CASH_WALLET_CURRENT for user UID1 and the balance should be 50 PKR exact

    And I check the balance of the wallet with product code CASH_WALLET_CURRENT for user UID2 and the balance should be 50 PKR exact

  Scenario: Delete Payee

    Then I initiate the initial user authorisation to ADD_PAYEE for user UID1 and expect a status of USER_AUTHORISATION_SUCCESS

    Then I initiate the final user authorisation to ADD_PAYEE and expect a user authorisation status as USER_AUTHORISATION_INITIATED for user UID1

    And I initiate the OTP journey within the OTP_STEP for user UID1 to authorise the user and expect a status JOURNEY_INITIATED

    Then I process the OTP journey within the OTP_STEP for user UID1 to authorise the user and expect a status JOURNEY_PROCESSED

    And I submit the OTP journey within the OTP_STEP for user UID1 to authorise the user and expect a status JOURNEY_SUCCESSFUL

    And I initiate the PASSCODE journey within the PASSCODE_STEP for user UID1 to authorise the user and expect a status JOURNEY_INITIATED

    Then I process the PASSCODE journey within the PASSCODE_STEP for user UID1 to authorise the user and expect a status JOURNEY_PROCESSED

    And I submit the PASSCODE journey within the PASSCODE_STEP for user UID1 to authorise the user and expect a status JOURNEY_SUCCESSFUL

    Then I submit the final user authorisation for ADD_PAYEE of user UID1 and expect a status USER_AUTHORISATION_SUBMITTED

    And I get the final user authorisation token for ADD_PAYEE of user UID1 and expect a status USER_AUTHORISATION_SUCCESS

    Then I get the user cash wallets for the user UID2 and expect the account status of CASH_ACCOUNT_STATUS_CREATED

    Then I add the wallet with product code CASH_WALLET_CURRENT of user UID2 to user UID1 as payee PID1 with valid_swift_bic and expect a status code of 200 and a status of BENEFICIARY_STATUS_PENDING

    And I check if the wallet with product code CASH_WALLET_CURRENT of user UID2 is added as payee to user UID1 and expect a status of BENEFICIARY_STATUS_CREATED

    Given I delete the payee UID2 added to user UID1

    Then I wait for 10 seconds

    And I check if the wallet with product code CASH_WALLET_CURRENT of user UID2 is not_added as payee to user UID1 and expect a status of BENEFICIARY_STATUS_CREATED
