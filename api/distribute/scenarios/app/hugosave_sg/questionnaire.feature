Feature: Questionnaire Scenarios

  Background:

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

    Given I fetch list of questionnaire

    Given I check if questionnaire exists with name SUITABILITY_ASSESSMENT else create new questionnaire

    Then I fetch questionnaire SUITABILITY_ASSESSMENT and check status as QUESTIONNAIRE_ACTIVE

  Scenario: User Questionnaire Scenarios - create, update, submit

    Given I create questionnaire UQID1 for user UID1 - questionnaire SUITABILITY_ASSESSMENT

    Then I request to get user questionnaire UQID1 - SUITABILITY_ASSESSMENT for user UID1

    Then I request to update and verify user questionnaire answer UQID1 for user UID1 - questionnaire SUITABILITY_ASSESSMENT and expect a status code of 200

    Then I request to submit user questionnaire UQID1 for user UID1 and expect a status code of 200

    Then I verify score UQID1 for user UID1
