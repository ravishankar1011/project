Feature:  Create a new PREMIUM User Account

  Scenario: Create a new account for a user

    Given The user UID1 provides a valid mobile number on device_1 to initiate onboarding and the expected status is VERIFICATION_INITIATED
      | user_name | user_name_type | ph_prefix |
      | random    | PHONE_NUMBER   | +372      |

    Then The user UID1 submits OTP to proceed with verification and expects a status code of 200 and a status of VERIFICATION_SUCCESS

    Given I open a new HUGOSAVE user account and expect the status code 200
      | user_profile_identifier | email          | legal_name | name   | account_type |
      | UID1                    | test@gmail.com | John Doe   | Johnny | PERSONAL     |

    Then I initiate the initial onboarding of the user UID1 and expect a status INITIATED

    Then I submit the initial onboarding for UID1, the onboarding status should be IN_PROGRESS and the account level should be L0

    And I check the status of initial onboarding for UID1 and expect a onboarding status of COMPLETED

    And I get user details for user UID1 and the user profile status should be PROFILE_IN_PROGRESS

    Then I check the authorisation status of the device_1 for the user UID1 and expect a device authorisation status of DEVICE_AUTHORISATION_SUCCESS

    And Create a binding signature for the user UID1 to bind the device_1 and the device binding status should be ACTIVE

    Then I list all user devices for user UID1 and the user should have device_1

    And I check the user details to confirm if user UID1 is L0 and the user profile status should be PROFILE_ACTIVE

    When I initiate progress onboarding for the user UID1 to upgrade the account to L3 and expect an onboarding status of INITIATED

    Then I initiate the progress onboarding journey HUGOSAVE_SINGPASS within the ID_VERIFICATION_STEP for the user UID1 and expect a status of JOURNEY_INITIATED

    Then I update HUGOSAVE_SINGPASS journey within the ID_VERIFICATION_STEP for user UID1 as pass

    Then I process the progress onboarding journey HUGOSAVE_SINGPASS within the ID_VERIFICATION_STEP for user UID1, and expect a status JOURNEY_PROCESSED

    Then I check status of HUGOSAVE_SINGPASS journey within the ID_VERIFICATION_STEP for the user UID1, the status should be JOURNEY_PROCESSED

    And I submit the progress onboarding journey HUGOSAVE_SINGPASS within the ID_VERIFICATION_STEP for the user UID1 and expect the journey status to be JOURNEY_SUCCESSFUL

    Then I initiate the progress onboarding journey HUGOSAVE_ADDITIONAL_DETAILS within the ADDITIONAL_DETAILS_STEP for the user UID1 and expect a status of JOURNEY_INITIATED

    Then I update HUGOSAVE_ADDITIONAL_DETAILS journey within the ADDITIONAL_DETAILS_STEP for user UID1 as pass

    Then I process the progress onboarding journey HUGOSAVE_ADDITIONAL_DETAILS within the ADDITIONAL_DETAILS_STEP for user UID1, and expect a status JOURNEY_PROCESSED

    Then I check status of HUGOSAVE_ADDITIONAL_DETAILS journey within the ADDITIONAL_DETAILS_STEP for the user UID1, the status should be JOURNEY_PROCESSED

    And I submit the progress onboarding journey HUGOSAVE_ADDITIONAL_DETAILS within the ADDITIONAL_DETAILS_STEP for the user UID1 and expect the journey status to be JOURNEY_SUCCESSFUL

    Then I initiate the progress onboarding journey HUGOSAVE_TRUST within the TRUST_ACCEPTANCE_STEP for the user UID1 and expect a status of JOURNEY_INITIATED

    Then I process the progress onboarding journey HUGOSAVE_TRUST within the TRUST_ACCEPTANCE_STEP for user UID1, and expect a status JOURNEY_PROCESSED

    Then I check status of HUGOSAVE_TRUST journey within the TRUST_ACCEPTANCE_STEP for the user UID1, the status should be JOURNEY_PROCESSED

    And I submit the progress onboarding journey HUGOSAVE_TRUST within the TRUST_ACCEPTANCE_STEP for the user UID1 and expect the journey status to be JOURNEY_SUCCESSFUL

    Then I submit the progress onboarding for user UID1, the onboarding status should be IN_PROGRESS and the account level should be L3

    Given I update the onboarding status as ACCEPT if operator action status is OPERATOR_ACTION_REQUIRED for user UID1 to upgrade the account to level L3

    And I check progress onboarding status for the user UID1, the onboardingStatus status should be COMPLETED

    And I check the user details to confirm if user UID1 is L3 and the user profile status should be PROFILE_ACTIVE


  Scenario: Open User Account with Valid Referral Code

#user 1
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
#user 2
    Given The user UID2 provides a valid mobile number on device_1 to initiate onboarding and the expected status is VERIFICATION_INITIATED
      | user_name | user_name_type | ph_prefix |
      | random    | PHONE_NUMBER   | +378      |

    Then The user UID2 submits OTP to proceed with verification and expects a status code of 200 and a status of VERIFICATION_SUCCESS

    Given I open a new HUGOSAVE user account and expect the status code 200
      | user_profile_identifier | email          | legal_name | name   | account_type |
      | UID2                    | test@gmail.com | John Doe   | Johnny | PERSONAL     |

    Then I check the authorisation status of the device_1 for the user UID2 and expect a device authorisation status of DEVICE_AUTHORISATION_SUCCESS

    And Create a binding signature for the user UID2 to bind the device_1 and the device binding status should be ACTIVE

    And I check the user details to confirm if user UID2 is L3 and the user profile status should be PROFILE_ACTIVE

    Then I check the referral status of user UID2 with referee user as UID1

  Scenario: Open User Account with Invalid Referral Code

    Given The user UID2 provides a valid mobile number on device_1 to initiate onboarding and the expected status is VERIFICATION_INITIATED
      | user_name | user_name_type | ph_prefix |
      | random    | PHONE_NUMBER   | +372      |

    Then The user UID2 submits OTP to proceed with verification and expects a status code of 200 and a status of VERIFICATION_SUCCESS

    Given I open a new HUGOSAVE user account and expect the status code 200
      | user_profile_identifier | email          | legal_name | name   | account_type |
      | UID2                    | test@gmail.com | John Doe   | Johnny | PERSONAL     |

    Then I check the authorisation status of the device_1 for the user UID1 and expect a device authorisation status of DEVICE_AUTHORISATION_SUCCESS

    And Create a binding signature for the user UID1 to bind the device_1 and the device binding status should be ACTIVE

    And I check the user details to confirm if user UID1 is L3 and the user profile status should be PROFILE_ACTIVE

    Then I check the referral status of user UID1 with referee user as invalid

