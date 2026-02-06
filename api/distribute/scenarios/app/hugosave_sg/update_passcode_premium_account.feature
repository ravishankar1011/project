Feature: Update user passcode for a Hugosave PREMIUM Account

  Background: Open a Hugosave PREMIUM Account

    Given The user UID1 provides a valid mobile number on device_1 to initiate onboarding and the expected status is VERIFICATION_INITIATED
      | user_name | user_name_type | ph_prefix |
      | random    | PHONE_NUMBER   | +378      |

    Then The user UID1 submits OTP to proceed with verification and expects a status code of 200 and a status of VERIFICATION_SUCCESS

    Given I open a new HUGOSAVE user account and expect the status code 200
      | user_profile_identifier | email          | legal_name | name   | account_type |
      | UID1                    | test@gmail.com | John Doe   | Johnny | PERSONAL     |

    Then I check the authorisation status of the device_1 for the user UID1 and expect a device authorisation status of DEVICE_AUTHORISATION_SUCCESS

    And Create a binding signature for the user UID1 to bind the device_1 and the device binding status should be ACTIVE

    And I check the user details to confirm if user UID1 is L3 and the user profile status should be PROFILE_ACTIVE

  Scenario: Update the PREMIUM user Passcode

    Then I initiate the initial user authorisation to UPDATE_PASSCODE for user UID1 and expect a status of USER_AUTHORISATION_SUCCESS

    Then I initiate the final user authorisation to UPDATE_PASSCODE and expect a user authorisation status as USER_AUTHORISATION_SUCCESS for user UID1

    Then I update passcode for the user UID1 and expect a status code of 200

    Then I log into the account of user UID1 on device_1 and the verification status should be VERIFICATION_INITIATED

    Then The user UID1 submits OTP to log into the user account from device_1 and expects a status VERIFICATION_SUCCESS

    Given I enter the current passcode for the user UID1 and expect an authentication status of AUTHENTICATION_SUCCESSFUL

  Scenario: Test incorrect passcode scenario

    Given I enter incorrect passcode for the user UID1 and expect a status of AUTHENTICATION_FAILED
