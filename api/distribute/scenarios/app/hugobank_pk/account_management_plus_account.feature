Feature: Account Management for PLUS account

  Background: Create a new PLUS account

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

  Scenario: Bind 3 devices and check device binding limits

    Then I log into the account of user UID1 on device_2 and the verification status should be VERIFICATION_INITIATED

    Then The user UID1 submits OTP to log into the user account from device_2 and expects a status VERIFICATION_SUCCESS

    Then I authenticate the user UID1 from device - device_2 and expect a status of AUTHENTICATION_SUCCESSFUL

    Then I authorise the device_2 for the user UID1 and expect the device authorisation status of DEVICE_AUTHORISATION_INITIATED

    Then I initiate the HUGOBANK_BIO_VERISYS journey within the BIOMETRIC_VERIFICATION_STEP for user UID1 to authorise the device - device_2 and expect a status JOURNEY_INITIATED

    Then I update HUGOBANK_BIO_VERISYS journey within the BIOMETRIC_VERIFICATION_STEP for user UID1 as pass

    Then I process the HUGOBANK_BIO_VERISYS journey within the BIOMETRIC_VERIFICATION_STEP for user UID1 to authorise the device - device_2 and expect a status JOURNEY_PROCESSED

    Then I check status of the HUGOBANK_BIO_VERISYS journey within the BIOMETRIC_VERIFICATION_STEP for the user UID1 to authorise the device - device_2 and expect a status JOURNEY_PROCESSED

    Then I submit the HUGOBANK_BIO_VERISYS journey within the BIOMETRIC_VERIFICATION_STEP for user UID1 to authorise the device - device_2 and expect a status JOURNEY_SUBMITTED

    Then I submit the device authorisation of device_2 for user UID1 and expect a device authorisation status of DEVICE_AUTHORISATION_SUBMITTED

    Then I check the authorisation status of the device_2 for the user UID1 and expect a device authorisation status of DEVICE_AUTHORISATION_SUCCESS

    And Create a binding signature for the user UID1 to bind the device_2 and the device binding status should be ACTIVE

    Given I list all user devices for user UID1 and the user should have device_1,device_2

    Then I log into the account of user UID1 on device_3 and the verification status should be VERIFICATION_INITIATED

    Then The user UID1 submits OTP to log into the user account from device_3 and expects a status VERIFICATION_SUCCESS

    Then I authenticate the user UID1 from device - device_3 and expect a status of AUTHENTICATION_SUCCESSFUL

    Then I authorise the device_3 for the user UID1 and expect the device authorisation status of DEVICE_AUTHORISATION_INITIATED

    Then I initiate the HUGOBANK_BIO_VERISYS journey within the BIOMETRIC_VERIFICATION_STEP for user UID1 to authorise the device - device_3 and expect a status JOURNEY_INITIATED

    Then I update HUGOBANK_BIO_VERISYS journey within the BIOMETRIC_VERIFICATION_STEP for user UID1 as pass

    Then I process the HUGOBANK_BIO_VERISYS journey within the BIOMETRIC_VERIFICATION_STEP for user UID1 to authorise the device - device_3 and expect a status JOURNEY_PROCESSED

    Then I check status of the HUGOBANK_BIO_VERISYS journey within the BIOMETRIC_VERIFICATION_STEP for the user UID1 to authorise the device - device_3 and expect a status JOURNEY_PROCESSED

    Then I submit the HUGOBANK_BIO_VERISYS journey within the BIOMETRIC_VERIFICATION_STEP for user UID1 to authorise the device - device_3 and expect a status JOURNEY_SUBMITTED

    Then I submit the device authorisation of device_3 for user UID1 and expect a device authorisation status of DEVICE_AUTHORISATION_SUBMITTED

    Then I check the authorisation status of the device_3 for the user UID1 and expect a device authorisation status of DEVICE_AUTHORISATION_SUCCESS

    And Create a binding signature for the user UID1 to bind the device_3 and the device binding status should be ACTIVE

    Given I list all user devices for user UID1 and the user should have device_1,device_2,device_3

    Then I log into the account of user UID1 on device_4 and the verification status should be VERIFICATION_INITIATED

    Then The user UID1 submits OTP to log into the user account from device_4 and expects a status VERIFICATION_SUCCESS

    Then I authenticate the user UID1 from device - device_4 and expect a status of AUTHENTICATION_SUCCESSFUL

    Then I authorise the device_4 for the user UID1 and expect the device authorisation status of DEVICE_LIMIT_EXCEEDED

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

    Then I authorise the device_2 for the user UID1 and expect the device authorisation status of DEVICE_AUTHORISATION_INITIATED

    Then I initiate the HUGOBANK_BIO_VERISYS journey within the BIOMETRIC_VERIFICATION_STEP for user UID1 to authorise the device - device_2 and expect a status JOURNEY_INITIATED

    Then I update HUGOBANK_BIO_VERISYS journey within the BIOMETRIC_VERIFICATION_STEP for user UID1 as pass

    Then I process the HUGOBANK_BIO_VERISYS journey within the BIOMETRIC_VERIFICATION_STEP for user UID1 to authorise the device - device_2 and expect a status JOURNEY_PROCESSED

    Then I check status of the HUGOBANK_BIO_VERISYS journey within the BIOMETRIC_VERIFICATION_STEP for the user UID1 to authorise the device - device_2 and expect a status JOURNEY_PROCESSED

    Then I submit the HUGOBANK_BIO_VERISYS journey within the BIOMETRIC_VERIFICATION_STEP for user UID1 to authorise the device - device_2 and expect a status JOURNEY_SUBMITTED

    Then I submit the device authorisation of device_2 for user UID1 and expect a device authorisation status of DEVICE_AUTHORISATION_SUBMITTED

    Then I check the authorisation status of the device_2 for the user UID1 and expect a device authorisation status of DEVICE_AUTHORISATION_SUCCESS

    And Create a binding signature for the user UID1 to bind the device_2 and the device binding status should be ACTIVE

    Given I list all user devices for user UID1 and the user should have device_2

    Then I initiate the initial user authorisation to ADD_PAYEE for user UID1 and expect cool-off
