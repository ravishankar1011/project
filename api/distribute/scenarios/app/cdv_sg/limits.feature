Feature:  Limits

  Background: : Create a new account for a user

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

  Scenario Outline: I edit the <limit_type> Limits - send more than set limit and send exactly set limit amount

    Then I get the user cash wallets for the user UID1 and expect the account status of CASH_ACCOUNT_STATUS_CREATED

     # add payee
    Then I initiate the initial user authorisation to ADD_PAYEE for user UID1 and expect a status of USER_AUTHORISATION_SUCCESS

    Then I initiate the final user authorisation to ADD_PAYEE and expect a user authorisation status as USER_AUTHORISATION_INITIATED for user UID1

    And I initiate the OTP journey within the OTP_STEP for user UID1 to authorise the user and expect a status JOURNEY_INITIATED

    Then I process the OTP journey within the OTP_STEP for user UID1 to authorise the user and expect a status JOURNEY_PROCESSED

    And I submit the OTP journey within the OTP_STEP for user UID1 to authorise the user and expect a status JOURNEY_SUCCESSFUL

    Then I submit the final user authorisation for ADD_PAYEE of user UID1 and expect a status USER_AUTHORISATION_SUBMITTED

    And I get the final user authorisation token for ADD_PAYEE of user UID1 and expect a status USER_AUTHORISATION_SUCCESS

      # We can test out other payment exchanges as well by changing the Country in the below feature step (while Adding a payee)
    Then I add the user UID2 as External Payee PID1 for the user UID1 with the Country IND and expect a status code of 200 and status of BENEFICIARY_STATUS_PENDING

    And I check if the user UID2 is added as a External Payee PID1 for the user UID1 and expect a status of BENEFICIARY_STATUS_CREATED

    Then I deposit 15000 USD into wallet with product code CASH_WALLET_DIGITAL for user UID1 and expect a status code of 200

    And I check the balance of the wallet with product code CASH_WALLET_DIGITAL for user UID1 and the balance should be 15000 USD exact

    Then I initiate the initial user authorisation to UPDATE_USER_TRANSACTION_LIMITS for user UID1 and expect a status of USER_AUTHORISATION_SUCCESS

    Then I initiate the final user authorisation to UPDATE_USER_TRANSACTION_LIMITS and expect a user authorisation status as USER_AUTHORISATION_INITIATED for user UID1

    And I initiate the PASSCODE journey within the PASSCODE_STEP for user UID1 to authorise the user and expect a status JOURNEY_INITIATED

    Then I process the PASSCODE journey within the PASSCODE_STEP for user UID1 to authorise the user and expect a status JOURNEY_PROCESSED

    And I submit the PASSCODE journey within the PASSCODE_STEP for user UID1 to authorise the user and expect a status JOURNEY_SUCCESSFUL

    Then I submit the final user authorisation for UPDATE_USER_TRANSACTION_LIMITS of user UID1 and expect a status USER_AUTHORISATION_SUBMITTED

    And I get the final user authorisation token for UPDATE_USER_TRANSACTION_LIMITS of user UID1 and expect a status USER_AUTHORISATION_SUCCESS

    Given I edit the <limit_type> limits for user UID1 to 10000 USD and expect a status code of 200

    Then I check if the hard limits are updated to 10000 for user UID1

      # pay payee - above set limits
    Then I initiate the initial user authorisation to PAY_PAYEE for user UID1 and expect a status of USER_AUTHORISATION_SUCCESS

    Then I initiate the final user authorisation to PAY_PAYEE and expect a user authorisation status as USER_AUTHORISATION_INITIATED for user UID1 with below soft limit

    And I initiate the OTP journey within the OTP_STEP for user UID1 to authorise the user and expect a status JOURNEY_INITIATED

    Then I process the OTP journey within the OTP_STEP for user UID1 to authorise the user and expect a status JOURNEY_PROCESSED

    And I submit the OTP journey within the OTP_STEP for user UID1 to authorise the user and expect a status JOURNEY_SUCCESSFUL

    Then I submit the final user authorisation for PAY_PAYEE of user UID1 and expect a status USER_AUTHORISATION_SUBMITTED

    And I get the final user authorisation token for PAY_PAYEE of user UID1 and expect a status USER_AUTHORISATION_SUCCESS

    Then I transfer 10100 USD from user UID1 to user UID2 with no reference and valid payee id and expect a status code of 200

    Then I wait for 5 seconds

    And I check the balance of the wallet with product code CASH_WALLET_DIGITAL for user UID1 and the balance should be 15000 USD exact

      # pay payee - exact set limits
    Then I initiate the initial user authorisation to PAY_PAYEE for user UID1 and expect a status of USER_AUTHORISATION_SUCCESS

    Then I initiate the final user authorisation to PAY_PAYEE and expect a user authorisation status as USER_AUTHORISATION_INITIATED for user UID1 with below soft limit

    And I initiate the OTP journey within the OTP_STEP for user UID1 to authorise the user and expect a status JOURNEY_INITIATED

    Then I process the OTP journey within the OTP_STEP for user UID1 to authorise the user and expect a status JOURNEY_PROCESSED

    And I submit the OTP journey within the OTP_STEP for user UID1 to authorise the user and expect a status JOURNEY_SUCCESSFUL

    Then I submit the final user authorisation for PAY_PAYEE of user UID1 and expect a status USER_AUTHORISATION_SUBMITTED

    And I get the final user authorisation token for PAY_PAYEE of user UID1 and expect a status USER_AUTHORISATION_SUCCESS

    Then I transfer 10000 USD from user UID1 to user UID2 with no reference and valid payee id and expect a status code of 200

    And I check the balance of the wallet with product code CASH_WALLET_DIGITAL for user UID1 and the balance should be 5000 USD exact

    Examples:
      | limit_type |
      | Daily      |
      | Monthly    |


