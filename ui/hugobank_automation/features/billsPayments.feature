Feature: Bills and Payments

  Background:
    Given I sign up with bypass number
      | prefix | name  | place_of_birth | maiden_name |
      | +9247  | Ishaa | Sector 17B     | Fernandez   |

#  NOTE: The categories and their respective operators that can be tested are listed below
#      | Mobile                 | Electricity          | Gas            |
#      | Test Mobilink Prepaid  | Test-Electric        | TEST-SSGC      |
#      | Test Mobilink Postpaid | Test-Elec Connection | TEST-SNGPL     |
#      | Test Telenor Prepaid   |                      |                |
#      | Test Telenor Postpaid  |
#      | Test Bundle 70         |
#      | Test Bundle 349        |
#  prepaid prefix - 928+8digits and postpaid prefix - 9184+YY/MM/DD+random digits

  Scenario: Display error message for invalid Biller ID
    Given I tap on the Bills & Recharges and select the Mobile
    When I select the Test Mobilink Prepaid operator and tap on the Add Consumer card
    When I enter the mobile number 92232
    Then I tap on the Confirm button
    Then I should see the error message "Invalid Mobile Number"
    When I enter the mobile number Abcds@
    Then the confirm button should be disabled


  Scenario: Add a biller with missing, invalid, or valid names, discard the savings and handle OTP errors
    Given I tap on the Bills & Recharges and select the Mobile
    When I select the Test Mobilink Prepaid operator and tap on the Add Consumer card
    When I enter the mobile number 9281234567
    Then I tap on the Confirm button
    Then the 'Get OTP' button should be disabled
    Then I enter the biller nickname and validate the 'Get OTP' button
      | Name | Button state |
      | A    | disabled     |
      | Sara | enabled      |
    Then I tap on the Cancel button
    Then I tap on the Add Consumer card
    When I enter the mobile number 928123456789
    Then I tap on the Confirm button
    Then I enter the biller nickname and validate the 'Get OTP' button
      | Name | Button state |
      | Sara | enabled      |
    When I tap on the Get OTP button
    Then I navigate to the OTP screen, enter the OTPs, and verify the error messages
      | OTP    | Error message               |
      | 123455 | Incorrect OTP               |
      | 123459 | Incorrect OTP               |
      | 123459 | Incorrect OTP               |
      | 123455 | Please try after 29 minutes |


  Scenario: Add a biller with valid OTP and invalid passcodes
    Given I tap on the Bills & Recharges and select the Mobile
    When I select the Test Mobilink Prepaid operator and tap on the Add Consumer card
    When I enter the mobile number 928123456789
    Then I tap on the Confirm button
    Then I enter the biller nickname and validate the 'Get OTP' button
      | Name | Button state |
      | Sara | enabled      |
    When I tap on the Get OTP button
    When I provide the OTP 123456
    Then I navigate to the passcode screen, enter invalid passcodes, and verify the error messages
      | Passcode | Error message |
      | 212345   | Incorrect PIN |
      | 123459   | Incorrect PIN |
      | 123455   | Incorrect PIN |


  Scenario: Add a biller with valid OTP and passcode, then re-add the same biller under the same operator
    Given I tap on the Bills & Recharges and select the Mobile
    When I select the Test Mobilink Postpaid operator and tap on the Add Consumer card
    When I enter the mobile number 928123456789
    Then I tap on the Confirm button
    Then I enter the biller nickname and validate the 'Get OTP' button
      | Name | Button state |
      | Sara | enabled      |
    When I tap on the Get OTP button
    When I provide the OTP 123456
    Then I enter the passcode 123456
    Then I verify the biller name Sara on the individual biller screen
    Then I verify the biller card on the bill operator screen
      | Name | consumer number |
      | Sara | 928123456789    |
    Then I tap on the Add Consumer card
    When I enter the mobile number 928123456789
    Then I tap on the Confirm button
    Then I should see the error message for adding an existing biller
    Then I tap on the 'Go to Bill' and verify the biller name Sara on the individual biller screen


  Scenario: Add a biller and retry adding it with another operator
    Given I tap on the Bills & Recharges and select the Mobile
    When I select the Test Telenor Prepaid operator and tap on the Add Consumer card
    When I enter the mobile number 928123456789
    Then I tap on the Confirm button
    Then I enter the biller nickname and validate the 'Get OTP' button
      | Name | Button state |
      | Sara | enabled      |
    When I tap on the Get OTP button
    When I provide the OTP 123456
    Then I enter the passcode 123456
    Then I verify the biller name Sara on the individual biller screen
    Then I verify the biller card on the bill operator screen
      | Name | consumer number |
      | Sara | 928123456789    |
    When I tap on the back button
    When I select the Test Bundle 349 operator and tap on the Add Consumer card
    When I enter the mobile number 928123456789
    Then I tap on the Confirm button
    Then I enter the biller nickname and validate the 'Get OTP' button
      | Name | Button state |
      | Zara | enabled      |
    When I tap on the Get OTP button
    When I provide the OTP 123456
    Then I enter the passcode 123456
    Then I verify the biller name Zara on the individual biller screen
    Then I verify the biller card on the bill operator screen
      | Name | consumer number |
      | Zara | 928123456789    |


  Scenario: Edit biller details
    Given I tap on the Bills & Recharges and select the Mobile
    When I select the Test Bundle 349 operator and enter the mobile number 928123456789
    Then I enter the biller nickname and validate the 'Get OTP' button
      | Name | Button state |
      | Sara | enabled      |
    Then I provide the OTP 123456 and the passcode 123456
    Then I verify the biller name Sara on the individual biller screen
    When I tap on the "Edit Details" option and verify the biller details
      | Mobile Number | Service Operator | Nickname |
      | 928123456789  | Test Bundle 349  | Sara     |
    Then I update the biller nickname to Xara
    Then I verify the biller name Xara on the individual biller screen


  Scenario: Delete a biller
    Given I tap on the Bills & Recharges and select the Mobile
    When I select the Test Mobilink Prepaid operator and enter the mobile number 928123456789
    Then I enter the biller nickname and validate the 'Get OTP' button
      | Name | Button state |
      | Sara | enabled      |
    Then I provide the OTP 123456 and the passcode 123456
    Then I verify the biller name Sara on the individual biller screen
    Then I delete the Sara biller and verify if it is deleted


  Scenario: Verify payment input field with invalid inputs
    Given I have deposited 50 PKR into my account using non-prod options
    Given I tap on the Bills & Recharges and select the Mobile
    When I select the Test Mobilink Prepaid operator and enter the mobile number 928123456782
    Then I enter the biller nickname and validate the 'Get OTP' button
      | Name | Button state |
      | Sara | enabled      |
    Then I provide the OTP 123456 and the passcode 123456
    Then I verify the biller name Sara on the individual biller screen
    Then I navigate to the New Payment screen and verify the input field
      | Amount | Proceed button state |
      | 0      | disabled             |
      | abc    | disabled             |
    Then I enter the amount 100 and verify the error message 'Insufficient account balance'
    Then I tap on the Cancel button and re-visit the new payment screen
    Then I enter the amount 10 and navigate to the preview screen


  Scenario: Attempt to make a transaction with invalid passcodes
    Given I have deposited 500 PKR into my account using non-prod options
    Given I tap on the Bills & Recharges and select the Mobile
    When I select the Test Mobilink Prepaid operator and enter the mobile number 928123456789
    Then I enter the biller nickname and validate the 'Get OTP' button
      | Name | Button state |
      | Sara | enabled      |
    Then I provide the OTP 123456 and the passcode 123456
    Then I verify the biller name Sara on the individual biller screen
    Then I click on the Top-up button
    When I enter the amount 100
    Then I enter invalid passcodes, and verify the error messages
      | Passcode | Error message |
      | 212345   | Incorrect PIN |
      | 123459   | Incorrect PIN |
      | 123455   | Incorrect PIN |


  Scenario: Validate the bill payment transaction - Prepaid
    Given I have deposited 500 PKR into my account using non-prod options
    Given I tap on the Bills & Recharges and select the Mobile
    When I select the Test Telenor Prepaid operator and enter the mobile number 928123456789
    Then I enter the biller nickname and validate the 'Get OTP' button
      | Name | Button state |
      | Sara | enabled      |
    Then I provide the OTP 123456 and the passcode 123456
    Then I verify the biller name Sara on the individual biller screen
    Then I click on the Top-up button
    Then I enter the amount 100 and enter the passcode 123456
    Then I validate the transaction is Settled

  Scenario: Validate the bill payment transaction - Postpaid
    Given I have deposited 500 PKR into my account using non-prod options
    Given I tap on the Bills & Recharges and select the Mobile
    When I select the Test Mobilink Postpaid operator and enter the mobile number 918426123012
    Then I enter the biller nickname and validate the 'Get OTP' button
      | Name | Button state |
      | Sara | enabled      |
    Then I provide the OTP 123456 and the passcode 123456
    Then I verify the biller name Sara on the individual biller screen
    Then I click on the Pay button
    Then I enter the amount 100 and enter the passcode 123456
    Then I validate the transaction is Settled

  Scenario: Validate the bill payment transaction - Bundle
    Given I have deposited 500 PKR into my account using non-prod options
    Given I tap on the Bills & Recharges and select the Mobile
    When I select the Test Bundle 349 operator and enter the mobile number 928123456782
    Then I enter the biller nickname and validate the 'Get OTP' button
      | Name | Button state |
      | Sara | enabled      |
    Then I provide the OTP 123456 and the passcode 123456
    Then I verify the biller name Sara on the individual biller screen
    Then I click on the Select Bundle button
    Then I click the proceed, pay buttons and enter the passcode  123456
    Then I validate the transaction is Settled


  Scenario: Verify behavior when adding more than five consumers
    Given I tap on the Bills & Recharges and select the Mobile
    Then I select the Test Mobilink Prepaid operator
    Then I enter the mobile number, name, otp and passcode
      | Mobile Number | Nick name | Otp    | Passcode |
      | 928123456789  | sara      | 123456 | 123456   |
      | 928123456781  | jhon      | 123456 | 123456   |
      | 928123456782  | rock      | 123456 | 123456   |
      | 928123456783  | marc      | 123456 | 123456   |
      | 928123456784  | henry     | 123456 | 123456   |
    Then I check the 'Add consumer' button is in the disabled state


  Scenario: Attempt schedule creation with incomplete details
    Given I tap on the Bills & Recharges and select the Mobile
    When I select the Test Mobilink Prepaid operator and enter the mobile number 928123456789
    Then I enter the biller nickname and validate the 'Get OTP' button
      | Name | Button state |
      | Sara | enabled      |
    Then I provide the OTP 123456 and the passcode 123456
    Then I verify the biller name Sara on the individual biller screen
    When I navigate to the create schedule screen for the Prepaid operator
    When I create a new schedule with the following details
      | frequency | amount | start_date | make_payment | preview_button | bundle_schedule |
      | Weekly    |        |            |              | disabled       | False           |
      | Monthly   | 100    |            |              | disabled       | False           |
      | Weekly    | 20     |            | Once         | disabled       | False           |
      | Monthly   | ten    | today      | Once         | disabled       | False           |
      | Weekly    | 00     | today      | Twice        | disabled       | False           |
      | Daily     | 100    | today      | Once         | enabled        | False           |


  Scenario: Attempt schedule creation with complete details and edit details
    Given I tap on the Bills & Recharges and select the Mobile
    When I select the Test Mobilink Prepaid operator and enter the mobile number 928123456789
    Then I enter the biller nickname and validate the 'Get OTP' button
      | Name | Button state |
      | Sara | enabled      |
    Then I provide the OTP 123456 and the passcode 123456
    Then I verify the biller name Sara on the individual biller screen
    When I navigate to the create schedule screen for the Prepaid operator
    When I create a new schedule with the following details
      | frequency | amount | start_date | make_payment | preview_button | bundle_schedule |
      | Daily     | 200    | today      | Once         | enabled        | False           |
    When I click the Preview button and Confirm button
    Then I verify the newly created schedule is displayed in the biller dashboard
    When I navigate to the edit schedule screen
    When I edit the schedule with the following details
      | frequency | amount | make_payment | save_button |
      | Weekly    | 300    | Once         | enabled     |
    When I click the Save button
    Then I verify the edited schedule details in the biller dashboard


  Scenario: Verify the schedule transaction - prepaid
    Given I have deposited 500 PKR into my account using non-prod options
    Given I tap on the Bills & Recharges and select the Mobile
    When I select the Test Mobilink Prepaid operator and enter the mobile number 928123456789
    Then I enter the biller nickname and validate the 'Get OTP' button
      | Name | Button state |
      | Sara | enabled      |
    Then I provide the OTP 123456 and the passcode 123456
    Then I verify the biller name Sara on the individual biller screen
    When I navigate to the create schedule screen for the Prepaid operator
    When I create a new schedule with the following details
      | frequency | amount | start_date | make_payment | preview_button | bundle_schedule |
      | Daily     | 100    | today      | Once         | enabled        | False           |
    When I click the Preview button and Confirm button
    Then I verify the newly created schedule is displayed in the biller dashboard
    When I navigate to the home screen
    Then I trigger the schedule using non-prod options
    Then I navigate to the biller dashboard
      | operator              | biller name |
      | Test Mobilink Prepaid | Sara        |
    Then I verify the schedule transaction is Settled

  Scenario: Verify the schedule transaction - Bundle
    Given I have deposited 500 PKR into my account using non-prod options
    Given I tap on the Bills & Recharges and select the Mobile
    When I select the Test Bundle 349 operator and enter the mobile number 928123456789
    Then I enter the biller nickname and validate the 'Get OTP' button
      | Name | Button state |
      | Sara | enabled      |
    Then I provide the OTP 123456 and the passcode 123456
    Then I verify the biller name Sara on the individual biller screen
    When I navigate to the create schedule screen for the Bundle operator
    When I create a new schedule with the following details
      | frequency | amount | start_date | make_payment | preview_button | bundle_schedule |
      | Daily     | 1      | today      | Once         | enabled        | True            |
    When I click the Preview button and Confirm button
    Then I verify the newly created schedule is displayed in the biller dashboard
    When I navigate to the home screen
    Then I trigger the schedule using non-prod options
    Then I navigate to the biller dashboard
      | operator        | biller name |
      | Test Bundle 349 | Sara        |
    Then I verify the schedule transaction is Settled


  Scenario: Verify the schedule transaction is not triggered after stopping it
    Given I have deposited 500 PKR into my account using non-prod options
    Given I tap on the Bills & Recharges and select the Mobile
    When I select the Test Mobilink Prepaid operator and enter the mobile number 928123456789
    Then I enter the biller nickname and validate the 'Get OTP' button
      | Name | Button state |
      | Sara | enabled      |
    Then I provide the OTP 123456 and the passcode 123456
    Then I verify the biller name Sara on the individual biller screen
    When I navigate to the create schedule screen for the Prepaid operator
    When I create a new schedule with the following details
      | frequency | amount | start_date | make_payment | preview_button | bundle_schedule |
      | Quarterly | 300    | today      | Once         | enabled        | False               |
    When I click the Preview button and Confirm button
    Then I verify the newly created schedule is displayed in the biller dashboard
    When I stop the schedule
    When I navigate to the home screen
    Then I trigger the schedule using non-prod options
    Then I navigate to the biller dashboard
      | operator              | biller name |
      | Test Mobilink Prepaid | Sara        |
    Then I verify the schedule transaction is not occurred


  Scenario: Verify the schedule transaction is not triggered after skipping it
    Given I have deposited 500 PKR into my account using non-prod options
    Given I tap on the Bills & Recharges and select the Mobile
    When I select the Test Mobilink Prepaid operator and enter the mobile number 928123456789
    Then I enter the biller nickname and validate the 'Get OTP' button
      | Name | Button state |
      | Sara | enabled      |
    Then I provide the OTP 123456 and the passcode 123456
    Then I verify the biller name Sara on the individual biller screen
    When I navigate to the create schedule screen for the Prepaid operator
    When I create a new schedule with the following details
      | frequency | amount | start_date | make_payment | preview_button | bundle_schedule |
      | Monthly   | 300    | today      | Twice        | enabled        | False           |
    When I click the Preview button and Confirm button
    Then I verify the newly created schedule is displayed in the biller dashboard
    When I skip the schedule
    When I navigate to the home screen
    Then I trigger the schedule using non-prod options
    Then I navigate to the biller dashboard
      | operator              | biller name |
      | Test Mobilink Prepaid | Sara        |
    Then I verify the schedule transaction is not occurred
