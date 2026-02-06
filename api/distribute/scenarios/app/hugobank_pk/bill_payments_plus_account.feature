Feature: Bill Payments for a PLUS account

  Background: Create 1 HUGOBANK PLUS account to test limits scenarios

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

  Scenario: Pay the Electricity Bill

    Then I get the user cash wallets for the user UID1 and expect the account status of CASH_ACCOUNT_STATUS_CREATED

    Then I deposit 70000 PKR into wallet with product code CASH_WALLET_CURRENT for user UID1 and expect a status code of 200

    And I check the balance of the wallet with product code CASH_WALLET_CURRENT for user UID1 and the balance should be 70000 PKR exact

    Given I list out all the available operators for ELECTRICITY Bill Payment for the user UID1

    Then I initiate the initial user authorisation to ADD_BILL_PAYEE for user UID1 and expect a status of USER_AUTHORISATION_SUCCESS

    Then I initiate the final user authorisation to ADD_BILL_PAYEE and expect a user authorisation status as USER_AUTHORISATION_INITIATED for user UID1

    And I initiate the OTP journey within the OTP_STEP for user UID1 to authorise the user and expect a status JOURNEY_INITIATED

    Then I process the OTP journey within the OTP_STEP for user UID1 to authorise the user and expect a status JOURNEY_PROCESSED

    And I submit the OTP journey within the OTP_STEP for user UID1 to authorise the user and expect a status JOURNEY_SUCCESSFUL

    And I initiate the PASSCODE journey within the PASSCODE_STEP for user UID1 to authorise the user and expect a status JOURNEY_INITIATED

    Then I process the PASSCODE journey within the PASSCODE_STEP for user UID1 to authorise the user and expect a status JOURNEY_PROCESSED

    And I submit the PASSCODE journey within the PASSCODE_STEP for user UID1 to authorise the user and expect a status JOURNEY_SUCCESSFUL

    Then I submit the final user authorisation for ADD_BILL_PAYEE of user UID1 and expect a status USER_AUTHORISATION_SUBMITTED

    And I get the final user authorisation token for ADD_BILL_PAYEE of user UID1 and expect a status USER_AUTHORISATION_SUCCESS

    Then I add a Consumer 91842508071342 to the service TESTFELECSCO for the user UID1 and expect the bill payee status BILL_PAYEE_INITIATED

    Then I fetch bill inquiry for user UID1 and expect a status BILL_UNPAID

    Then I initiate the initial user authorisation to PAY_BILL_PAYEE for user UID1 and expect a status of USER_AUTHORISATION_SUCCESS

    Then I initiate the final user authorisation to PAY_BILL_PAYEE and expect a user authorisation status as USER_AUTHORISATION_INITIATED for user UID1

    And I initiate the PASSCODE journey within the PASSCODE_STEP for user UID1 to authorise the user and expect a status JOURNEY_INITIATED

    Then I process the PASSCODE journey within the PASSCODE_STEP for user UID1 to authorise the user and expect a status JOURNEY_PROCESSED

    And I submit the PASSCODE journey within the PASSCODE_STEP for user UID1 to authorise the user and expect a status JOURNEY_SUCCESSFUL

    Then I submit the final user authorisation for PAY_BILL_PAYEE of user UID1 and expect a status USER_AUTHORISATION_SUBMITTED

    And I get the final user authorisation token for PAY_BILL_PAYEE of user UID1 and expect a status USER_AUTHORISATION_SUCCESS

    Then I make a Postpaid Bill Payment for the user UID1 and expect a intent status PENDING

    Then I verify below intent record in present in intents list
      | user_profile_identifier | product_code        | intent_type      | intent_status | count | view |
      | UID1                    | CASH_WALLET_CURRENT | PAY_BILL         | SETTLED       | 1     | cash |

  Scenario: Pay the Gas Bill

    Then I get the user cash wallets for the user UID1 and expect the account status of CASH_ACCOUNT_STATUS_CREATED

    Then I deposit 70000 PKR into wallet with product code CASH_WALLET_CURRENT for user UID1 and expect a status code of 200

    And I check the balance of the wallet with product code CASH_WALLET_CURRENT for user UID1 and the balance should be 70000 PKR exact

    Given I list out all the available operators for GAS_PAYMENTS Bill Payment for the user UID1

    Then I initiate the initial user authorisation to ADD_BILL_PAYEE for user UID1 and expect a status of USER_AUTHORISATION_SUCCESS

    Then I initiate the final user authorisation to ADD_BILL_PAYEE and expect a user authorisation status as USER_AUTHORISATION_INITIATED for user UID1

    And I initiate the OTP journey within the OTP_STEP for user UID1 to authorise the user and expect a status JOURNEY_INITIATED

    Then I process the OTP journey within the OTP_STEP for user UID1 to authorise the user and expect a status JOURNEY_PROCESSED

    And I submit the OTP journey within the OTP_STEP for user UID1 to authorise the user and expect a status JOURNEY_SUCCESSFUL

    And I initiate the PASSCODE journey within the PASSCODE_STEP for user UID1 to authorise the user and expect a status JOURNEY_INITIATED

    Then I process the PASSCODE journey within the PASSCODE_STEP for user UID1 to authorise the user and expect a status JOURNEY_PROCESSED

    And I submit the PASSCODE journey within the PASSCODE_STEP for user UID1 to authorise the user and expect a status JOURNEY_SUCCESSFUL

    Then I submit the final user authorisation for ADD_BILL_PAYEE of user UID1 and expect a status USER_AUTHORISATION_SUBMITTED

    And I get the final user authorisation token for ADD_BILL_PAYEE of user UID1 and expect a status USER_AUTHORISATION_SUCCESS

    Then I add a Consumer 91842508071342 to the service TEST-SSGC for the user UID1 and expect the bill payee status BILL_PAYEE_INITIATED

    Then I fetch bill inquiry for user UID1 and expect a status BILL_UNPAID

    Then I initiate the initial user authorisation to PAY_BILL_PAYEE for user UID1 and expect a status of USER_AUTHORISATION_SUCCESS

    Then I initiate the final user authorisation to PAY_BILL_PAYEE and expect a user authorisation status as USER_AUTHORISATION_INITIATED for user UID1

    And I initiate the PASSCODE journey within the PASSCODE_STEP for user UID1 to authorise the user and expect a status JOURNEY_INITIATED

    Then I process the PASSCODE journey within the PASSCODE_STEP for user UID1 to authorise the user and expect a status JOURNEY_PROCESSED

    And I submit the PASSCODE journey within the PASSCODE_STEP for user UID1 to authorise the user and expect a status JOURNEY_SUCCESSFUL

    Then I submit the final user authorisation for PAY_BILL_PAYEE of user UID1 and expect a status USER_AUTHORISATION_SUBMITTED

    And I get the final user authorisation token for PAY_BILL_PAYEE of user UID1 and expect a status USER_AUTHORISATION_SUCCESS

    Then I make a Postpaid Bill Payment for the user UID1 and expect a intent status PENDING

    Then I verify below intent record in present in intents list
      | user_profile_identifier | product_code        | intent_type      | intent_status | count | view |
      | UID1                    | CASH_WALLET_CURRENT | PAY_BILL         | SETTLED       | 1     | cash |

  Scenario: Pay the Water Bill

    Then I get the user cash wallets for the user UID1 and expect the account status of CASH_ACCOUNT_STATUS_CREATED

    Then I deposit 70000 PKR into wallet with product code CASH_WALLET_CURRENT for user UID1 and expect a status code of 200

    And I check the balance of the wallet with product code CASH_WALLET_CURRENT for user UID1 and the balance should be 70000 PKR exact

    Given I list out all the available operators for WATER Bill Payment for the user UID1

    Then I initiate the initial user authorisation to ADD_BILL_PAYEE for user UID1 and expect a status of USER_AUTHORISATION_SUCCESS

    Then I initiate the final user authorisation to ADD_BILL_PAYEE and expect a user authorisation status as USER_AUTHORISATION_INITIATED for user UID1

    And I initiate the OTP journey within the OTP_STEP for user UID1 to authorise the user and expect a status JOURNEY_INITIATED

    Then I process the OTP journey within the OTP_STEP for user UID1 to authorise the user and expect a status JOURNEY_PROCESSED

    And I submit the OTP journey within the OTP_STEP for user UID1 to authorise the user and expect a status JOURNEY_SUCCESSFUL

    And I initiate the PASSCODE journey within the PASSCODE_STEP for user UID1 to authorise the user and expect a status JOURNEY_INITIATED

    Then I process the PASSCODE journey within the PASSCODE_STEP for user UID1 to authorise the user and expect a status JOURNEY_PROCESSED

    And I submit the PASSCODE journey within the PASSCODE_STEP for user UID1 to authorise the user and expect a status JOURNEY_SUCCESSFUL

    Then I submit the final user authorisation for ADD_BILL_PAYEE of user UID1 and expect a status USER_AUTHORISATION_SUBMITTED

    And I get the final user authorisation token for ADD_BILL_PAYEE of user UID1 and expect a status USER_AUTHORISATION_SUCCESS

    Then I add a Consumer 91842508071340 to the service TEST-MWASA for the user UID1 and expect the bill payee status BILL_PAYEE_INITIATED

    Then I fetch bill inquiry for user UID1 and expect a status BILL_UNPAID

    Then I initiate the initial user authorisation to PAY_BILL_PAYEE for user UID1 and expect a status of USER_AUTHORISATION_SUCCESS

    Then I initiate the final user authorisation to PAY_BILL_PAYEE and expect a user authorisation status as USER_AUTHORISATION_INITIATED for user UID1

    And I initiate the PASSCODE journey within the PASSCODE_STEP for user UID1 to authorise the user and expect a status JOURNEY_INITIATED

    Then I process the PASSCODE journey within the PASSCODE_STEP for user UID1 to authorise the user and expect a status JOURNEY_PROCESSED

    And I submit the PASSCODE journey within the PASSCODE_STEP for user UID1 to authorise the user and expect a status JOURNEY_SUCCESSFUL

    Then I submit the final user authorisation for PAY_BILL_PAYEE of user UID1 and expect a status USER_AUTHORISATION_SUBMITTED

    And I get the final user authorisation token for PAY_BILL_PAYEE of user UID1 and expect a status USER_AUTHORISATION_SUCCESS

    Then I make a Postpaid Bill Payment for the user UID1 and expect a intent status PENDING

    Then I verify below intent record in present in intents list
      | user_profile_identifier | product_code        | intent_type      | intent_status | count | view |
      | UID1                    | CASH_WALLET_CURRENT | PAY_BILL         | SETTLED       | 1     | cash |

  Scenario: Pay the Mobile Recharge - Postpaid

    Then I get the user cash wallets for the user UID1 and expect the account status of CASH_ACCOUNT_STATUS_CREATED

    Then I deposit 70000 PKR into wallet with product code CASH_WALLET_CURRENT for user UID1 and expect a status code of 200

    And I check the balance of the wallet with product code CASH_WALLET_CURRENT for user UID1 and the balance should be 70000 PKR exact

    Given I list out all the available operators for MOBILE Bill Payment for the user UID1

    Then I initiate the initial user authorisation to ADD_BILL_PAYEE for user UID1 and expect a status of USER_AUTHORISATION_SUCCESS

    Then I initiate the final user authorisation to ADD_BILL_PAYEE and expect a user authorisation status as USER_AUTHORISATION_INITIATED for user UID1

    And I initiate the OTP journey within the OTP_STEP for user UID1 to authorise the user and expect a status JOURNEY_INITIATED

    Then I process the OTP journey within the OTP_STEP for user UID1 to authorise the user and expect a status JOURNEY_PROCESSED

    And I submit the OTP journey within the OTP_STEP for user UID1 to authorise the user and expect a status JOURNEY_SUCCESSFUL

    And I initiate the PASSCODE journey within the PASSCODE_STEP for user UID1 to authorise the user and expect a status JOURNEY_INITIATED

    Then I process the PASSCODE journey within the PASSCODE_STEP for user UID1 to authorise the user and expect a status JOURNEY_PROCESSED

    And I submit the PASSCODE journey within the PASSCODE_STEP for user UID1 to authorise the user and expect a status JOURNEY_SUCCESSFUL

    Then I submit the final user authorisation for ADD_BILL_PAYEE of user UID1 and expect a status USER_AUTHORISATION_SUBMITTED

    And I get the final user authorisation token for ADD_BILL_PAYEE of user UID1 and expect a status USER_AUTHORISATION_SUCCESS

    Then I add a Consumer 9184250810123 to the service Test Mobilink Postpaid for the user UID1 and expect the bill payee status BILL_PAYEE_INITIATED

    Then I fetch bill inquiry for user UID1 and expect a status BILL_UNPAID

    Then I initiate the initial user authorisation to PAY_BILL_PAYEE for user UID1 and expect a status of USER_AUTHORISATION_SUCCESS

    Then I initiate the final user authorisation to PAY_BILL_PAYEE and expect a user authorisation status as USER_AUTHORISATION_INITIATED for user UID1

    And I initiate the PASSCODE journey within the PASSCODE_STEP for user UID1 to authorise the user and expect a status JOURNEY_INITIATED

    Then I process the PASSCODE journey within the PASSCODE_STEP for user UID1 to authorise the user and expect a status JOURNEY_PROCESSED

    And I submit the PASSCODE journey within the PASSCODE_STEP for user UID1 to authorise the user and expect a status JOURNEY_SUCCESSFUL

    Then I submit the final user authorisation for PAY_BILL_PAYEE of user UID1 and expect a status USER_AUTHORISATION_SUBMITTED

    And I get the final user authorisation token for PAY_BILL_PAYEE of user UID1 and expect a status USER_AUTHORISATION_SUCCESS

    Then I make a Postpaid Bill Payment for the user UID1 and expect a intent status PENDING

    Then I verify below intent record in present in intents list
      | user_profile_identifier | product_code        | intent_type      | intent_status | count | view |
      | UID1                    | CASH_WALLET_CURRENT | PAY_BILL         | SETTLED       | 1     | cash |

  Scenario: Pay the Mobile Recharge - Prepaid

    Then I get the user cash wallets for the user UID1 and expect the account status of CASH_ACCOUNT_STATUS_CREATED

    Then I deposit 70000 PKR into wallet with product code CASH_WALLET_CURRENT for user UID1 and expect a status code of 200

    And I check the balance of the wallet with product code CASH_WALLET_CURRENT for user UID1 and the balance should be 70000 PKR exact

    Given I list out all the available operators for MOBILE Bill Payment for the user UID1

    Then I initiate the initial user authorisation to ADD_BILL_PAYEE for user UID1 and expect a status of USER_AUTHORISATION_SUCCESS

    Then I initiate the final user authorisation to ADD_BILL_PAYEE and expect a user authorisation status as USER_AUTHORISATION_INITIATED for user UID1

    And I initiate the OTP journey within the OTP_STEP for user UID1 to authorise the user and expect a status JOURNEY_INITIATED

    Then I process the OTP journey within the OTP_STEP for user UID1 to authorise the user and expect a status JOURNEY_PROCESSED

    And I submit the OTP journey within the OTP_STEP for user UID1 to authorise the user and expect a status JOURNEY_SUCCESSFUL

    And I initiate the PASSCODE journey within the PASSCODE_STEP for user UID1 to authorise the user and expect a status JOURNEY_INITIATED

    Then I process the PASSCODE journey within the PASSCODE_STEP for user UID1 to authorise the user and expect a status JOURNEY_PROCESSED

    And I submit the PASSCODE journey within the PASSCODE_STEP for user UID1 to authorise the user and expect a status JOURNEY_SUCCESSFUL

    Then I submit the final user authorisation for ADD_BILL_PAYEE of user UID1 and expect a status USER_AUTHORISATION_SUBMITTED

    And I get the final user authorisation token for ADD_BILL_PAYEE of user UID1 and expect a status USER_AUTHORISATION_SUCCESS

    Then I add a Consumer 92887329 to the service Test Mobilink Prepaid for the user UID1 and expect the bill payee status BILL_PAYEE_INITIATED

    Then I fetch bill inquiry for user UID1 and expect a status BILL_PAYEE_CREATED

    Then I initiate the initial user authorisation to PAY_BILL_PAYEE for user UID1 and expect a status of USER_AUTHORISATION_SUCCESS

    Then I initiate the final user authorisation to PAY_BILL_PAYEE and expect a user authorisation status as USER_AUTHORISATION_INITIATED for user UID1

    And I initiate the PASSCODE journey within the PASSCODE_STEP for user UID1 to authorise the user and expect a status JOURNEY_INITIATED

    Then I process the PASSCODE journey within the PASSCODE_STEP for user UID1 to authorise the user and expect a status JOURNEY_PROCESSED

    And I submit the PASSCODE journey within the PASSCODE_STEP for user UID1 to authorise the user and expect a status JOURNEY_SUCCESSFUL

    Then I submit the final user authorisation for PAY_BILL_PAYEE of user UID1 and expect a status USER_AUTHORISATION_SUBMITTED

    And I get the final user authorisation token for PAY_BILL_PAYEE of user UID1 and expect a status USER_AUTHORISATION_SUCCESS

    Then I make a Prepaid Bill Payment of amount 1121 for the user UID1 and expect a intent status PENDING

    Then I verify below intent record in present in intents list
      | user_profile_identifier | product_code        | intent_type | intent_status | count | view |
      | UID1                    | CASH_WALLET_CURRENT | PAY_BILL    | SETTLED       | 1     | cash |

  Scenario: Pay the Mobile Recharge payment - Prepaid (schedules for prepaid bill payments)

    Then I get the user cash wallets for the user UID1 and expect the account status of CASH_ACCOUNT_STATUS_CREATED

    Then I deposit 50000 PKR into wallet with product code CASH_WALLET_CURRENT for user UID1 and expect a status code of 200

    And I check the balance of the wallet with product code CASH_WALLET_CURRENT for user UID1 and the balance should be 50000 PKR exact

    Given I list out all the available operators for MOBILE Bill Payment for the user UID1

    Then I initiate the initial user authorisation to ADD_BILL_PAYEE for user UID1 and expect a status of USER_AUTHORISATION_SUCCESS

    Then I initiate the final user authorisation to ADD_BILL_PAYEE and expect a user authorisation status as USER_AUTHORISATION_INITIATED for user UID1

    And I initiate the OTP journey within the OTP_STEP for user UID1 to authorise the user and expect a status JOURNEY_INITIATED

    Then I process the OTP journey within the OTP_STEP for user UID1 to authorise the user and expect a status JOURNEY_PROCESSED

    And I submit the OTP journey within the OTP_STEP for user UID1 to authorise the user and expect a status JOURNEY_SUCCESSFUL

    And I initiate the PASSCODE journey within the PASSCODE_STEP for user UID1 to authorise the user and expect a status JOURNEY_INITIATED

    Then I process the PASSCODE journey within the PASSCODE_STEP for user UID1 to authorise the user and expect a status JOURNEY_PROCESSED

    And I submit the PASSCODE journey within the PASSCODE_STEP for user UID1 to authorise the user and expect a status JOURNEY_SUCCESSFUL

    Then I submit the final user authorisation for ADD_BILL_PAYEE of user UID1 and expect a status USER_AUTHORISATION_SUBMITTED

    And I get the final user authorisation token for ADD_BILL_PAYEE of user UID1 and expect a status USER_AUTHORISATION_SUCCESS

    Then I add a Consumer 92887329 to the service Test Mobilink Prepaid for the user UID1 and expect the bill payee status BILL_PAYEE_INITIATED

    Then I create a schedule for Bill Payments BPID1 and expect status 200
      | user_profile_identifier | schedule_identifier | frequency | schedule_type          | product_code        | target_weekdays | target_week | amount |
      | UID1                    | SID1                | DAILY     | SCHEDULE_BILL_PAYMENTS | CASH_WALLET_CURRENT |                 | 1           | 10000  |

    Then I check if the schedule SID1 has a status code of 200 and a status of SCHEDULE_STATUS_ACTIVE for user UID1

    Then I trigger schedule SID1 for user UID1 and expect a status code of 200

    And I check the balance of the wallet with product code CASH_WALLET_CURRENT for user UID1 and the balance should be 40000 PKR approx
