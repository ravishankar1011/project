Feature: Update user passcode for a HUGOBANK LITE Account

  Background: Open a HUGOBANK LITE Account

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

  Scenario: Update the Passcode

    Then I initiate the initial user authorisation to UPDATE_PASSCODE for user UID1 and expect a status of USER_AUTHORISATION_INITIATED

    Then I initiate the HUGOBANK_BIO_VERISYS journey within the BIOMETRIC_VERIFICATION_STEP for user UID1 to authorise the user and expect a status JOURNEY_INITIATED

    Then I update HUGOBANK_BIO_VERISYS journey within the BIOMETRIC_VERIFICATION_STEP for user UID1 as pass

    Then I process the HUGOBANK_BIO_VERISYS journey within the BIOMETRIC_VERIFICATION_STEP for user UID1 to authorise the user and expect a status JOURNEY_PROCESSED

    Then I check status of HUGOBANK_BIO_VERISYS journey within the BIOMETRIC_VERIFICATION_STEP for the user UID1, the user authorisation journey status should be JOURNEY_PROCESSED

    Then I submit the HUGOBANK_BIO_VERISYS journey within the BIOMETRIC_VERIFICATION_STEP for user UID1 to authorise the user and expect a status JOURNEY_SUBMITTED

    Then I submit the initial user authorisation for UPDATE_PASSCODE for user UID1 and expect an user authorisation status of USER_AUTHORISATION_SUBMITTED

    And I check the status of initial user authorisation for user UID1 and expect an user authorisation status of USER_AUTHORISATION_SUCCESS

    Then I initiate the final user authorisation to UPDATE_PASSCODE and expect a user authorisation status as USER_AUTHORISATION_SUCCESS for user UID1

    Then I update passcode for the user UID1 and expect a status code of 200

    Then I log into the account of user UID1 on device_1 and the verification status should be VERIFICATION_INITIATED

    Then The user UID1 submits OTP to log into the user account from device_1 and expects a status VERIFICATION_SUCCESS

    Given I enter the current passcode for the user UID1 and expect an authentication status of AUTHENTICATION_SUCCESSFUL

  Scenario: Test incorrect passcode scenario

    Given I enter incorrect passcode for the user UID1 and expect a status of AUTHENTICATION_FAILED
