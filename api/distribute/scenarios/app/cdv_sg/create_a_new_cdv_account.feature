Feature:  Create a new CDV User Account

  Scenario: Create a new account for a user

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
