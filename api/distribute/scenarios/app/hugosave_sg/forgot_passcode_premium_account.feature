Feature: Forgot Passcode

  Background: Create a new User Account

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

  Scenario: Change Passcode

    Then I initiate forgot passcode for user UID1 and expect the status FORGOT_PASSCODE_INITIATED

    And I initiate the OTP journey within the OTP_STEP for user UID1 and expect a journey status of JOURNEY_INITIATED

    Then I process the OTP journey within the OTP_STEP for user UID1 and expect a journey status of JOURNEY_PROCESSED

    And I submit the OTP journey within the OTP_STEP for user UID1 and expect a journey status of JOURNEY_SUCCESSFUL

    And I submit forgot passcode of user UID1 and expect a status of FORGOT_PASSCODE_SUBMITTED

    And I get the forgot password token for user UID1 and expect a status of FORGOT_PASSCODE_SUCCESS

    And I update the password for user UID1 and expect a status code of 200
