Feature: Account management feature

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

  Scenario: Unbind user device

    Then I initiate the initial user authorisation to REMOVE_DEVICE for user UID1 and expect a status of USER_AUTHORISATION_SUCCESS

    Then I initiate the final user authorisation to REMOVE_DEVICE and expect a user authorisation status as USER_AUTHORISATION_INITIATED for user UID1

    And I initiate the PASSCODE journey within the PASSCODE_STEP for user UID1 to authorise the user and expect a status JOURNEY_INITIATED

    Then I process the PASSCODE journey within the PASSCODE_STEP for user UID1 to authorise the user and expect a status JOURNEY_PROCESSED

    And I submit the PASSCODE journey within the PASSCODE_STEP for user UID1 to authorise the user and expect a status JOURNEY_SUCCESSFUL

    Then I submit the final user authorisation for REMOVE_DEVICE of user UID1 and expect a status USER_AUTHORISATION_SUBMITTED

    And I get the final user authorisation token for REMOVE_DEVICE of user UID1 and expect a status USER_AUTHORISATION_SUCCESS

    Then I list all user devices for user UID1 and the user should have device_1

    Then I unbind the device_1 for user UID1 and expect a status code of 200

  Scenario: Bind multiple devices

    Then I log into the account of user UID1 on device_2 and the verification status should be VERIFICATION_INITIATED

    Then The user UID1 submits OTP to log into the user account from device_2 and expects a status VERIFICATION_SUCCESS

    Then I authenticate the user UID1 from device - device_2 and expect a status of AUTHENTICATION_SUCCESSFUL

    Then I authorise the device_2 for the user UID1 and expect the device authorisation status of DEVICE_LIMIT_EXCEEDED

  Scenario: Unbind a device and bind a new device, cool-off expected

    Then I initiate the initial user authorisation to REMOVE_DEVICE for user UID1 and expect a status of USER_AUTHORISATION_SUCCESS

    Then I initiate the final user authorisation to REMOVE_DEVICE and expect a user authorisation status as USER_AUTHORISATION_INITIATED for user UID1

    And I initiate the PASSCODE journey within the PASSCODE_STEP for user UID1 to authorise the user and expect a status JOURNEY_INITIATED

    Then I process the PASSCODE journey within the PASSCODE_STEP for user UID1 to authorise the user and expect a status JOURNEY_PROCESSED

    And I submit the PASSCODE journey within the PASSCODE_STEP for user UID1 to authorise the user and expect a status JOURNEY_SUCCESSFUL

    Then I submit the final user authorisation for REMOVE_DEVICE of user UID1 and expect a status USER_AUTHORISATION_SUBMITTED

    And I get the final user authorisation token for REMOVE_DEVICE of user UID1 and expect a status USER_AUTHORISATION_SUCCESS

    Then I list all user devices for user UID1 and the user should have device_1

    Then I unbind the device_1 for user UID1 and expect a status code of 200

    Then I log into the account of user UID1 on device_2 and the verification status should be VERIFICATION_INITIATED

    Then The user UID1 submits OTP to log into the user account from device_2 and expects a status VERIFICATION_SUCCESS

    Then I authenticate the user UID1 from device - device_2 and expect a status of AUTHENTICATION_SUCCESSFUL

    Then I authorise the device_2 for the user UID1 and expect the device authorisation status of DEVICE_AUTHORISATION_SUCCESS

    Then I check the authorisation status of the device_2 for the user UID1 and expect a device authorisation status of DEVICE_AUTHORISATION_SUCCESS

    And Create a binding signature for the user UID1 to bind the device_2 and the device binding status should be ACTIVE

    Given I list all user devices for user UID1 and the user should have device_2

    Then I initiate the initial user authorisation to ADD_PAYEE for user UID1 and expect cool-off

  Scenario: Block user profile

    Then I initiate the initial user authorisation to UPDATE_USER_PROFILE_STATUS for user UID1 and expect a status of USER_AUTHORISATION_SUCCESS

    Then I initiate the final user authorisation to UPDATE_USER_PROFILE_STATUS and expect a user authorisation status as USER_AUTHORISATION_INITIATED for user UID1

    And I initiate the PASSCODE journey within the PASSCODE_STEP for user UID1 to authorise the user and expect a status JOURNEY_INITIATED

    Then I process the PASSCODE journey within the PASSCODE_STEP for user UID1 to authorise the user and expect a status JOURNEY_PROCESSED

    And I submit the PASSCODE journey within the PASSCODE_STEP for user UID1 to authorise the user and expect a status JOURNEY_SUCCESSFUL

    Then I submit the final user authorisation for UPDATE_USER_PROFILE_STATUS of user UID1 and expect a status USER_AUTHORISATION_SUBMITTED

    And I get the final user authorisation token for UPDATE_USER_PROFILE_STATUS of user UID1 and expect a status USER_AUTHORISATION_SUCCESS

    Then I block user UID1 and expect a status code of 200

    Then I log into the account of user UID1 on device_1 and the verification status should be VERIFICATION_INITIATED

    Then The user UID1 submits OTP to log into the user account from device_1 and expects a status VERIFICATION_SUCCESS

    Then I authenticate the user UID1 from device - device_1 and expect a status of AUTHENTICATION_FAILED
